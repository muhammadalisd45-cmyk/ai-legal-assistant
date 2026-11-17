# Pakistan Legal Corpus — Source Register

Primary-source policy: only official government and court systems belong in the Tier-1 corpus.

## Statutes — official code websites

Direct PDF links are resolved from the team catalogs in `frontend/data/catalog/` by
`backend/scripts/import_catalog.py`, which matches each law by name and year on the official code website of its
jurisdiction. `frontend/data/catalog/import_report.json` lists every match, every catalog correction and what is still missing.

| Jurisdiction | Official source | Verified direct PDFs |
|---|---|---|
| Federal (`PK-*`) | Pakistan Code — https://pakistancode.gov.pk/english/ | 38 |
| Punjab (`PB-*`) | Punjab Code — https://punjabcode.punjab.gov.pk/ | 4 |
| Sindh (`SD-*`) | Sindh Code — https://www.sindhlaws.gov.pk/SindhIndex.aspx | 9 |
| Khyber Pakhtunkhwa (`KP-*`) | KP Code — https://kpcode.kp.gov.pk/ | 3 |
| Balochistan (`BL-*`) | Balochistan Code — https://balochistancode.gob.pk/ | 2 |

Still metadata-only (the principal Act is not published on the Sindh Code; only amendments are):
`SD-001` Sindh Civil Courts Ordinance, 1962 and `SD-011` Sindh Land Revenue Act, 1967.

Assembly websites and court search pages listed in the catalogs (Punjab/Sindh/KP/Balochistan Assemblies, Supreme Court
and Islamabad High Court judgment search) are portals, not documents; they are recorded in the import report only.

## Sindh High Court case law
- Official case-law search: https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search
- The five `SHC-*` rows supplied in the starter dataset are placeholders and are quarantined from evidence retrieval until replaced with real case records and official judgment/order files.

## Integrity rules
- Preserve title, source URL, authority, date/citation where available and file name.
- Do not substitute unofficial mirrors when an official download fails.
- `source_url_verified` means the official file endpoint is known; it does **not** mean text has been ingested.
- `metadata_only` can identify a candidate source but cannot justify an exact section/article claim.
- `ingested` is assigned only after source text has actually been chunked and pushed to the corpus store.
- Exact legal text shown to users must come from an ingested source chunk whose provenance points back to the official document.
