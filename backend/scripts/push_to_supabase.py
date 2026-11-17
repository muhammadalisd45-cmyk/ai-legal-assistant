"""Publish the verified legal index to Supabase pgvector — incrementally, including deletions.

    python scripts/push_to_supabase.py              # upsert changed chunks, delete stale ones, sync registry
    python scripts/push_to_supabase.py --dry-run    # show what would change, write nothing
    python scripts/push_to_supabase.py --full       # re-upload every chunk (e.g. after changing the embedding model)

Requires SUPABASE_URL and SUPABASE_SECRET_KEY (service role, server-side only) and migrations 001–005.
Production search (RETRIEVAL_BACKEND=auto with the secret key set) reads Supabase directly, so new and amended
laws are live as soon as this finishes — no redeploy. Used by .github/workflows/publish-legal-corpus.yml.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.acquisition import load_provenance  # noqa: E402
from app.legal.embeddings import EXPECTED_DIM  # noqa: E402
from app.legal.index import LocalIndex  # noqa: E402
from app.legal.manifest import load_manifest  # noqa: E402
from app.legal.source_sync import load_inventory  # noqa: E402
from app.legal.supabase_sync import (  # noqa: E402
    COMPARE_COLUMNS, SupabaseRest, chunk_payload, plan_publish, vectors_for,
)


def document_rows(ingested: set[str]) -> list[dict]:
    provenance = load_provenance(settings.provenance_path).get("documents", {})
    # "Official source last checked" per corpus document, from the source-sync inventory (shown as "as of").
    last_checked: dict[str, str] = {}
    for row in load_inventory().values():
        if row.get("manifest_id"):
            last_checked[row["manifest_id"]] = max(last_checked.get(row["manifest_id"], ""), row.get("last_seen", ""))
    docs = []
    for row in load_manifest(settings.manifest_path):
        prov = provenance.get(row.document_id, {})
        docs.append({
            "document_id": row.document_id, "title": row.title, "document_type": row.document_type,
            "jurisdiction": row.jurisdiction, "court": row.court or None, "bench": row.bench or None,
            "authority": row.authority, "citation": row.citation or None, "language": row.language,
            "source_url": row.source_url, "file_name": row.file_name or None,
            "status": "ingested" if row.document_id in ingested else row.status, "source_tier": row.source_tier,
            "metadata": {"source_name": row.source_name, "priority": row.priority,
                         "sha256": prov.get("sha256"), "fetched_at": prov.get("fetched_at"),
                         "validation_ok": (prov.get("validation") or {}).get("ok"),
                         "source_last_checked": last_checked.get(row.document_id) or None},
        })
    return docs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch", type=int, default=200)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--full", action="store_true", help="re-upload every chunk")
    args = parser.parse_args()
    url, secret = settings.supabase_url.rstrip("/"), settings.supabase_secret_key
    if not url or not secret:
        raise SystemExit("Set SUPABASE_URL and SUPABASE_SECRET_KEY (server-side only).")

    started = time.time()
    index, status = LocalIndex.load(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path)
    if not index.size:
        raise SystemExit("Chunk index is empty. Run scripts/acquire_corpus.py and scripts/build_index.py first.")
    matrix = index.embeddings
    if matrix is not None and matrix.shape[1] != EXPECTED_DIM:
        raise SystemExit("Embedding dimension mismatch with vector(384).")
    chunks = index.chunks
    ingested = {c["document_id"] for c in chunks}
    docs = document_rows(ingested)
    manifest_ids = {d["document_id"] for d in docs}

    api = SupabaseRest(url, secret)
    try:
        remote = {r["chunk_id"]: r for r in api.select_all("legal_chunks", COMPARE_COLUMNS, "chunk_id")}
        remote_docs = {r["document_id"] for r in api.select_all("legal_documents", ["document_id"], "document_id")}
        plan = plan_publish(chunks, remote, manifest_ids, remote_docs, full=args.full)
        print(json.dumps({"remote_chunks": len(remote), "local_chunks": len(chunks), **plan.summary()}, indent=2))
        if args.dry_run:
            return 0

        # 1. Registry first (chunks reference it).
        api.upsert("legal_documents", docs, "document_id")
        print(f"upserted {len(docs)} legal_documents")

        # 2. Changed / new chunks with embeddings (reused when the embedded text is unchanged).
        from app.legal.embeddings import FastEmbedEmbedder

        # FastEmbedEmbedder loads its model lazily, on the first embed() call, i.e. only if some chunk's
        # vector cannot be reused from the local index.
        vectors = vectors_for(plan.upsert, chunks, matrix, FastEmbedEmbedder())
        for start in range(0, len(plan.upsert), args.batch):
            part = plan.upsert[start:start + args.batch]
            api.upsert("legal_chunks", [chunk_payload(chunks[i], vectors.get(i)) for i in part], "chunk_id")
            print(f"upserted {min(start + args.batch, len(plan.upsert))}/{len(plan.upsert)} chunks")

        # 3. Remove superseded chunks, then documents no longer in the manifest (their chunks cascade).
        api.delete_in("legal_chunks", "chunk_id", plan.delete_chunks)
        if plan.delete_chunks:
            print(f"deleted {len(plan.delete_chunks)} stale chunks")
        api.delete_in("legal_documents", "document_id", plan.drop_documents)
        if plan.drop_documents:
            print(f"deleted {len(plan.drop_documents)} documents no longer in the manifest")
    finally:
        api.close()
    print(json.dumps({"documents": len(docs), "chunks": len(chunks), "embeddings": matrix is not None,
                      "seconds": round(time.time() - started, 1), **plan.summary()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
