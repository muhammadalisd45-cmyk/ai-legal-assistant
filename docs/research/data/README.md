# Research data (generated)

Machine-readable exports of `../reports/Pakistan case law and statute sources.md`. **Do not edit these files by
hand**: fix the report, then regenerate:

```bash
cd backend
python scripts/export_research_data.py                 # parse + validate
python scripts/export_research_data.py --check-links   # + HTTP check of every URL (about 5 minutes)
```

| File | Report section | Rows are |
|---|---|---|
| `source_directory.csv` | Part B (B1–B5) | Every source: `section`, `Title`, `URL`, `Organisation`, `Category`, `Date / last updated`, `Credibility`, `Access status`; with `--check-links` also `http_status`, `final_url`, `check_error`, `checked_at` |
| `extracted_courts.csv`, `extracted_tribunals.csv`, `extracted_statute_portals.csv`, `extracted_third_party_datasets.csv`, `extracted_legal_provisions.csv` | Part C (C1–C5) | Raw extracted facts with their source, kept separate from analysis |
| `evidence.csv` | Part D | Finding → evidence → source URL(s) |
| `gap_federal_ict_punjab_sindh.csv` | E1 | Gap #1 fill (13 Nov 2026) |
| `gap_inaccessible_sources.csv`, `gap_open_questions.csv` | E2, E3 | What could not be accessed or answered |
| `actions.csv` | Part F | Prioritised actions |
| `research_repository.json` | all of the above | `{datasets: {name: {columns, rows}}}` |
| `validation_report.json` | — | Row counts, schema problems (empty fields, malformed or duplicate URLs) and link-check summary |
| `link_check.csv` | — | One row per URL occurrence (report + `frontend/data/sources/official_sources.csv`): HTTP status, final URL, error |

Link-check notes: each URL is requested once (HEAD, falling back to a 2 KB ranged GET), at most one request per
second per host. Hosts that ask automated agents to stay away (Supreme Court hosts, `digital.shc.gov.pk`,
`printing.balochistan.gov.pk`, BHC `/media/`) are **not fetched** and are marked as such. A non-200 status is a
fact about that moment, not proof a source is gone; government sites are often intermittently down.

The live, per-law data (every statute with its direct PDF link) is produced by the source-sync pipeline, not by
this export: see `frontend/data/sources/law_inventory.csv` and `backend/docs/SOURCE_SYNC_PIPELINE.md`.
