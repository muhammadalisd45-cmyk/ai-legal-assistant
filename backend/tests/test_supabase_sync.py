"""Incremental Supabase publishing: updated laws replace superseded text; nothing else is touched (offline)."""
import json
from urllib.parse import parse_qs, urlparse

import httpx
import numpy as np

from app.legal.supabase_sync import SupabaseRest, chunk_payload, plan_publish, vectors_for


def chunk(cid, doc="PB-001", content="text", title="Punjab Consumer Protection Act, 2005", url="https://x/v1.pdf"):
    return {"chunk_id": cid, "chunk_index": 0, "document_id": doc, "title": title, "section_or_article": "Section 1",
            "section_heading": "", "content": content, "content_hash": f"h:{content}", "source_url": url,
            "fetched_at": ""}


class FakeSupabase:
    """In-memory PostgREST stand-in for the two tables the publisher touches."""

    def __init__(self, chunks=(), documents=()):
        self.tables = {"legal_chunks": {c["chunk_id"]: dict(c) for c in chunks},
                       "legal_documents": {d: {"document_id": d} for d in documents}}
        self.calls = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        table = urlparse(str(request.url)).path.rsplit("/", 1)[-1]
        rows = self.tables[table]
        key = "chunk_id" if table == "legal_chunks" else "document_id"
        params = parse_qs(urlparse(str(request.url)).query)
        self.calls.append((request.method, table))
        if request.method == "GET":
            ordered = [rows[k] for k in sorted(rows)]
            offset, limit = int(params["offset"][0]), int(params["limit"][0])
            return httpx.Response(200, json=ordered[offset:offset + limit])
        if request.method == "POST":
            for row in json.loads(request.content):
                rows[row[key]] = {**rows.get(row[key], {}), **row}
            return httpx.Response(201)
        if request.method == "DELETE":
            values = params[key][0][len("in.("):-1].split(",")
            for value in values:
                rows.pop(value.strip('"'), None)
                if table == "legal_documents":  # ON DELETE CASCADE
                    for cid in [c for c, r in self.tables["legal_chunks"].items() if r["document_id"] == value.strip('"')]:
                        self.tables["legal_chunks"].pop(cid)
            return httpx.Response(204)
        return httpx.Response(405)


def test_amended_law_replaces_superseded_chunks_and_leaves_the_rest():
    remote = [chunk("PB-001-s1", content="old s1"), chunk("PB-001-s2", content="old s2"),
              chunk("PB-001-s3", content="repealed s3"), chunk("PK-002-s1", doc="PK-002", content="ppc")]
    local = [chunk("PB-001-s1", content="new s1", url="https://x/v2.pdf"),   # amended text, new official PDF
             chunk("PB-001-s2", content="old s2"),                            # unchanged
             chunk("PK-002-s1", doc="PK-002", content="ppc")]                 # unchanged
    fake = FakeSupabase(remote, documents=["PB-001", "PK-002", "PB-999"])
    api = SupabaseRest("https://example.supabase.co", "secret", httpx.Client(transport=httpx.MockTransport(fake.handler)))
    remote_rows = {r["chunk_id"]: r for r in api.select_all("legal_chunks", ["chunk_id"], "chunk_id")}
    remote_docs = {r["document_id"] for r in api.select_all("legal_documents", ["document_id"], "document_id")}
    plan = plan_publish(local, remote_rows, {"PB-001", "PK-002"}, remote_docs)
    assert [local[i]["chunk_id"] for i in plan.upsert] == ["PB-001-s1"]
    assert plan.delete_chunks == ["PB-001-s3"] and plan.drop_documents == ["PB-999"] and plan.unchanged == 2

    api.upsert("legal_chunks", [chunk_payload(local[i], np.zeros(384)) for i in plan.upsert], "chunk_id")
    api.delete_in("legal_chunks", "chunk_id", plan.delete_chunks)
    api.delete_in("legal_documents", "document_id", plan.drop_documents)
    published = fake.tables["legal_chunks"]
    assert sorted(published) == ["PB-001-s1", "PB-001-s2", "PK-002-s1"]
    assert published["PB-001-s1"]["content"] == "new s1" and published["PB-001-s1"]["source_url"].endswith("v2.pdf")
    assert "PB-999" not in fake.tables["legal_documents"]


def test_unchanged_corpus_publishes_nothing():
    rows = [chunk(f"c{i}", content=f"t{i}") for i in range(5)]
    plan = plan_publish(rows, {r["chunk_id"]: r for r in rows}, {"PB-001"}, {"PB-001"})
    assert plan.summary() == {"upsert_chunks": 0, "delete_chunks": 0, "drop_documents": 0, "unchanged_chunks": 5}
    assert len(plan_publish(rows, {r["chunk_id"]: r for r in rows}, {"PB-001"}, {"PB-001"}, full=True).upsert) == 5


def test_select_all_pages_through_large_tables():
    fake = FakeSupabase([chunk(f"c{i:05d}", content=str(i)) for i in range(2500)])
    api = SupabaseRest("https://example.supabase.co", "secret", httpx.Client(transport=httpx.MockTransport(fake.handler)))
    assert len(api.select_all("legal_chunks", ["chunk_id"], "chunk_id")) == 2500


def test_vectors_are_reused_and_only_changed_text_is_embedded():
    class Counting:
        calls = 0

        def embed(self, texts):
            Counting.calls += len(texts)
            return np.ones((len(texts), 384), dtype=np.float32)

    chunks = [chunk("a", content="same"), chunk("b", content="changed")]
    matrix = np.full((2, 384), 0.5, dtype=np.float32)
    # Local matrix aligned with the *current* chunks: both reusable, nothing embedded.
    assert set(vectors_for([0, 1], chunks, matrix, Counting())) == {0, 1} and Counting.calls == 0
    # No local vectors at all (e.g. CI without the .npy): only the requested chunks are embedded.
    out = vectors_for([1], chunks, None, Counting())
    assert list(out) == [1] and Counting.calls == 1
