# Corpus folders

- `constitution/` — official Constitution source files
- `federal_laws/` — federal Acts / Codes from Pakistan Code
- `sindh_laws/` — Sindh legislation from Sindh Code
- `punjab_laws/` — Punjab legislation from Punjab Code
- `kp_laws/` — Khyber Pakhtunkhwa legislation from KP Code
- `balochistan_laws/` — Balochistan legislation from Balochistan Code
- `supreme_court/` — reserved for official Supreme Court judgments
- `high_courts/` — official High Court judgments grouped by court
- `metadata/legal_documents.csv` — source register used by ingestion

The repository intentionally does not ship fabricated PDFs. Run `python backend/scripts/acquire_corpus.py` to download every verified direct official PDF (SHA-256 recorded in `provenance.json`), then `python backend/scripts/build_index.py`.
