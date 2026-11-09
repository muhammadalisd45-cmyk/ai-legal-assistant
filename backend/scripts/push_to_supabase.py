"""Phase 6 — upload the verified chunk index (with 384-d embeddings) to Supabase pgvector.

Requires SUPABASE_URL and SUPABASE_SECRET_KEY (service role, server-side only) and migrations 001–005.
Usage:  python scripts/push_to_supabase.py [--batch 200]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.acquisition import load_provenance  # noqa: E402
from app.legal.embeddings import EXPECTED_DIM  # noqa: E402
from app.legal.index import LocalIndex  # noqa: E402
from app.legal.manifest import load_manifest  # noqa: E402

CHUNK_COLUMNS = ("chunk_id", "chunk_index", "document_id", "title", "document_type", "jurisdiction", "court", "bench",
                 "authority", "citation", "section_or_article", "section_heading", "section_confidence", "page_start",
                 "page_end", "source_name", "source_url", "source_tier", "content", "content_hash", "file_sha256",
                 "fetched_at")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=200)
    args = parser.parse_args()
    url, secret = settings.supabase_url.rstrip("/"), settings.supabase_secret_key
    if not url or not secret:
        raise SystemExit("Set SUPABASE_URL and SUPABASE_SECRET_KEY (server-side only).")
    index, status = LocalIndex.load(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path)
    if not index.size:
        raise SystemExit("Chunk index is empty. Run scripts/acquire_corpus.py and scripts/build_index.py first.")
    if index.embeddings is None:
        print(f"WARNING: no aligned embeddings ({status.problem or 'missing'}); pushing lexical-only chunks.")
    elif index.embeddings.shape[1] != EXPECTED_DIM:
        raise SystemExit("Embedding dimension mismatch with vector(384).")

    headers = {"apikey": secret, "Authorization": f"Bearer {secret}", "Content-Type": "application/json",
               "Prefer": "resolution=merge-duplicates,return=minimal"}
    provenance = load_provenance(settings.provenance_path).get("documents", {})
    ingested = {c["document_id"] for c in index.chunks}
    with httpx.Client(timeout=60) as client:
        # 1. Document registry (FK target) with provenance in metadata.
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
                             "validation_ok": (prov.get("validation") or {}).get("ok")},
            })
        client.post(f"{url}/rest/v1/legal_documents?on_conflict=document_id", headers=headers, json=docs).raise_for_status()
        print(f"upserted {len(docs)} legal_documents")

        # 2. Chunks + embeddings.
        for start in range(0, index.size, args.batch):
            batch = []
            for i in range(start, min(start + args.batch, index.size)):
                chunk = index.chunks[i]
                item = {key: chunk.get(key) for key in CHUNK_COLUMNS}
                item["fetched_at"] = item["fetched_at"] or None
                if index.embeddings is not None:
                    item["embedding"] = "[" + ",".join(f"{v:.6f}" for v in np.asarray(index.embeddings[i]).tolist()) + "]"
                batch.append(item)
            client.post(f"{url}/rest/v1/legal_chunks?on_conflict=chunk_id", headers=headers, json=batch).raise_for_status()
            print(f"pushed {min(start + args.batch, index.size)}/{index.size} chunks")
    print(json.dumps({"documents": sorted(ingested), "chunks": index.size, "embeddings": index.embeddings is not None}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
