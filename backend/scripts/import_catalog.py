"""Import the team law catalogs into the corpus manifest, with direct official PDF links.

The catalogs (frontend/data/catalog/*.json) name laws but carry no text or direct PDF link. This script
finds each law on the official code website of its jurisdiction (Pakistan Code, Punjab Code, KP Code,
Balochistan Code, Sindh Code), then writes the manifest and the files derived from it:

  frontend/data/member4_manifest.csv / .json   (source of truth for the backend and frontend)
  frontend/data/legal_documents.csv / .json     (source-library directory)
  frontend/supabase/seed.sql                    (legal_documents registry)
  frontend/data/catalog/import_report.json      (what matched, what did not, catalog corrections)

Existing `metadata_only` rows are upgraded in place when their official PDF is found.
Next steps after this script:  python scripts/acquire_corpus.py  &&  python scripts/build_index.py

Usage:  python scripts/import_catalog.py [--dry-run] [--cache DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.catalog import (  # noqa: E402
    ID_PREFIX, PORTAL_HOME, SOURCE_NAME, Target, authority, document_type, load_catalogs, match, priority, slug,
    year_of,
)
from app.legal.manifest_io import DATA_DIR, read_manifest, write_manifest, write_text, next_id  # noqa: E402
from app.legal.official_codes import SITE_FOR_JURISDICTION, Fetcher, crawl, pdf_url  # noqa: E402

CATALOG_DIR = DATA_DIR / "catalog"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="report matches without writing any file")
    parser.add_argument("--cache", default="", help="cache fetched listing pages in this folder (development)")
    args = parser.parse_args()

    fields, rows = read_manifest(settings.manifest_path)
    catalogs = sorted(CATALOG_DIR.glob("*.json"))
    catalogs = [p for p in catalogs if p.name != "import_report.json"]
    targets, portals, skipped = load_catalogs(catalogs)

    # Existing rows: verified ones absorb catalog duplicates; metadata-only ones become targets too.
    by_key: dict[tuple, dict] = {}
    for row in rows:
        if row["jurisdiction"] in ID_PREFIX and row["status"] != "placeholder" and not row["court"]:
            probe = Target(row["jurisdiction"], row["title"], row["title"], year_of(row["title"]))
            by_key[probe.key] = row
    already: list[dict] = []
    work: list[Target] = []
    for target in targets:
        row = by_key.get(target.key)
        if row and row["status"] != "metadata_only":
            already.append({"document_id": row["document_id"], "title": row["title"],
                            "catalog_titles": target.catalog_titles})
            continue
        if row:
            target.existing_id = row["document_id"]
        work.append(target)
    covered = {t.existing_id for t in work if t.existing_id}
    for key, row in by_key.items():
        if row["status"] == "metadata_only" and row["document_id"] not in covered:
            work.append(Target(row["jurisdiction"], row["title"], row["title"], key[2], existing_id=row["document_id"]))

    fetcher = Fetcher(cache_dir=Path(args.cache) if args.cache else None)
    needed_sites = sorted({SITE_FOR_JURISDICTION[t.jurisdiction] for t in work})
    listings = crawl(needed_sites, fetcher)
    by_site = defaultdict(list)
    for item in listings:
        by_site[item.site].append(item)

    resolved, unresolved = [], []
    for target in work:
        candidates = match(target, by_site[SITE_FOR_JURISDICTION[target.jurisdiction]])
        url, chosen = "", None
        for candidate in candidates:
            url = pdf_url(fetcher, candidate)
            if url:
                chosen = candidate
                break
        record = {"jurisdiction": target.jurisdiction, "title": target.display_title, "year": target.year,
                  "catalog_titles": target.catalog_titles, "existing_id": target.existing_id or None,
                  "correction": target.note or None}
        if chosen:
            resolved.append((target, chosen, url, record | {"official_title": chosen.title,
                                                              "detail_url": chosen.detail_url, "pdf_url": url}))
        else:
            unresolved.append((target, record | {"reason": "no listing with the same name and year on "
                                                           + SOURCE_NAME[target.jurisdiction]
                                                 if not candidates else "listing found but no PDF link"}))
    fetcher.close()

    # Apply to manifest rows.
    by_id = {row["document_id"]: row for row in rows}
    used_files = {row["file_name"] for row in rows if row["file_name"]}
    for target, chosen, url, record in resolved:
        file_name = slug(target.display_title) + ".pdf"
        if file_name in used_files and not (target.existing_id and by_id[target.existing_id]["file_name"] == file_name):
            file_name = f"{ID_PREFIX[target.jurisdiction].lower()}_{file_name}"
        used_files.add(file_name)
        if target.existing_id:
            row = by_id[target.existing_id]
        else:
            row = {key: "" for key in fields}
            row.update({"document_id": next_id(rows, target.jurisdiction), "title": target.display_title,
                        "document_type": document_type(target.jurisdiction, target.display_title),
                        "jurisdiction": target.jurisdiction,
                        "authority": authority(target.jurisdiction, target.display_title),
                        "language": "English", "priority": priority(target.category), "source_tier": "1"})
            rows.append(row)
        row.update({"source_name": SOURCE_NAME[target.jurisdiction], "source_url": url, "file_name": file_name,
                    "status": "source_url_verified"})
        if row["title"].startswith("Qanun-e-Shahadat"):
            row["document_type"] = "Federal Order"  # provisions are Articles, not Sections
        record["document_id"] = row["document_id"]
    for target, record in unresolved:
        if target.existing_id:
            record["document_id"] = target.existing_id
            continue
        row = {key: "" for key in fields}
        row.update({"document_id": next_id(rows, target.jurisdiction), "title": target.display_title,
                    "document_type": document_type(target.jurisdiction, target.display_title),
                    "jurisdiction": target.jurisdiction, "authority": authority(target.jurisdiction, target.display_title),
                    "language": "English", "source_name": SOURCE_NAME[target.jurisdiction],
                    "source_url": PORTAL_HOME[target.jurisdiction], "status": "metadata_only",
                    "priority": priority(target.category), "source_tier": "1"})
        rows.append(row)
        record["document_id"] = row["document_id"]


    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalogs": [p.name for p in catalogs],
        "summary": {"resolved_to_official_pdf": len(resolved), "unresolved_metadata_only": len(unresolved),
                    "already_in_corpus": len(already), "portals_not_documents": len(portals),
                    "skipped": len(skipped), "manifest_rows": len(rows)},
        "resolved": [r for *_, r in resolved],
        "unresolved": [r for _, r in unresolved],
        "already_in_corpus": already,
        "portals_not_documents": portals,
        "skipped": skipped,
    }
    print(json.dumps(report["summary"], indent=2))
    for _, record in unresolved:
        print(f"UNRESOLVED {record['jurisdiction']}: {record['title']} — {record['reason']}")
    if args.dry_run:
        for *_, record in resolved:
            print(f"OK {record['jurisdiction']:<18} {record['title']}  <=  {record['official_title']}")
        return 0

    write_manifest(fields, rows)
    write_text(CATALOG_DIR / "import_report.json", json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} manifest rows. Next: python scripts/acquire_corpus.py && python scripts/build_index.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
