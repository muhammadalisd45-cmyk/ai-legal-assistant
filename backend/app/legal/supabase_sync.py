"""Incremental publishing of the local legal index to Supabase (pgvector), so production search goes live with
updated law without a redeploy.

Why incremental and why deletes matter: when an official PDF is replaced (an amended, consolidated text), its
chunks change. Upserting the new chunks is not enough: chunks of the old version that no longer exist must be
deleted, or users could be shown superseded text. The plan therefore has three parts:

  upsert  local chunks that are missing remotely or whose content/title/section/source changed
  delete  remote chunks that are no longer in the local index (stale versions, quarantined documents)
  drop    remote documents that are no longer in the manifest (their chunks cascade)

Embeddings are taken from the local .npy where the exact embedded text matches, else computed for just the
changed chunks, so a weekly publish embeds a handful of chunks, not ten thousand.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Iterable

import httpx
import numpy as np

from app.legal.index import embedding_key, embedding_text

CHUNK_COLUMNS = ("chunk_id", "chunk_index", "document_id", "title", "document_type", "jurisdiction", "court", "bench",
                 "authority", "citation", "section_or_article", "section_heading", "section_confidence", "page_start",
                 "page_end", "source_name", "source_url", "source_tier", "content", "content_hash", "file_sha256",
                 "fetched_at")
# Columns compared to decide whether a remote chunk is stale (small, so the remote snapshot is cheap to read).
COMPARE_COLUMNS = ("chunk_id", "document_id", "content_hash", "title", "section_or_article", "source_url")
PAGE = 1000


@dataclass
class PublishPlan:
    upsert: list[int] = field(default_factory=list)      # indexes into local chunks
    delete_chunks: list[str] = field(default_factory=list)
    drop_documents: list[str] = field(default_factory=list)
    unchanged: int = 0

    def summary(self) -> dict:
        return {"upsert_chunks": len(self.upsert), "delete_chunks": len(self.delete_chunks),
                "drop_documents": len(self.drop_documents), "unchanged_chunks": self.unchanged}


def fingerprint(chunk: dict) -> tuple:
    return tuple(str(chunk.get(column) or "") for column in COMPARE_COLUMNS)


def plan_publish(local_chunks: list[dict], remote_chunks: dict[str, dict], manifest_ids: set[str],
                 remote_document_ids: set[str], full: bool = False) -> PublishPlan:
    plan = PublishPlan()
    local_ids = set()
    for index, chunk in enumerate(local_chunks):
        local_ids.add(chunk["chunk_id"])
        remote = remote_chunks.get(chunk["chunk_id"])
        if full or remote is None or fingerprint(remote) != fingerprint(chunk):
            plan.upsert.append(index)
        else:
            plan.unchanged += 1
    plan.delete_chunks = sorted(cid for cid in remote_chunks if cid not in local_ids)
    plan.drop_documents = sorted(remote_document_ids - manifest_ids)
    return plan


def vectors_for(indexes: list[int], chunks: list[dict], local_matrix: np.ndarray | None, embedder,
                log=print) -> dict[int, np.ndarray]:
    """Vectors for the chunks to upsert: reuse the local index's vector when the embedded text is identical."""
    reuse: dict[str, np.ndarray] = {}
    if local_matrix is not None and local_matrix.shape[0] == len(chunks):
        reuse = {embedding_key(chunk): local_matrix[i] for i, chunk in enumerate(chunks)}
    out: dict[int, np.ndarray] = {}
    missing = []
    for i in indexes:
        key = embedding_key(chunks[i])
        if key in reuse:
            out[i] = reuse[key]
        else:
            missing.append(i)
    if missing:
        if embedder is None:
            raise RuntimeError(f"{len(missing)} chunks need embeddings but no embedder is available")
        for start in range(0, len(missing), 128):
            part = missing[start:start + 128]
            for i, vector in zip(part, embedder.embed([embedding_text(chunks[i]) for i in part])):
                out[i] = np.asarray(vector, dtype=np.float32)
            log(f"embedded {min(start + 128, len(missing))}/{len(missing)} changed chunks")
    return out


class SupabaseRest:
    """Minimal PostgREST client using the server-side secret key (never ship this key to a browser)."""

    def __init__(self, url: str, secret: str, client: httpx.Client | None = None):
        self.base = url.rstrip("/") + "/rest/v1"
        self.headers = {"apikey": secret, "Authorization": f"Bearer {secret}", "Content-Type": "application/json"}
        self.client = client or httpx.Client(timeout=120)

    def select_all(self, table: str, columns: Iterable[str], order: str) -> list[dict]:
        rows: list[dict] = []
        offset = 0
        while True:
            response = self.client.get(f"{self.base}/{table}", headers=self.headers,
                                       params={"select": ",".join(columns), "order": order,
                                               "limit": PAGE, "offset": offset})
            response.raise_for_status()
            page = response.json()
            rows.extend(page)
            if len(page) < PAGE:
                return rows
            offset += PAGE

    def upsert(self, table: str, rows: list[dict], conflict: str) -> None:
        if not rows:
            return
        headers = self.headers | {"Prefer": "resolution=merge-duplicates,return=minimal"}
        self.client.post(f"{self.base}/{table}?on_conflict={conflict}", headers=headers,
                         content=json.dumps(rows, ensure_ascii=False)).raise_for_status()

    def delete_in(self, table: str, column: str, values: list[str], batch: int = 100) -> None:
        for start in range(0, len(values), batch):
            quoted = ",".join('"' + v.replace('"', '\\"') + '"' for v in values[start:start + batch])
            self.client.delete(f"{self.base}/{table}", headers=self.headers | {"Prefer": "return=minimal"},
                               params={column: f"in.({quoted})"}).raise_for_status()

    def close(self) -> None:
        self.client.close()


def chunk_payload(chunk: dict, vector: np.ndarray | None) -> dict:
    item = {key: chunk.get(key) for key in CHUNK_COLUMNS}
    item["fetched_at"] = item["fetched_at"] or None
    if vector is not None:
        item["embedding"] = "[" + ",".join(f"{v:.6f}" for v in np.asarray(vector).tolist()) + "]"
    return item
