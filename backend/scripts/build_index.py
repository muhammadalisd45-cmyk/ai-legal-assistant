"""Phase 5/6 — extract, clean, chunk and embed the verified corpus.

Usage:  python scripts/build_index.py [--no-embeddings] [--full]

Embeddings are reused for chunks whose exact text is unchanged since the last build (same model), so routine
updates only embed new or changed provisions. --full re-embeds everything.
Writes frontend/data/rag_index/legal_chunks.jsonl (+ legal_chunk_embeddings.npy / .meta.json).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.embeddings import FastEmbedEmbedder  # noqa: E402
from app.legal.index import build_chunk_rows, previous_vectors, write_index  # noqa: E402
from app.legal.manifest import load_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-embeddings", action="store_true")
    parser.add_argument("--full", action="store_true", help="re-embed every chunk instead of reusing vectors")
    args = parser.parse_args()
    started = time.time()
    rows = load_manifest(settings.manifest_path)
    chunk_rows = build_chunk_rows(rows, settings.corpus_dir, settings.provenance_path)
    if not chunk_rows:
        print("No verified PDFs found. Run scripts/acquire_corpus.py first.", file=sys.stderr)
        return 1
    embedder = None if args.no_embeddings else FastEmbedEmbedder()
    reuse = {} if (embedder is None or args.full) else previous_vectors(
        settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path, embedder.name)
    meta = write_index(chunk_rows, settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path, embedder,
                       reuse=reuse)
    labelled = sum(1 for r in chunk_rows if r["section_or_article"])
    print(json.dumps({
        "chunks": meta["chunk_count"], "documents": meta["documents"],
        "chunks_with_section_label": labelled,
        "embedding_model": meta["embedding_model"], "embedding_dim": meta["embedding_dim"],
        "embeddings_reused": meta.get("embeddings_reused", 0),
        "seconds": round(time.time() - started, 1),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
