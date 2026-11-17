"""Sync the law inventory with the official code websites and (optionally) ingest what changed.

    python scripts/sync_sources.py                      # crawl enabled sources, update inventory + change log
    python scripts/sync_sources.py --ingest             # ...then add new laws / refresh changed PDFs, download,
                                                        #    validate, quarantine failures, and re-index
    python scripts/sync_sources.py --sources punjab_code,sindh_code
    python scripts/sync_sources.py --resolve all        # re-check every law's direct PDF link (slow: ~1 h)
    python scripts/sync_sources.py --ingest --backfill punjab_code --backfill-limit 25
                                                        # also add up to 25 existing principal Punjab laws

Sources, listing URLs and policies live in frontend/data/sources/official_sources.csv. The first crawl of a
source is a baseline (its back catalogue is recorded, not reported as "new"). Exit code 2 = a source failed.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.acquisition import acquire, load_provenance  # noqa: E402
from app.legal.auto_ingest import apply_plan, eligibility, plan_ingest, quarantine  # noqa: E402
from app.legal.manifest import load_manifest  # noqa: E402
from app.legal.manifest_io import read_manifest, write_manifest, write_text  # noqa: E402
from app.legal.source_sync import SOURCES_DIR, load_inventory, load_registry, run_sync, save_inventory  # noqa: E402

SUMMARY_PATH = SOURCES_DIR / "last_run_summary.md"


def rebuild_index(log=print) -> dict:
    from app.legal.embeddings import FastEmbedEmbedder
    from app.legal.index import build_chunk_rows, previous_vectors, write_index

    rows = load_manifest(settings.manifest_path)
    chunk_rows = build_chunk_rows(rows, settings.corpus_dir, settings.provenance_path, log=lambda *_: None)
    embedder = FastEmbedEmbedder()
    reuse = previous_vectors(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path, embedder.name)
    meta = write_index(chunk_rows, settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path,
                       embedder, log=log, reuse=reuse)
    return {"chunks": meta["chunk_count"], "documents": len(meta["documents"]),
            "embeddings_reused": meta.get("embeddings_reused", 0)}


def summary_markdown(report, plan, added, updated, quarantined, index_info) -> str:
    lines = [f"# Legal source sync — {report.run_date}", "", "| Source | Listed | New PDFs resolved | Changes | Note |",
             "|---|---|---|---|---|"]
    for source_id, stats in report.sources.items():
        if "error" in stats:
            lines.append(f"| {source_id} | — | — | — | FAILED: {stats['error'][:80]} |")
            continue
        note = "baseline" if stats["baseline"] else ("partial crawl" if stats["partial"] else "")
        if stats.get("anomaly"):
            note = f"ANOMALY - auto-ingest blocked: {stats['anomaly']}"
        lines.append(f"| {source_id} | {stats['listed']} | {stats['pdf_resolved']} | {stats['changes']} | {note} |")
    by_kind: dict[str, list] = {}
    for change in report.changes:
        by_kind.setdefault(change["change"], []).append(change)
    lines += ["", "## Changes", ""]
    if not report.changes:
        lines.append("No changes since the last run.")
    for kind, items in sorted(by_kind.items()):
        lines.append(f"**{kind}** ({len(items)})")
        lines += [f"- {c['jurisdiction']}: {c['title']}" + (f" — {c['pdf_url']}" if c.get("pdf_url") else "")
                  for c in items[:40]]
        if len(items) > 40:
            lines.append(f"- … {len(items) - 40} more (see changes/{report.run_date}.json)")
        lines.append("")
    if plan is not None:
        lines += ["## Corpus updates", "", f"- Added: {', '.join(added) or 'none'}",
                  f"- Re-downloaded (official PDF changed): {', '.join(updated) or 'none'}",
                  f"- Deferred by the per-run cap: {sum(1 for _, _, r in plan.skipped if r.startswith('deferred'))}",
                  f"- Blocked by source anomaly: {sum(1 for _, _, r in plan.skipped if r.startswith('source anomaly'))}",
                  f"- Quarantined (failed validation): "
                  + (", ".join(f"{d} ({r})" for d, r in quarantined) or "none"),
                  f"- Amendments linked to principal laws: "
                  + (", ".join(f"{t} → {d}" for t, d in plan.linked_amendments[:20]) or "none")]
    if index_info:
        lines += ["", f"Index: {index_info['chunks']} chunks from {index_info['documents']} documents "
                      f"({index_info['embeddings_reused']} embeddings reused)."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sources", default="", help="comma-separated source_ids (default: all enabled, open ones)")
    parser.add_argument("--resolve", choices=["auto", "all", "none"], default="auto",
                        help="auto: new/changed/tracked laws and missing links; all: every law; none: skip")
    parser.add_argument("--ingest", action="store_true", help="apply changes to the corpus and re-index")
    parser.add_argument("--include-amendments", action="store_true", help="also ingest amendment Acts")
    parser.add_argument("--backfill", default="", help="source_id whose existing principal laws to add")
    parser.add_argument("--backfill-limit", type=int, default=25)
    parser.add_argument("--backfill-match", default="", help="only backfill titles containing this text")
    parser.add_argument("--no-index", action="store_true", help="with --ingest: download but skip re-indexing")
    parser.add_argument("--max-add", type=int, default=25, help="cap on laws added per run (rest deferred)")
    parser.add_argument("--delay", type=float, default=0.5, help="seconds between requests to the same site")
    parser.add_argument("--cache", default="", help="development only: cache fetched pages in this folder")
    args = parser.parse_args()

    registry = load_registry()
    by_id = {s.source_id: s for s in registry}
    wanted = [s.strip() for s in args.sources.split(",") if s.strip()]
    unknown = [s for s in wanted if s not in by_id]
    if unknown:
        parser.error(f"unknown source_id(s): {', '.join(unknown)}")
    sources = [by_id[s] for s in wanted] if wanted else [s for s in registry if s.syncable]
    not_syncable = [s.source_id for s in sources if not s.syncable]
    if not_syncable:
        parser.error(f"not syncable (disabled, no adapter, or collection_status != open): {', '.join(not_syncable)}")

    started = time.time()
    fields, manifest_rows = read_manifest()
    report = run_sync(sources, resolve=args.resolve, cache_dir=Path(args.cache) if args.cache else None,
                      delay=args.delay, manifest_rows=manifest_rows)
    print(json.dumps({"run_date": report.run_date, "sources": report.sources, "changes": len(report.changes)},
                     indent=2, default=str))

    plan = None
    added: list[str] = []
    updated: list[str] = []
    quarantined: list[tuple[str, str]] = []
    index_info: dict = {}
    if args.ingest or args.backfill:
        inventory = load_inventory()
        backfill_keys: list[str] = []
        if args.backfill:
            if args.backfill not in by_id:
                parser.error(f"unknown backfill source: {args.backfill}")
            match = args.backfill_match.lower()
            for key, row in sorted(inventory.items(), key=lambda kv: kv[1]["title"]):
                if row["source_id"] == args.backfill and not row.get("manifest_id") and not eligibility(row) \
                        and (not match or match in row["title"].lower()):
                    backfill_keys.append(key)
            backfill_keys = backfill_keys[:args.backfill_limit]
        plan = plan_ingest(report.changes, inventory, by_id, manifest_rows, args.include_amendments, backfill_keys,
                           source_stats=report.sources, max_add=args.max_add)
        added, updated = apply_plan(plan, fields, manifest_rows, by_id)
        if added or updated:
            write_manifest(fields, manifest_rows)
            save_inventory(inventory)  # manifest_id links for newly added laws
            targets = [r for r in load_manifest(settings.manifest_path) if r.document_id in set(added + updated)]
            acquire([r for r in targets if r.document_id in added], settings.corpus_dir, settings.provenance_path)
            acquire([r for r in targets if r.document_id in updated], settings.corpus_dir, settings.provenance_path,
                    force=True)
            provenance = load_provenance(settings.provenance_path).get("documents", {})
            quarantined = quarantine(manifest_rows, provenance, added + updated)
            if quarantined:
                write_manifest(fields, manifest_rows)
            if not args.no_index:
                index_info = rebuild_index()
        print(json.dumps({"added": added, "updated": updated, "quarantined": quarantined,
                          "linked_amendments": plan.linked_amendments[:20], "index": index_info}, indent=2))

    write_text(SUMMARY_PATH, summary_markdown(report, plan, added, updated, quarantined, index_info))
    print(f"Summary: {SUMMARY_PATH}  ({round(time.time() - started)} s)")
    return 2 if any("error" in stats for stats in report.sources.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
