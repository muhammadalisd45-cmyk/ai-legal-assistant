# Third-party Hugging Face statute datasets: vetting for Pakistan Justice Navigator

Research date: 2026-11-12/13. Everything marked "fetched" was retrieved directly in this session, via the Hugging Face Hub API, raw README files, the datasets-server API (`/is-valid`, `/info`, `/splits`, `/size`, `/first-rows`, `/rows`, `/statistics`, `/filter`), HTTP byte-range requests (dataset #1 only), and official PDFs from pakistancode.gov.pk. No dataset was downloaded in full. Dataset #1 was read only through three ~6 KB byte ranges of its 46.9 MB file. "Snippet only" means the information came from a search-result snippet and was not fetched.

Abbreviations: D1 = `AyeshaJadoon/Pakistan_Laws_Dataset`; D2 = `endomorphosis/ipfs_pakistan_provincial_laws`; D3 = `abdullah693/adaption-pakistan-law-qa-pairs`.

---

## Q0. Source inventory and how far the user's descriptions match the repos

### Takeaway
All three repos exist and are public. Each differs from the user's description in at least one way that changes the decision. D1 has no usable metadata and the HF viewer can't read it. D2 covers only Khyber Pakhtunkhwa (KP) and Balochistan: 1,122 laws split into 21,857 section rows, not "10K–100K provincial texts". D3 is mostly about the PPC and the Constitution, not the CPC, and 31% of its rows are unrelated general chat data.

### Source inventory

| Title | URL | Organisation / owner | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| D1 Hub API metadata | https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset | HF user AyeshaJadoon | Third-party dataset (metadata) | created 2025-01-29; lastModified 2025-01-30 | Authoritative for repo facts | fetched |
| D1 README / dataset card | https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/raw/main/README.md | AyeshaJadoon | Dataset card | 2025-01-30 | Self-description, unverified | fetched |
| D1 datasets-server (`info`/`splits`/`size`/`is-valid`) | https://datasets-server.huggingface.co/info?dataset=AyeshaJadoon/Pakistan_Laws_Dataset | Hugging Face | Viewer API | 2026-11-12 | Authoritative | fetched. `info`/`splits`/`size` returned HTTP 500 `{"error":"No (supported) data files found in AyeshaJadoon/Pakistan_Laws_Dataset"}`. `is-valid` returned all false |
| D1 data file `pdf_data.json` (byte ranges 0–6000, 23,000,000–23,006,000, 46,918,000–end) | https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json | AyeshaJadoon | Raw data (partial) | 2025-01-30 | Primary for content | fetched (HTTP 206 partial content only) |
| AyeshaJadoon "BarristerBot" Space | https://huggingface.co/api/spaces/AyeshaJadoon/BarristerBot | AyeshaJadoon | Owner's related repo | lastModified 2025-01-30 | Context only | fetched (API, README, app.py) |
| Pakistan Code PDF named like a D1 `file_name` | https://pakistancode.gov.pk/pdffiles/administrator00532129aba2e10fe634ab8fbd94c50b.pdf | Ministry of Law and Justice | Official source | n/a | Official | fetched (first 1,001 bytes, HTTP 206 `application/pdf`; content not compared) |
| D2 Hub API metadata (851 files) | https://huggingface.co/api/datasets/endomorphosis/ipfs_pakistan_provincial_laws | HF user endomorphosis (profile full name "Benjamin J Barber"; 367 datasets) | Third-party dataset | created 2026-10-23; lastModified 2026-11-06 | Authoritative for repo facts | fetched |
| D2 README / dataset card | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md | endomorphosis | Dataset card | snapshot 2026-10-23 | Detailed self-description; internally consistent with manifests | fetched |
| D2 datasets-server info/size/splits/first-rows/statistics | https://datasets-server.huggingface.co/size?dataset=endomorphosis/ipfs_pakistan_provincial_laws | Hugging Face | Viewer API | 2026-11-12 | Authoritative | fetched |
| D2 manifests (`build_stats.json`, `fetch_stats_bal.json`, `fetch_stats_kp.json`, `post_checks.json`, `stopped_hosts_history.jsonl`) | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/manifests/build_stats.json (same folder for the others) | endomorphosis | Build provenance | 2026-10-17 to 10-23 | Primary (producer's own logs) | fetched (first 2.5 KB of each) |
| D2 `scrapers/PROVENANCE.md` | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/scrapers/PROVENANCE.md | endomorphosis | Provenance note | 2026-10-17/23 | Primary (producer) | fetched |
| endomorphosis federal sibling `ipfs_pakistan_laws` (README + first-rows + search) | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_laws/raw/main/README.md | endomorphosis | Adjacent third-party dataset (not one of the three) | snapshot 2026-10-16; lastModified 2026-11-06 | Self-description | fetched (README head, first-rows, one search) |
| D3 Hub API metadata | https://huggingface.co/api/datasets/abdullah693/adaption-pakistan-law-qa-pairs | HF user abdullah693 | Third-party dataset | created and modified 2026-06-20 | Authoritative for repo facts | fetched |
| D3 README / dataset card | https://huggingface.co/datasets/abdullah693/adaption-pakistan-law-qa-pairs/raw/main/README.md | abdullah693 / "Adaption" platform | Dataset card | 2026-06-20 | Marketing-style self-description | fetched |
| D3 datasets-server info/size/statistics/first-rows/rows/filter | https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train | Hugging Face | Viewer API | 2026-11-12/13 | Authoritative | fetched. `/rows` at offsets 0, 100, 1000, 3000, 5000, 7000 (600 rows). `/filter domain IS NULL` OK. `/filter domain='civil_procedure'` and `/search` returned HTTP 500 "Authentication check on the Hugging Face Hub failed or timed out" |
| D3 owner's model card `pakistan-legal-qa-llama70b` | https://huggingface.co/abdullah693/pakistan-legal-qa-llama70b/raw/main/README.md | abdullah693 | Owner's related repo (documents D3 construction) | 2026-06-20 | Self-description | fetched |
| LEGAL-UQA dataset card (D3 "seed") | https://huggingface.co/datasets/nlp-anonymous-researcher/LEGAL-UQA/raw/main/README.md | nlp-anonymous-researcher | Upstream dataset | created 2024-10-13 | Upstream self-description | fetched (YAML only; no licence field seen) |
| mariamffatima/Pakistan_Law_QA_Dataset (search hit) | https://huggingface.co/api/datasets/mariamffatima/Pakistan_Law_QA_Dataset | mariamffatima | Unrelated similar dataset | 2026-04-05 | n/a | fetched (no link to D3 found) |
| Pakistan Code: Constitution page + PDF | https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Fvbpw%3D-sg-jjjjjjjjjjjjj ; https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf | Ministry of Law and Justice | Official | footnotes include the 27th Amendment 2025 | Official (site disclaims authenticity; Gazette prevails) | fetched (1.18 MB PDF, converted to text) |
| Pakistan Code: CPC page + PDF | https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apeb-sg-jjjjjjjjjjjjj ; https://pakistancode.gov.pk/pdffiles/administrator6598dabbad120033d4d42d717dcf9755.pdf | Ministry of Law and Justice | Official | listed "(Under Review)"; includes Act VII of 2020 amendments | Official | fetched (2.28 MB PDF) |
| Pakistan Code: Copyright Ordinance 1962 PDF | https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf | Ministry of Law and Justice | Official | n/a | Official | fetched |
| Pakistan Code alphabetical list "C" | https://pakistancode.gov.pk/english/LGu0xAD.php?alp=C | Ministry of Law and Justice | Official index | n/a | Official | fetched |
| Web search "pakistancode.gov.pk Code of Civil Procedure 1908 pdffiles" | (WebSearch) | various | Search | 2026-11-13 | n/a | snippet only (not relied on) |

### Claims vs reality

| # | User's claim | What the repo actually shows | Verdict |
|---|---|---|---|
| D1 | "969 federal laws" | The card says "969 laws and acts". The HF viewer can't count rows, and I did not download the full file to count records. | **Unverified** (card claim only) |
| D1 | "scraped from Pakistan's Ministry of Law and Justice" | The card says "collected from the Ministry of Law and Justice website". `file_name` values have the form `administrator<32-hex>.pdf`, the same naming as pakistancode.gov.pk `/pdffiles/`. One such URL resolves to a PDF. | **Plausible / partly corroborated** |
| D1 | "clean" | Page headers ("Page 1 of 19"), split words ("r eceive", "privati sation") and, in one sampled region, letter-spaced extraction garbage ("t he   a c c us e d") | **False** |
| D1 | "46.9 MB JSON" | `pdf_data.json` is 46,924,676 bytes | **True** |
| D1 | "mapping document names to full text" | It is a JSON array of `{"file_name", "text"}` objects. `file_name` is a hashed PDF name, not a law title. The card's example uses a `content` key and readable names, but the actual key is `text`. | **Misleading** |
| D2 | "10,000–100,000" texts | 1,122 law instruments plus 21,857 section rows (22,979 rows across two configs). The card's YAML says `1K<n<10K`. HF's auto tag `10K<n<100K` counts the section rows. | **Misleading** |
| D2 | "official provincial legal texts" (implicitly all provinces) | Only KP (568 laws) and Balochistan (554). The card says Punjab, Sindh, ICT, GB and AJK are not covered. | **Partly false** |
| D2 | "in Parquet" | `data/laws.parquet` (7.57 MB) and `data/articles.parquet` (7.47 MB) | **True** |
| D3 | "111 MB" | `data/train_0.jsonl` is 111,434,327 bytes (one JSONL file, not Parquet) | **True** |
| D3 | "Q&A pairs on the Constitution and the CPC" | 11,195 rows. Of the 7,717 labelled legal rows: criminal (PPC) 3,349; constitutional 2,951; evidence (QSO) 1,117; civil_procedure (CPC) 208; family 92. The other 3,478 rows are non-legal general instruction data. | **Largely false** (CPC is under 2% of all rows) |
| D3 | "citing exact articles/orders/rules" | The base `citation`/`answer` fields matched official text in 9 of 9 spot checks. The LLM-"enhanced" fields contained wrong citations or hallucinations in 2 of the few checked. | **Partly true** (base fields only) |

### Gaps
- D1's 969 count is unverified. Counting would require the full 46.9 MB file, which this brief excluded.

---

## Q1. Repo existence, ownership, dates, files, row counts

### Takeaway
D1 is a single unstructured JSON blob that the HF viewer can't read, and its card metadata is wrong. D2 is a well-instrumented two-table Parquet release with 30 manifests. D3 is a 12-column JSONL with 11,195 rows and no licence.

### Cited findings
**D1: AyeshaJadoon/Pakistan_Laws_Dataset**
- Hub API: `"author":"AyeshaJadoon"`, `"createdAt":"2025-01-29T07:36:11.000Z"`, `"lastModified":"2025-01-30T12:36:59.000Z"`, `"tags":["license:odc-by","region:us"]`, downloads 74, likes 8 — [HF API](https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset)
- Files: `.gitattributes` (2,511 B), `README.md` (1,230 B), `pdf_data.json` (46,924,676 B, LFS sha256 `8556bdcc…2944`). There are no other files and no licence file — [HF API](https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset)
- Card YAML declares `configs … path: data/train-*` and `num_examples: 0`, `dataset_size: 0`, but no `data/` folder exists — [README](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/raw/main/README.md)
- datasets-server: `{"error":"No (supported) data files found in AyeshaJadoon/Pakistan_Laws_Dataset"}`; is-valid `{"preview":false,"viewer":false,"search":false,"filter":false,"statistics":false}` — [datasets-server info](https://datasets-server.huggingface.co/info?dataset=AyeshaJadoon/Pakistan_Laws_Dataset), [is-valid](https://datasets-server.huggingface.co/is-valid?dataset=AyeshaJadoon/Pakistan_Laws_Dataset)
- Card text: "This dataset contains a comprehensive collection of **969 laws and acts** relevant to Pakistan. The data was collected from the **Ministry of Law and Justice** website. The legal documents were originally in **PDF format** and have been converted into **JSON format**, where each entry includes: File Name … Content: The full text extracted from the PDF file." — [README](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/raw/main/README.md)
- The owner's only other public repo is the Gradio Space "BarristerBot" ("BarristerBot, an AI-based legal advisor", licence MIT, model `HuggingFaceH4/zephyr-7b-beta`). Its `app.py` is the stock Gradio chat template ("You are a friendly Chatbot.") and does not load D1 — [Space API](https://huggingface.co/api/spaces/AyeshaJadoon/BarristerBot), [app.py](https://huggingface.co/spaces/AyeshaJadoon/BarristerBot/raw/main/app.py)

**D2: endomorphosis/ipfs_pakistan_provincial_laws**
- Hub API: author `endomorphosis`, created 2026-10-23T21:12:05Z, lastModified 2026-11-06T16:25:17Z, tags include `license:other`, `size_categories:10K<n<100K`, `format:parquet`; downloads 251; 851 files (762 `.py`, 51 `.json`, 25 `.md`, 2 `.parquet`). Top-level folders: `scrapers_and_normalizers/` (720 files), `scrapers/` (96), `manifests/` (29), `data/` (2), plus `MANIFEST.md`, `SHA256SUMS.json` — [HF API](https://huggingface.co/api/datasets/endomorphosis/ipfs_pakistan_provincial_laws)
- Data files: `data/laws.parquet` 7,571,261 B; `data/articles.parquet` 7,470,187 B — [HF API](https://huggingface.co/api/datasets/endomorphosis/ipfs_pakistan_provincial_laws)
- datasets-server size: config `laws` 1,122 rows × 20 columns; config `articles` 21,857 rows × 10 columns; total 22,979 rows; viewer, search, filter and statistics all enabled — [size](https://datasets-server.huggingface.co/size?dataset=endomorphosis/ipfs_pakistan_provincial_laws), [is-valid](https://datasets-server.huggingface.co/is-valid?dataset=endomorphosis/ipfs_pakistan_provincial_laws)
- `laws` columns: id, title, text, source_url, source_type, jurisdiction, country, language, eli, date, date_issued, retrieved_at, license, law_status, identifier, official_identifier, article_count, json_path, metadata_json, province. `articles` columns: law_id, id, title, text, source_url, document_number, article_number, record_type, metadata_json, body_status — [info](https://datasets-server.huggingface.co/info?dataset=endomorphosis/ipfs_pakistan_provincial_laws)
- The owner's HF profile shows full name "Benjamin J Barber", 367 datasets and membership of orgs including "laion" (LAION eV). The account publishes a fleet of `ipfs_<country>_laws` datasets (UK, India, Bangladesh, Malta, EU, etc.) — [profile overview API](https://huggingface.co/api/users/endomorphosis/overview), [dataset list API](https://huggingface.co/api/datasets?author=endomorphosis&limit=1000)

**D3: abdullah693/adaption-pakistan-law-qa-pairs**
- Hub API: author `abdullah693`, created 2026-06-20T17:16:52Z, lastModified 2026-06-20T17:17:11Z, downloads 30, likes 0; `cardData.license: []`; files `.gitattributes`, `README.md` (2,143 B), `data/train_0.jsonl` (111,434,327 B) — [HF API](https://huggingface.co/api/datasets/abdullah693/adaption-pakistan-law-qa-pairs)
- datasets-server: 1 config / 1 split (`train`), 11,195 rows, 12 columns (prompt, answer, enhanced_prompt, enhanced_completion, reasoning_trace, citation[list], completion, domain, generation, id, language, reasoning); Parquet conversion 55,380,273 B — [info](https://datasets-server.huggingface.co/info?dataset=abdullah693/adaption-pakistan-law-qa-pairs), [size](https://datasets-server.huggingface.co/size?dataset=abdullah693/adaption-pakistan-law-qa-pairs)
- Card: "This dataset is a remastered version prepared using Adaption's Adaptive Data platform … question-answer pairs focused on Pakistani law, specifically covering the Code of Civil Procedure (CPC) and the Constitution of Pakistan … Each sample provides a direct legal inquiry followed by a precise answer citing relevant articles, orders, or rules." "There are 11,195 data points … This is an instruction tuning dataset." "The final quality is B, with a relative quality improvement of 35.0%." Domain: "Legal (76%) Governance (22%) History (2%)". Language: "English (100%)" — [README](https://huggingface.co/datasets/abdullah693/adaption-pakistan-law-qa-pairs/raw/main/README.md)
- The owner's other repos are four further `adaption-*` datasets (health worker / Urdu education) and models, including `pakistan-legal-qa-llama70b` (a LoRA trained on D3) — [datasets API](https://huggingface.co/api/datasets?author=abdullah693&limit=50), [models API](https://huggingface.co/api/models?author=abdullah693&limit=50)

### Inferences
- D1's card was apparently copied from a template. The example JSON uses a `content` key and readable names like `Constitution_of_Pakistan.pdf`, which don't match the real data. That suggests little curation.
- D2 is the only one of the three built with production-grade provenance and QA instrumentation.

### Gaps
- D1 record count, duplicate rate and the full list of `file_name` values (requires the full file).

---

## Q2. Provenance: source sites, scrape date, per-record traceability

### Takeaway
Only D2 keeps per-record official URLs: the PDF URL, detail page, PDF SHA-256 and retrieval timestamp. That makes each record checkable against the KP Code and Balochistan Code portals. D1 records keep only a hashed PDF filename, which can probably be rebuilt into a pakistancode.gov.pk URL. D3 gives statute-style citation strings but no source URLs.

### Cited findings
**D1**
- Sampled record 1: `"file_name": "administrator00532129aba2e10fe634ab8fbd94c50b.pdf"`, text begins "Page 1 of 19 … THE PRIVATISATION COMMISSION ORDINANCE, 2000 … Updated till 3.8.2022". No URL, title, year or jurisdiction fields are present — [pdf_data.json bytes 0–6000](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json)
- `https://pakistancode.gov.pk/pdffiles/administrator00532129aba2e10fe634ab8fbd94c50b.pdf` returned HTTP 206 `application/pdf`. I fetched only the first 1 KB, so I did not confirm it is the same Ordinance — [Pakistan Code PDF](https://pakistancode.gov.pk/pdffiles/administrator00532129aba2e10fe634ab8fbd94c50b.pdf)
- Pakistan Code's own PDFs use the same `pdffiles/administrator<hex>.pdf` scheme (Constitution: `administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf`; CPC: `administrator6598dabbad120033d4d42d717dcf9755.pdf`) — [Constitution page](https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Fvbpw%3D-sg-jjjjjjjjjjjjj), [CPC page](https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apeb-sg-jjjjjjjjjjjjj)
- The card states no scrape date. The repo was created 2025-01-29, and sampled text carries "Updated till 3.8.2022" — [HF API](https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset), [pdf_data.json](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json)

**D2**
- Snapshot table: "Snapshot date | 2026-10-23"; "Source | the official provincial law portals KP Code (Government of Khyber Pakhtunkhwa) and Balochistan Code (Government of Balochistan)"; "Collector | `scrapers/collect_pk.py` + `scrapers/build_pk.py`" — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- "Collected 2026-10-23 .. 2026-10-23 (America/Los_Angeles) directly from the two official provincial portals above; no mirrors, no archives." "Every request and every redirect hop was checked against that host's robots.txt … Crawl-delay honoured, otherwise >= 3 s between requests … No logins, no captcha/WAF handling." "Each law row carries the listing and detail page, the PDF URL and its SHA-256 (metadata_json.pdf_url / pdf_sha256), page count and OCR page numbers." "Wayback/archive fallbacks disabled." — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- `PROVENANCE.md`: "Sources: kpcode.kp.gov.pk and balochistancode.gob.pk only (official provincial government portals)… Balochistan's plain-http PDF links were fetched over https on the same host." Build revisions r2–r6 are dated 2026-10-17 and r7–r8 2026-10-23 — [PROVENANCE.md](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/scrapers/PROVENANCE.md)
- Sample record (pk-bal-1002): `source_url` `https://balochistancode.gob.pk/lawdir/799b925d-29d6-4dda-95a3-3a43fc0e0e79.pdf`; metadata_json includes `"detail_page": "https://balochistancode.gob.pk/Document.aspx?wise=opendoc&docid=1002&docc=952"`, `"index_page": "https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1"`, `"listing_meta": "Government | Act II of 2017 of 2017 | Promulgation Date: Thu Jun 08, 2017 | Views: 2754 | Status: Published"`, `"pdf_sha256": "0e6862a7…e135"`, `"pdf_bytes": 84513`, `"pages": 19`, `"ocr_pages": 0` — [first-rows laws](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- All 1,122 rows have `source_type` = `official_provincial_law_pdf`. `retrieved_at` ranges from 2026-10-23 20:59:57 to 21:00:13 (a narrow window, so this is probably the build/freeze timestamp rather than per-page fetch time) — [statistics laws](https://datasets-server.huggingface.co/statistics?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- Article rows also carry `source_url` (the same official PDF URL as the parent law) — [first-rows articles](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=articles&split=train)
- Fetch stats: Balochistan listed 611, staged 609, failed 0, non_pdf 2, pages 8,742, pages_need_ocr 881, requests 1,223. KP listed 575, staged 569, failed 3, no_pdf 3, pages 6,975, pages_need_ocr 46, requests 1,186 — [fetch_stats_bal.json](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/manifests/fetch_stats_bal.json), [fetch_stats_kp.json](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/manifests/fetch_stats_kp.json)
- One stop event: "HTTP 200 challenge" on balochistancode.gob.pk (2026-10-17), cleared as a "false positive … Cloudflare's passive JS-detection snippet" — [stopped_hosts_history.jsonl](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/manifests/stopped_hosts_history.jsonl)

**D3**
- Rows carry a `citation` list in an internal shorthand (e.g. `["QSO art.90", "QSO art.90(1)"]`, `["CONST art.116"]`, `["CPC o.8 r.1"]`) and no URL, edition or version date — [first-rows](https://datasets-server.huggingface.co/first-rows?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)
- The owner's model card describes the source corpora: "Constitution of Pakistan 1973 — full text, 305 provisions (LEGAL-UQA seed, MIT licence); Pakistan Penal Code — 498 provisions (CC-BY); Qanun-e-Shahadat Order 1984 — 165 provisions (CC-BY); Muslim Family Laws Ordinance 1961 — 59 provisions (CC-BY); Code of Civil Procedure — 143 provisions (CC-BY)". It also says "All answers are grounded in verbatim provision text extracted from official Pakistani statutes." No upstream URLs are given for the "CC-BY" corpora — [model card](https://huggingface.co/abdullah693/pakistan-legal-qa-llama70b/raw/main/README.md)
- The LEGAL-UQA HF card (fetched) contains only YAML `dataset_info` (495 train + 124 validation; question/context/answer in English and Urdu) and no licence field in what was fetched — [LEGAL-UQA README](https://huggingface.co/datasets/nlp-anonymous-researcher/LEGAL-UQA/raw/main/README.md)

### Inferences
- D1 could probably be made traceable by prefixing each `file_name` with `https://pakistancode.gov.pk/pdffiles/`. But Pakistan Code re-uploads consolidated PDFs when it updates them, so hashes from a ≤2025 snapshot may no longer match current versions. Each one would need re-checking, at which point scraping Pakistan Code directly is simpler.
- D2's per-row `pdf_url` + `pdf_sha256` let the team re-fetch each official PDF and confirm byte-identity. This meets a "trace to official URL" policy, as long as the product cites the official URL rather than the HF row.
- The "CC-BY" licence the D3 owner claims for PPC/QSO/CPC/MFLO text is unexplained. No such open licence exists on Pakistan Code, so the upstream corpora are unidentified.

### Gaps
- Whether all 969 D1 file names still resolve on Pakistan Code (not tested beyond one).
- The identity and URLs of the "CC-BY" statute corpora behind D3.
- The LEGAL-UQA licence: the model card asserts "MIT", but the fetched HF card shows no licence. The associated paper/GitHub was not fetched.

---

## Q3. Content quality from sampled rows

### Takeaway
D1 is raw PDF-text dumps with page furniture and, in at least one long document, unusable letter-spaced text. D2 has a full-text column plus section-split rows, with OCR noise in 144 documents, some title/date mismatches and documented section-split heuristics. D3's base Q/A fields are concise and accurate on spot checks. Its LLM-"enhanced" fields contain hallucinations, and a third of the dataset is off-topic.

### Cited findings
**D1 (three byte-range samples)**
- Head sample (truncated): `"text": " \nPage 1 of 19  \n \n \n \nTHE PRIVATISATION COMMISSION ORDINANCE, 2000 … 17. Power to obtain finance and r eceive grants. … Updated till 3.8.2022 \nPage 2 of 19  20. Accounts. … 41. Regulation s. … ORDINANCE  No. LII OF 2000 … [28th September, 2000]`. Section numbers and the ordinance number/date are preserved, with page headers and broken words — [pdf_data.json bytes 0–6000](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json)
- Mid-file sample (Code of Criminal Procedure ss.468–471 text, "Page 164 of 319"): `"470.  Ju d gm e n t  of   ac q u i ttal   on   gr ou n d   of   l u n ac y .  W he ne ve r  a ny  pe rs on  i s   a c qui t t e d  upon  t he   g round…"`. This is letter-spaced extraction garbage that keyword search and embeddings would handle poorly — [pdf_data.json bytes 23,000,000–23,006,000](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json)
- Tail sample: the last record is an ordinance repealing "The Sindh Shops and Establishments Act, 1940 … The Punjab Trade Employees Act, 1940 …" (West Pakistan Shops and Establishments Ordinance, 1969 text). It ends with a long run of `\n \n` padding, and the file closes with `]` (well-formed end) — [pdf_data.json tail](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json)

**D2**
- Law text sample (pk-bal-1000): `"THE BALOCHISTAN ORPHANAGES\n(SUPERVISION AND CONTROL)\nORDINANCE, 1978\n(Baln Ordinance V of 1978)\nCONTENTS\nSECTIONS\n\nPreamble.\n1. Short title, extent and commencement.\n2. Definitions.…"`. But the row's `title` is "The Balochistan Orphanges ( Supervision and Control) Ordinance, 1987", its `date` is 1987-02-18 and its `identifier` is "Ordinance V of 1978 of 1987", so the portal metadata conflicts with the document text — [first-rows laws](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- Another mismatch: pk-bal-1042 "West Pakistan Animals Slaughter Control Act, 1963" has `date` 1960-04-17. pk-bal-1045's title is just "Baln Ordinance X of 1984" — [first-rows laws](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- Section row sample (pk-bal-1000-s1): `"1. Short title, extent and.- (1) This Ordinance may be called the Balochistan\nOrphanages (Supervision and Control) Ordinance. 1978.\ncommencemen\n(2) It extends to the whole of Balochistan except the\nt.\nTribal Areas."`. The marginal heading is interleaved and split ("commencemen … t."). Section 2's row contains a page-footnote ("…promulgated by the Governor of Baloch1stan on 18 th February, 1978…"), showing OCR digit/letter confusion — [first-rows articles](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=articles&split=train)
- Card disclosures: "OCR: 816 pages in 144 documents (tesseract `eng`, 250 dpi …); mean ocr_confidence 87.9 (min 0.0)". "Duplicates dropped: 43 identical texts, 2 same title/year with >= 90% similar text". "Texts are the documents as posted (often consolidated with amendment footnotes; some are original enactments). No point-in-time versioning; repeal status is not verified (law_status = published)." "Gaps in section numbering: 340 breaks in 176 laws". "Section splitting is heuristic … The full text is always in laws.text." "11 listed laws whose PDFs are Urdu scans … are left out." — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- `body_status` counts: text 21,673; repealed_placeholder 184 — [post_checks.json](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/resolve/main/manifests/post_checks.json)
- Column statistics: `date` minimum 1812-07-18 and maximum 2026-09-08 (median 2000-08-30); `eli` 100% null; `law_status` = "published" for all 1,122; `article_count` 0–191 (median 13); law `text` length 1,019–315,037 characters — [statistics laws](https://datasets-server.huggingface.co/statistics?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- The card says it includes "pk-bal-2142 (Finance Act 2026)" and "pk-kp-1610 (Finance Act 2025)" — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)

**D3**
- Row 0 (id `evidence-00619`, generation `synthetic_grounded`): answer "Generally yes. Under Article 90(1) of the Qanun-e-Shahadat, the Court shall presume such a government-certified document genuine…". But `reasoning_trace` reasons from US law: "Under rules of evidence—like Federal Rule of Evidence 902 in the US, though I'll keep the terminology general since the prompt doesn't specify a jurisdiction…" — [first-rows](https://datasets-server.huggingface.co/first-rows?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)
- Row 2: `prompt` in English, but `enhanced_prompt` and `enhanced_completion` in Urdu. The completion adds that the 62-year retirement age "is the same in India's constitutional framework" (translated) — [first-rows](https://datasets-server.huggingface.co/first-rows?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)
- Row 7 (CONST art.39): base answer "Article 39 directs that the State shall enable people from all parts of Pakistan to participate in the Armed Forces of Pakistan." The Urdu `enhanced_completion` instead analyses "Article 39 of the Uniform Code of Military Justice (UCMJ)" and says the provision contains no directive on geographic participation — [rows offset 0](https://datasets-server.huggingface.co/rows?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train&offset=0&length=100)
- `language` column = "en" for all 7,717 labelled rows, yet many prompts/answers are in Urdu (e.g. rows 3, 8, 10, 11, 19, 164) — [statistics](https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train), [first-rows](https://datasets-server.huggingface.co/first-rows?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)
- 3,478 rows (31.07%) have null `domain`/`generation`/`citation`/`id`. `/filter domain IS NULL` returns them starting at row 7717, and they are general-purpose chat items: "Where should I go on vacation?" (answer citing Time magazine destinations), "What is SCSS?", "How do you cook ribs?", Python list deduplication, "Should I immigrate to Canada?" — [filter](https://datasets-server.huggingface.co/filter?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train&where=%22domain%22%20IS%20NULL&length=5), [statistics](https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)
- Field-length statistics: `enhanced_completion` mean 2,788 chars vs `answer` mean 400 chars; `reasoning_trace` max 78,882 chars — [statistics](https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)

### Inferences
- 7,717 legal rows plus 3,478 null rows equals 11,195, and the first null row is at index 7717. So rows 0–7716 are the legal set and rows 7717–11194 are an appended general-instruction set. Usable legal rows are therefore 7,717, not 11,195.
- The "Time magazine" vacation answer and the other generic prompts look like items from a public general instruction dataset (they resemble databricks-dolly-15k). That is unconfirmed, but if true it would bring in that dataset's own licence (Dolly is CC BY-SA 3.0).
- D2's date/title conflicts (e.g. 1978 vs 1987) come from portal listing metadata. Any year or date the product shows should be taken from the document text or the official page, not D2's `date` column.

### Gaps
- No full-corpus duplicate or amendment-vs-principal-act analysis for D1 (needs the full file).
- I did not check what the D2 row with date 1812-07-18 is.
- No measured share of OCR-noisy text in D1.

---

## Q4. D2 specifics: size category, provinces, and what "ipfs" means

### Takeaway
"10K<n<100K" is HF's automatic size tag over both configs combined (22,979 rows, 95% of them section rows). The real unit count is 1,122 laws from two provinces. "ipfs" is the name of the publisher's tooling project (`ipfs_datasets_py`). The rows I sampled contain no IPFS CIDs. Traceability comes from official HTTPS URLs plus SHA-256 hashes.

### Cited findings
- Card YAML `size_categories: - "1K<n<10K"`, while Hub API tags show `size_categories:10K<n<100K` — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md), [HF API](https://huggingface.co/api/datasets/endomorphosis/ipfs_pakistan_provincial_laws)
- Coverage table: "Khyber Pakhtunkhwa | KP Code, https://kpcode.kp.gov.pk/homepage/list_all_law (English list) | 575 | 568 | 11,829" and "Balochistan | Balochistan Code, https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical (ACTS, ORDINANCE, REGULATIONS) | 611 | 554 | 10,028". By type: "Balochistan provincial_act: 357, … provincial_ordinance: 164, … provincial_regulation: 33, Khyber Pakhtunkhwa provincial_act: 407, … provincial_ordinance: 126, … provincial_regulation: 35" — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- "Punjab, Sindh, Islamabad Capital Territory, Gilgit-Baltistan and Azad Jammu and Kashmir: not covered. Federal law: not covered." "Khyber Pakhtunkhwa: only the English list … rules, notifications and other subordinate legislation are not collected." "Balochistan: … Out of scope on the same site: RULES (631), GAZETTE NOTIFICATION (496), POLICIES (40)." — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- Statistics confirm `province`: Khyber Pakhtunkhwa 568, Balochistan 554; `jurisdiction`: PK-KP 568, PK-BA 554 — [statistics laws](https://datasets-server.huggingface.co/statistics?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- "Upstream helpers pinned to ipfs_datasets_py@a1b5c73e5b687d8bd6c3b3051788860fd6e2f07a" and "scrapers/: collector code, pinned upstream helpers (ipfs_datasets_py@a1b5c73e)" — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- Sampled `metadata_json` has `content_sha256`, `pdf_sha256`, `pdf_url`, `detail_page`, `index_page`, with no CID/IPFS field. `json_path` is a local relative path (`instruments/pk-bal-1000.json`) — [first-rows laws](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- Sibling federal dataset `endomorphosis/ipfs_pakistan_laws`: "Pakistan Federal Acts and Constitution (Pakistan Code)", snapshot 2026-10-16, 970 instruments / 41,986 articles, licence `other` / `pk-pakistan-code-official-texts`. Rows carry `source_url` on pakistancode.gov.pk (e.g. Contract Act, 1872 → `https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-a50%3D-sg-jjjjjjjjjjjjj`). Updates of 2026-10-10 and 2026-10-16 added instruments "from the official-source local corpus (`scrapers/cc_country_harvest.py (Common Crawl ranged WARC)`)" — [ipfs_pakistan_laws README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_laws/raw/main/README.md), [first-rows](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_laws&config=laws&split=train)

### Inferences
- "ipfs" here does not mean the texts are served from IPFS or addressed by CID in a way that matters for provenance. The provenance chain is official HTTPS URL → PDF SHA-256 → extracted text, which is traceable.
- Punjab and Sindh, which most PJN users would likely need, are absent. D2 can't serve as a "provincial laws" source in general, only for KP and Balochistan Acts, Ordinances and Regulations.
- The federal sibling (`ipfs_pakistan_laws`, 970 instruments) partly overlaps D1's "969 federal laws" and has per-row Pakistan Code URLs. As a federal cross-check it is probably better than D1. Some of its records came from Common Crawl WARCs rather than live fetches, so those would need re-verification.

### Gaps
- I didn't check whether the upstream `ipfs_datasets_py` pipeline adds IPFS CIDs elsewhere (e.g. in `MANIFEST.md` or `SHA256SUMS.json`). The GitHub repo was not fetched.

---

## Q5. D3 specifics: human vs synthetic, generator model, citation accuracy

### Takeaway
D3 is LLM-generated. 6,806 rows are `synthetic_grounded` and 911 are `seed_legaluqa` (derived from LEGAL-UQA). The model card says reasoning traces were "generated and verified by Claude", and the `enhanced_*` fields come from the commercial "Adaption" platform (model not stated). The base `answer` + `citation` fields matched official Pakistan Code text in 9 of 9 spot checks. The `enhanced_completion` field failed 2 of the checks I made, with fabricated sub-clause numbers and wrong jurisdiction.

### Cited findings
- `generation` values: synthetic_grounded 6,806; seed_legaluqa 911; null 3,478. `domain`: criminal 3,349; constitutional 2,951; evidence 1,117; civil_procedure 208; family 92 — [statistics](https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)
- Model card: "Each QA pair includes a verbatim provision excerpt as grounding context plus a chain-of-thought reasoning trace generated and verified by Claude." "Trained via | Adaption AutoScientist / Together AI". It describes "a curated dataset of 5,116 question–answer pairs" (PPC 2,215; Constitution 1,957; QSO 742; CPC 143; MFLO 59) and says "Urdu-language queries are not yet well-supported (English-only training data)." — [model card](https://huggingface.co/abdullah693/pakistan-legal-qa-llama70b/raw/main/README.md)
- Dataset card: "remastered version prepared using Adaption's Adaptive Data platform"; "relative quality improvement of 35.0%" — [README](https://huggingface.co/datasets/abdullah693/adaption-pakistan-law-qa-pairs/raw/main/README.md)

**Spot checks against official Pakistan Code PDFs (fetched)**

| Row (id) | D3 claim (base `answer`) | Official text (Pakistan Code) | Result |
|---|---|---|---|
| 2 (const-seed-00405) CONST art.195 | HC judge serves "until the age of sixty-two years" | "195. Retiring age. A Judge of a High Court shall hold office until he attains the age of sixty-two years…" — [Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf) | Correct |
| 12 CONST art.179 | SC judge retires at sixty-five | "179. Retiring age.__A Judge of the Supreme Court shall hold office until he attains the age of sixty-five years…" (footnotes cite the 26th Amendment 2024 and 27th Amendment 2025) — [Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf) | Correct |
| 1 (const-seed-00381) CONST art.116 | Governor cannot return a Money Bill | "116 … (2) … the Governor shall, within 2[ten] days,__ (a) assent to the Bill; or (b) in the case of a Bill other than a Money Bill, return the Bill…" — [Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf) | Base answer correct. **`enhanced_completion` wrong**: it says "Article 116(1) … within thirty days" and quotes a proviso "the Governor shall not return a Money Bill", which is not in the official text (it is clause (2)(b), and the period is ten days) |
| 9 CONST art.51 | "three hundred and thirty-six seats … including seats reserved for women and non-Muslims" | "51 … (1) There shall be 3[three hundred and thirty-six] seats for members in the National Assembly, including seats reserved for women and non-Muslims." Totals row shows 266 general / 60 women — [Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf) | Correct (verbatim) |
| 3 CONST art.41 (Urdu) | Validity of presidential election cannot be challenged in any court | "(6) The validity of the election of the President shall not be called in question by or before any court or other authority." — [Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf) | Correct (citation could be more precise: 41(6)) |
| 7 CONST art.39 | State shall enable people from all parts of Pakistan to participate in Armed Forces | "39. Participation of people in Armed Forces. The State shall enable people from all parts of Pakistan to participate in the Armed Forces of Pakistan." — [Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf) | Base correct. **`enhanced_completion` wrong** (treats it as US UCMJ Art. 39) |
| 27 (civil_procedure-00098) CPC s.151 | Inherent power exercised "after recording reasons" for ends of justice / prevent abuse | "151. Saving of inherent powers of Court. Nothing in this Code shall … affect the inherent power of the Court 1[to be exercised after recording reasons] to make such orders as may be necessary for the ends of justice or to prevent abuse of the process of the Court." (1 Ins. by Act No. VII of 2020, s.18) — [CPC PDF](https://pakistancode.gov.pk/pdffiles/administrator6598dabbad120033d4d42d717dcf9755.pdf) | Correct, and current (reflects the 2020 amendment) |
| 47 (civil_procedure-00055) CPC O.8 r.1 | Written statement at/before first hearing; "ordinarily not more than thirty days" | "1. Written statement. The defendant may, and, if so required by the Court, shall, at or before the first hearing … Provided that the period allowed for filing the written statement shall not ordinarily exceed 3[thirty] days." — [CPC PDF](https://pakistancode.gov.pk/pdffiles/administrator6598dabbad120033d4d42d717dcf9755.pdf) | Correct |
| 55 (civil_procedure-00009) CPC O.2 r.2 | Omitted portion of claim cannot be sued for later | "2. Suit to include the whole claim.__ (1) Every suit shall include the whole of the claim … (2) … he shall not afterwards sue in respect of the portion so omitted or relinquished." — [CPC PDF](https://pakistancode.gov.pk/pdffiles/administrator6598dabbad120033d4d42d717dcf9755.pdf) | Correct (illustration not checked) |

### Inferences
- The base fields (`prompt`/`answer`/`reasoning`/`citation`/`completion`) look like the carefully grounded "Claude-generated and verified" set. The `enhanced_prompt`/`enhanced_completion`/`reasoning_trace` fields are a second, less reliable LLM rewrite by the Adaption platform. In two of the three enhanced completions I read closely, it imported US or Indian law or invented clause text.
- The dataset has 7,717 legal rows, but the model card says 5,116 pairs were used. The released dataset doesn't explain which subset that was. Splits or provenance of eval items (e.g. the "hard slice" of 110 test questions) are not identifiable from the release.
- The spot checks are positive for the base fields, but the sample is small (9 items, Constitution + CPC). No PPC, QSO or MFLO items were checked against official text.

### Gaps
- The generator model behind the `enhanced_*` fields is not disclosed.
- I couldn't run the `/filter domain='civil_procedure'` and `/search` calls (HTTP 500, HF authentication timeout). CPC rows were sampled via `/rows` instead (18 CPC rows in 600 sampled).
- No spot checks on QSO, PPC or MFLO citations.

---

## Q6. Licence and terms compatibility

### Takeaway
D1's ODC-BY tag allows commercial use with attribution, but only for the database layer. D2 states no licence and passes through the governments' "All rights reserved" footers. D3 has no licence at all, mixes in data of unknown provenance, and is therefore not cleared for commercial use. For the statute text itself, the Copyright Ordinance 1962 has a specific exception for reproducing Gazette-published matter (s.57(1)(q)(i)), separate from the judgments exception (q)(ii). Consolidated portal versions add editorial content that the exception may not clearly cover.

### Cited findings
- D1: `"tags":["license:odc-by",…]`, card YAML `license: odc-by`. There is no licence text or LICENSE file in the repo — [HF API](https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset), [README](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/raw/main/README.md)
- D2: `license: "other"`, `license_name: "public-law-no-licence-stated"`, `source_terms_note: "No open licence is stated by either source. Official statute text published by the provincial governments is redistributed as public law for research (same basis as the fleet's other provincial sets)…"`. KP Code footer: "© 2026 Law & Parliamentary Affairs Department, Government of KP"; Balochistan Code footer: "© Copyright, All rights reserved by Law & parliamentary affairs department Balochistan". "This dataset is **not** an official consolidation and is **not legal advice**." — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)
- D2 per-row `license` column repeats the source notice for every row (568 KP rows: "no licence stated; site states it is for informational purposes and subject to its disclaimer"; 554 Balochistan rows: "'© Copyright, All rights reserved …'") — [statistics laws](https://datasets-server.huggingface.co/statistics?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- D3: `license: []` (none) — [README](https://huggingface.co/datasets/abdullah693/adaption-pakistan-law-qa-pairs/raw/main/README.md). The owner's model card claims upstream "LEGAL-UQA seed, MIT licence" and statute corpora under "CC-BY", and licenses the LoRA weights "CC-BY-4.0 … Subject to Meta's Llama 3.3 Community Licence" — [model card](https://huggingface.co/abdullah693/pakistan-legal-qa-llama70b/raw/main/README.md)
- Pakistan Code footer and disclaimer: "© Copyright 2022 - Ministry of Law and Justice. Disclaimer: All laws on the website are currently under review. They are for general informational purposes only, and should not be taken as authentic or error-free legislative instruments. If you have any questions about the accuracy or completeness of a law, please refer to the original source i.e. the relevant Gazette notification(s)." — [Pakistan Code Constitution page](https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Fvbpw%3D-sg-jjjjjjjjjjjjj)
- Copyright Ordinance 1962, s.57(1): "The following acts shall not constitute an infringement of copyright, namely: … (q) the reproduction or publication of__ (i) any matter which has been published in any official Gazette, or the report of any committee, commission, council, board or other like body appointed by the Government unless the reproduction or publication of such matter or report is prohibited by the Government; (ii) any judgment or order of a court, tribunal or other judicial authority, unless the reproduction or publication of such judgment or order is prohibited by the court…" — [Copyright Ordinance PDF (Pakistan Code)](https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf)
- Same Ordinance, s.2: "'Government work' means a work which is made or published by or under the direction or control of__ (i) the Government or any department of the Government; or (ii) any court, tribunal or other judicial or legislative authority in Pakistan" — [Copyright Ordinance PDF](https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf)

### Inferences (not legal advice)
- The user's brief cites only s.57(1)(q)(ii) (judgments). The fetched text shows a separate (q)(i) exception covering "any matter which has been published in any official Gazette" unless prohibited. Acts and Ordinances are published in the Gazette, so reproducing statute text appears to fall within (q)(i). Portal consolidations (amendment footnotes, "Updated till…", editorial layout) are not themselves Gazette publications and are Government works. Counsel should confirm whether reproducing consolidated portal text, as opposed to gazetted text, is covered. The "All rights reserved" footers (Balochistan, Pakistan Code) don't override a statutory exception, but they do signal the publisher's position.
- ODC-BY (D1) can only license whatever rights the compiler holds, i.e. the arrangement and selection. It can't grant rights in the underlying Government works. In practice the D1 licence adds little beyond the s.57 position.
- D3 has no licence, a third-party commercial platform involved (Adaption), unverified "MIT"/"CC-BY" upstream claims, and appended general chat data whose source licence is unknown (possibly CC BY-SA). Commercial redistribution or training use is not cleared. Internal evaluation use is lower-risk but still needs the owner's permission or counsel's view.

### Gaps
- ODC-BY licence text was not fetched.
- KP Code disclaimer page text was not fetched (only as quoted in the D2 card).
- LEGAL-UQA's actual licence (paper/GitHub) was not fetched.
- The source of D3's 3,478 general-chat rows is unconfirmed.

---

## Q7. Practical recommendation per dataset

### Takeaway
Don't cite any of the three directly. D2 is a useful coverage cross-check and fetch index for KP and Balochistan, because every row links to an official PDF URL with a hash. D1 is redundant: scrape Pakistan Code directly, or use the endomorphosis federal sibling as the cross-check. D3 can serve as a seed for internal eval after heavy filtering and verification, and is not suitable as evidence or training data under its current licensing.

### Cited findings (basis)
- D2: per-row `source_url` + `pdf_sha256` + `detail_page`; snapshot 2026-10-23; KP + Balochistan only; "repeal status is not verified"; OCR in 144 documents — [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md), [first-rows laws](https://datasets-server.huggingface.co/first-rows?dataset=endomorphosis/ipfs_pakistan_provincial_laws&config=laws&split=train)
- D1: no URL/title/year fields; viewer broken; noisy text; text "Updated till 3.8.2022" — [pdf_data.json](https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset/resolve/main/pdf_data.json), [datasets-server](https://datasets-server.huggingface.co/info?dataset=AyeshaJadoon/Pakistan_Laws_Dataset)
- D3: 3,478 off-topic rows; enhanced-field hallucinations; base fields accurate in 9/9 checks; no licence — [filter](https://datasets-server.huggingface.co/filter?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train&where=%22domain%22%20IS%20NULL&length=5), [README](https://huggingface.co/datasets/abdullah693/adaption-pakistan-law-qa-pairs/raw/main/README.md)

### Inferences: recommendations

| Dataset | Citable evidence? | Coverage cross-check / gap-finder? | Eval / test data? | Recommended use |
|---|---|---|---|---|
| D1 AyeshaJadoon | **No.** No per-record URL, title or date. Text is a ≤2025 snapshot with extraction noise. | **Weak.** Hashed file names could be mapped to `pakistancode.gov.pk/pdffiles/…` to list which PDFs existed when it was scraped, but the record count and currency are unverified. | No | **Do not adopt.** If a federal cross-check is wanted, `endomorphosis/ipfs_pakistan_laws` (970 instruments, per-row Pakistan Code URLs, snapshot 2026-10-16) is a better candidate and needs its own vetting. |
| D2 endomorphosis provincial | **Not directly.** It is acceptable as a pointer only: re-fetch the `source_url` PDF, check `pdf_sha256`, then cite the official KP Code / Balochistan Code URL. | **Yes (KP + Balochistan only).** Use the listing/coverage counts (575 / 611 listed) to find gaps in PJN's own provincial ingest. Use `pdf_sha256` to detect when an official PDF has changed. | Partly. Section rows could seed retrieval tests for KP/Balochistan, after filtering `body_status == 'text'` and excluding OCR-flagged laws. | **Adopt as a gap-finder and fetch index.** Take dates and years from the document text, not the `date` column, and verify repeal status independently. It offers nothing for Punjab, Sindh, ICT, GB or AJK. |
| D3 abdullah693 QA | **No.** Synthetic Q&A, not a legal source. | No | **Conditionally.** Keep rows 0–7716 only. Use only `prompt`/`answer`/`citation`, ignoring `enhanced_*` and `reasoning_trace`. Re-verify each item against Pakistan Code before use. Domain mix is criminal- and constitution-heavy, with only 208 CPC items. Licence clearance is needed before any use beyond internal testing. | **Optional internal eval seed** (e.g. citation-accuracy tests). Do not train or fine-tune on it, and do not redistribute it. |

### Gaps
- No full-corpus comparison of D2 against PJN's own provincial ingest (outside scope).
- Vetting of `endomorphosis/ipfs_pakistan_laws` (federal) was only cursory. If it is considered, it needs its own vetting, including how many records came from Common Crawl rather than live fetches.
