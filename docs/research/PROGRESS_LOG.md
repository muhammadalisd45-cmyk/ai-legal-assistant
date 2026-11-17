# Research and data pipeline — progress log

Dates are when the work was done (Pakistan time). Each entry says what was done, how, and what came out.

## 2026-11-12 — Corpus expansion from team catalogs
- Imported the two team catalogs (`frontend/data/catalog/`). They held titles and portal links only (no text,
  no direct PDFs), so each law was matched by name + year on its official code site and its direct PDF found
  (`backend/scripts/import_catalog.py`). 43 laws resolved; 56 official PDFs validated and indexed (9,768 chunks).
- Catalog errors corrected and logged in `frontend/data/catalog/import_report.json`.

## 2026-11-12/13 — Deep research: case-law and statute sources
- **Approach:** six parallel research tracks (federal courts; LHC + SHC; other courts and tribunals;
  copyright and open data; federal/ICT/Punjab/Sindh statutes; KP/Balochistan/GB/AJK statutes), each fetching
  official sites directly, recording robots.txt and terms verbatim, testing sample PDFs, and keeping raw facts
  separate from analysis. A second round vetted the five third-party datasets named by the user.
- **Output:** `reports/Pakistan case law and statute sources.md` (Parts A–F) and notes in
  `research_notes/Pakistan case law and statute sources/`.
- **Gap:** the federal/ICT/Punjab/Sindh statute track was stopped early by an API safety filter.

## 2026-11-13 — Gap #1 filled (federal, ICT, Punjab, Sindh statutes)
- **Approach:** direct fetches of each official host: robots.txt, sitemap, disclaimer, every listing type
  (alphabetical, chronological, category, latest/recently updated, Urdu, rules), assembly Acts pages; searched
  official Sindh hosts for the two statutes missing from Sindh Code.
- **Findings:** listings carry Act number, promulgation date and (Punjab) "Last Updated On", enough to detect
  new and amended laws automatically; no separate ICT portal (46 ICT laws inside Pakistan Code); Pakistan Code
  disclaimer says texts are not authentic, Gazette prevails; Punjab robots.txt returns 403; **Sindh Civil Courts
  Ordinance 1962 found** (consolidated to Sindh Act VI of 2025) at the Sindh Judicial Academy; Sindh Land
  Revenue Act 1967 still not found (Board of Revenue Sindh unreachable).
- **Output:** `research_notes/.../statutes_federal_ict_punjab_sindh.md`; report Part E1 rewritten.

## 2026-11-13 — CSV/JSON exports rebuilt and debugged
- **Approach:** `backend/scripts/export_research_data.py` parses every report table (Parts B–F) into CSV and one
  JSON repository, validates rows, and link-checks every URL (report + source registry).
- **Bugs found and fixed by validation:**
  - three tables used `Date` / `Owner` instead of `Date / last updated` / `Organisation`, so values were dropped
    → columns normalised;
  - a URL containing parentheses was truncated → URL parsing fixed;
  - **the report listed the Sindh Code as `https://sindhcode.gos.pk/`, a URL that does not appear in any research
    note** (the official host is `sindhlaws.gov.pk`) → corrected, together with the Punjab Code row that still
    said "not fetched".
- **Link check (13 Nov 2026):** 194 URL occurrences — 168 OK, 13 deliberately not fetched (robots/AI-crawl
  restrictions), 13 failed (IHC POST-only services, FTO certificate mismatch, gba.gov.pk expired certificate,
  blncode.pitb.gov.pk timeout, Dawn 403, Hugging Face viewer 500, ihc.gov.pk dropped connection).
- **Output:** `docs/research/data/` (see its README).

## 2026-11-13 — Source-sync pipeline (automatic updates from official sources)
- **Approach:** a registry of official sources with their real listing URLs
  (`frontend/data/sources/official_sources.csv`) drives `backend/scripts/sync_sources.py`, which crawls each
  enabled source, keeps `law_inventory.csv/.json` (every law with its direct PDF link), logs changes, and with
  `--ingest` adds new principal laws / refreshes changed PDFs, validates them and re-indexes incrementally.
  Scheduled weekly via `.github/workflows/legal-sources-sync.yml` (PR for review) or
  `backend/scripts/run_source_sync.ps1` (Windows Task Scheduler). Full description:
  `backend/docs/SOURCE_SYNC_PIPELINE.md`.
- **Baseline run (22 min):** 5,572 laws inventoried from 6 official sources, 5,569 with a direct PDF link
  (3 KP laws have none on their pages). Spot check: 12/12 sampled links returned real PDFs.
- **Type classification debugged on the real inventory:** parenthetical notes such as "(Repealed by Ord. 52 …)"
  and "(Regulation)" were deciding the instrument type; ~38 principal Acts/Ordinances were wrongly typed
  "Regulations" (and would have been excluded from auto-ingest). Fixed and covered by tests.

## 2026-11-13 — Incident: Punjab Code key instability (found by the stability re-run)
- **What happened:** the immediate re-run that should have reported ~0 changes reported 746 `new` + 746
  `removed` for Punjab Code. Punjab Code gives every law a different article URL on each visit, and the URL
  was used as the law's key. With `--ingest` the run began adding Punjab laws (rows PB-005…PB-701).
- **Response:** process stopped during download (index was never rebuilt); manifest restored to its 63 rows,
  690 wrongly downloaded PDFs and their provenance removed, false change-log entries removed, run annotated in
  `sync_state.json`. Verified afterwards: 63 manifest rows, 56 validated PDFs, index 9,768 chunks / 56 documents.
- **Fixes:** Punjab keys = title + Act No. + promulgation date; anomaly guard blocks ingest on implausible change
  volume (would have blocked this: 746 > limit 37); per-run add cap (25); link-only manifest rows upgraded in
  place (this is why the Sindh Civil Courts backfill had silently done nothing). Regression tests added.
- **Verification after the fix:** Punjab re-baselined with stable keys; an immediate all-source re-run reported
  **0 changes on every source** except Balochistan Code, which had genuinely published new items (recorded,
  not ingested: one Rules, one implementation notice). The same run upgraded SD-001 Sindh Civil Courts
  Ordinance 1962 from link-only to a validated 19-page official PDF (Sindh Judicial Academy, tier 2); the
  index rebuild reused 9,768 embeddings and computed 29 (index now 9,797 chunks / 57 documents).
- **Genuine detection in the same run:** Balochistan Code had published one new item since the morning:
  "Implementation of Constitution Under Articles 189 & 190 to Resolve Service and Litigation, 2026".
