"""Phase 5 — download official PDFs listed in the manifest and record provenance.

Usage:  python scripts/acquire_corpus.py [--force] [--only PK-001,PK-008]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.acquisition import acquire  # noqa: E402
from app.legal.manifest import load_manifest  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="re-download even if the stored hash matches")
    parser.add_argument("--only", default="", help="comma-separated document IDs")
    args = parser.parse_args()

    rows = load_manifest(settings.manifest_path)
    if args.only:
        wanted = {item.strip().upper() for item in args.only.split(",") if item.strip()}
        rows = [row for row in rows if row.document_id.upper() in wanted]
    summary = acquire(rows, settings.corpus_dir, settings.provenance_path, force=args.force)
    print(json.dumps({k: v for k, v in summary.items()}, indent=2))
    if summary["failed"]:
        print("Some downloads failed. Never substitute files from unofficial sources.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
