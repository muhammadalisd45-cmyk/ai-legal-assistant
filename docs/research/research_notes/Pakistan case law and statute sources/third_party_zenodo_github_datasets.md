# Third-party Pakistani legal datasets: the Zenodo "Pakistani Law Dataset" and the GitHub repo SyedAhtsham/Pakistani-Law-Cases-Search-Engine

Research date: 12 November 2026. Every fact below comes from a live fetch made on that date unless it is marked otherwise. "API" means the Zenodo REST API (`https://zenodo.org/api/records/...`) or the GitHub REST API (`https://api.github.com/repos/...`), called with curl.

**What was downloaded (no bulk downloads):**
- **Zenodo:** one file in full, `Datatset For FAISS.csv` (1,500,268 bytes; its md5 matched the record). Every other file was sampled with HTTP range requests (the first ~1.4 KB and the last ~0.7 KB). The parquet file was not opened.
- **GitHub:** three small judgment PDFs (c.a_110.pdf, crl_10.pdf, s.m_1.pdf, about 1.28 MB together), the 0.96 MB `CaSearch Report.pdf`, and several small text and code files. The 1,000-PDF corpus (about 145 MB) was not downloaded.

---

## Q0. Source inventory and access status

### Takeaway
Both datasets exist and were reached directly through their APIs. The Zenodo record matches the user's description well. The GitHub repo is real, but it is a 2021 student coursework project, not a maintained dataset.

### Cited Findings: source inventory

| Title | URL | Organisation / owner | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| Pakistani Law Dataset: Structured Legal Acts of Pakistan (Criminal, Family, and Property Law) | https://zenodo.org/records/20509007 (API: https://zenodo.org/api/records/20509007) | Umair Ahmed (ORCID 0009-0009-3291-0686), no affiliation in record; hosted by Zenodo/CERN | Third-party dataset (academic, unreviewed) | Published 2026-06-02; created/updated 2026-06-02 | Low–medium: self-deposited, no peer review, quality defects found | Fetched (API JSON + HTML 200; one CSV in full, others range-sampled) |
| PakLegalAid: Lawyer-Written Legal Question-Answer Dataset for Pakistani Law | https://zenodo.org/records/20509273 | Umair Ahmed (same ORCID) | Third-party dataset (companion) | 2026-06-02 | Low–medium | Fetched (API JSON) |
| Annotated Pakistan Supreme Court Civil Appeal Judgments Dataset for Legal Named Entity Recognition | https://zenodo.org/records/21671415 | Adnan Ul-Hasan (NCAI Islamabad), Faisal Shafait (NUST) | Third-party dataset (alternative candidate) | pub. date 2022-12-30; deposited 2026-07-29; v1.0 | Medium (named academic affiliations) | Fetched (API JSON metadata only; zip not downloaded) |
| Smart Legal Assistance Chatbot for the Pakistan Penal Code | https://zenodo.org/records/18780573 | Not checked | Publication (not a dataset) | 2026-02-26 | Unknown | Title/date only from API search list |
| GitHub repo SyedAhtsham/Pakistani-Law-Cases-Search-Engine | https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine (API: https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine) | GitHub user SyedAhtsham (Syed Ahtsham) | Student coursework code + scraped court PDFs | Created 2022-12-10; last push 2023-05-08 | Low as a dataset; the PDFs inside appear to be genuine court-issued copies | Fetched (repo, /contents, /commits, /git/trees?recursive=1, /readme, /languages, /forks; /license returned 404 "Not Found") |
| CaSearch Report.pdf (in repo) | https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf | Muhammad Faizan & Syed Ahtsham (students) | Project report | Submission date stated 17 Dec 2021 | Primary source for provenance | Fetched (downloaded; text extracted) |
| ORCID public record 0009-0009-3291-0686 | https://pub.orcid.org/v3.0/0009-0009-3291-0686/works | ORCID | Author record | n/a | High (for what it lists) | Fetched (API) |
| PLOS search API | https://api.plos.org/search | PLOS | Paper lookup | n/a | High | Fetched: 0 results |
| Crossref works API | https://api.crossref.org/works | Crossref | Paper lookup | n/a | High | Fetched: no matching title |
| Hugging Face dataset search ("pakistan law") | https://huggingface.co/api/datasets?search=pakistan%20law | Hugging Face | Discovery | n/a | n/a | Fetched (list only) |
| Legal Sahara FYP (IBA Karachi) | https://ir.iba.edu.pk/fyp-bscs/60 | IBA Karachi | Unrelated FYP that appeared in search | 2026 | n/a | Fetched (WebFetch summary); not related to either dataset |

---

## Q1. Zenodo: which record is it, and what are its exact metadata?

### Takeaway
The best match is **Zenodo record 20509007**, "Pakistani Law Dataset: Structured Legal Acts of Pakistan (Criminal, Family, and Property Law)":
- DOI 10.5281/zenodo.20509007
- A single creator, Umair Ahmed
- Published 2 June 2026, licensed CC-BY-4.0, with 11 files totalling about 5.4 MB

The paper it cites has not been published or indexed anywhere that could be checked.

### Cited Findings
- **Candidates found by Zenodo API search.**
  - The query `title:(pakistan* AND law*) AND resource_type.type:dataset` returned 5 datasets. Two are relevant:
    - 20509007, "Pakistani Law Dataset: Structured Legal Acts of Pakistan (Criminal, Family, and Property Law)"
    - 20509273, "PakLegalAid: Lawyer-Written Legal Question-Answer Dataset for Pakistani Law"
  - The other three (17510363, 21852603, 22100868) are law-review style "datasets" on shipping agents, environmental law and legal pluralism. They are not statute corpora.
  - The query `pakistan legal dataset csv` also surfaced 21671415, an annotated Supreme Court NER dataset.
  - Sources: [Zenodo API search](https://zenodo.org/api/records?q=title:(pakistan*%20AND%20law*)%20AND%20resource_type.type:dataset); [Zenodo API search 2](https://zenodo.org/api/records?q=pakistan%20legal%20dataset%20csv)
- **Record metadata for 20509007.**
  - Title: "Pakistani Law Dataset: Structured Legal Acts of Pakistan (Criminal, Family, and Property Law)"
  - DOI: 10.5281/zenodo.20509007; concept DOI: 10.5281/zenodo.20509006
  - Created 2026-06-02T11:38:43Z; publication_date 2026-06-02; no version string; a single version (is_last = true)
  - Licence cc-by-4.0; access_right open; language eng
  - Keywords: 'pakstan' [sic], 'Legal', 'law', 'criminal-law', 'family-law', 'property-law', 'legal-nlp', 'llm', 'RAG', 'LLM'
  - No related_identifiers and no references
  - Source: [Zenodo API record](https://zenodo.org/api/records/20509007)
- **Creator.** "Ahmed, Umair", ORCID 0009-0009-3291-0686. The affiliation field is empty. — [Zenodo API record](https://zenodo.org/api/records/20509007)
- **Usage stats at fetch time.** 562 downloads (529 unique) and 356 views (319 unique). — [Zenodo API record](https://zenodo.org/api/records/20509007)
- **Description, quoted from the record.**
  - "This dataset contains structured and machine-readable data extracted from 8 major Pakistani legal documents, parsed from official PDF versions. It covers Family Law, Criminal Law, Civil Procedure, Property Law, and Evidence Law. Designed for use in legal AI, RAG pipelines, and LLM fine-tuning."
  - "Built as part of the paper: 'Enhancing Legal Assistance with Large Language Models: A Parameter-Efficient Fine-Tuning and Retrieval-Augmented Generation Approach' — Ahmed et al., submitted to PLOS ONE, 2025."
  - "All files follow schema: Book | Chapter Number | Chapter Title | Section | Heading | Definition"
  - "For research purposes only. Not a substitute for professional legal advice."
  - Source: [Zenodo record](https://zenodo.org/records/20509007)
- **Files listed by the API (key, bytes):**
  - Muslim_Family_Laws_Ordinance_1961.csv (10,259)
  - Legal_QA_dataset_From_lawyers.csv (43,753)
  - Transfer property.csv (153,689)
  - 2-limitation-act-1908-pdf_extracted.csv (34,009)
  - Code_of_Criminal_Procedure_Structured upto 16 chapter.csv (695,947)
  - combined_legal_dataset.csv (1,535,827)
  - train-00000-of-00001.parquet (662,881)
  - Datatset For FAISS.csv (1,500,268)
  - Pakistan_Penal_Code.csv (423,504)
  - Police_law.csv (183,689)
  - qanun-e-shahadat_1984.csv (149,119)
  - Total ≈ 5.39 MB. — [Zenodo API record](https://zenodo.org/api/records/20509007)
- **Companion record 20509273 (PakLegalAid).**
  - Same creator and date, CC-BY-4.0.
  - Contains a single file, Legal_QA_dataset_From_lawyers.csv. Its md5 is identical to the file in 20509007 (2c7c5d5f5686b152fd7f283e8cdcea9e).
  - Description: "practicing lawyers wrote the responses directly"; "used for: 1. Fine-tuning generative LLMs (LLaMA 3.x, Phi-3.5 Mini) 2. RAG pipeline retrieval via FAISS vector store 3. Evaluation of generated legal responses."
  - Source: [Zenodo API record 20509273](https://zenodo.org/api/records/20509273)
- **Associated paper: not found.**
  - The PLOS search API returned `numFound: 0` for `title:"Enhancing Legal Assistance" OR everything:"PakLegalAid"`. — [PLOS API](https://api.plos.org/search)
  - Crossref returned no matching title. — [Crossref API](https://api.crossref.org/works)
  - The author's public ORCID lists only two 2026 iCoMET conference papers, "Enhancing Whisper for Low Resource Sindhi Language" and "DeepFractNet…", and no legal-LLM paper. — [ORCID works](https://pub.orcid.org/v3.0/0009-0009-3291-0686/works)
  - A web search found only the Zenodo record itself. — [WebSearch result: Zenodo record](https://zenodo.org/records/20509007)
- **Authors and institution, from the data itself.** The FAISS CSV contains 21 "Chatbot Info" rows. They state: "This legal chatbot was created by Umair Ahmed, Ritika Rani, and Gungun Sadhwani, undergraduate students of the Computer Science department at Sukkur IBA University." — [Datatset For FAISS.csv](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content)

### Inferences
- The project is an undergraduate project at Sukkur IBA University. The "PLOS ONE, 2025" paper was "submitted" and, as of November 2026, has no findable publication. Treat it as unpublished.
- The file `train-00000-of-00001.parquet` uses Hugging Face's default export naming. This suggests a Hugging Face mirror existed or exists. It was not located: the HF search for "pakistan law" did not show an Umair Ahmed dataset ([HF API](https://huggingface.co/api/datasets?search=pakistan%20law)).

### Gaps
- The PLOS ONE submission status and any preprint could not be found.
- No affiliation is recorded on Zenodo or ORCID. The Sukkur IBA affiliation comes only from text inside the data.

---

## Q2. Zenodo: which statutes, what schema, where the text came from, and how good it is

### Takeaway
The record covers **7 statutes, not 8**:
- Pakistan Penal Code
- Code of Criminal Procedure, 1898
- Qanun-e-Shahadat Order, 1984
- Muslim Family Laws Ordinance, 1961
- Transfer of Property Act, 1882
- Police Order, 2002
- Limitation Act, 1908

The record never says where the text came from or which edition it is. The description claims "Civil Procedure", but no Civil Procedure Code (CPC) file exists. The data has serious structural defects: corrupted labels, missing lettered sections such as PPC 295-C and 489-F, a missing Limitation Schedule, inline footnote noise, and no sign of amendments after 2006. It cannot serve as citable statute text.

### Cited Findings
- **Header used by the statute files** (the column is misspelt "Defination"): `Book,Chapter Number,Chapter Title,Section,Heading,Defination`. — [Pakistan_Penal_Code.csv (range sample)](https://zenodo.org/api/records/20509007/files/Pakistan_Penal_Code.csv/content)
- **combined_legal_dataset.csv uses a different schema**, `Query,Response`. Its rows are generated prompts, for example "Section 1 of Chapter I in Code of Criminal Procedure, 1898 (Short Title and Commencement): What does it say?". The file ends with lawyer Q&A rows. This contradicts the description's claim that "all files follow schema". — [combined_legal_dataset.csv (range sample)](https://zenodo.org/api/records/20509007/files/combined_legal_dataset.csv/content)
- **Legal_QA_dataset_From_lawyers.csv** has header `Query,Response,,`. A sample answer: "Having been separated for a period of more than 3 years, the court will certainly dissolve your marriage." Another answer cites "the Inheritance Act, 1925". — [Legal_QA_dataset_From_lawyers.csv (range sample)](https://zenodo.org/api/records/20509007/files/Legal_QA_dataset_From_lawyers.csv/content)
- **CrPC file format problems.** The CrPC CSV has hundreds of trailing empty columns in its header and rows. Its filename says "upto 16 chapter", but its tail contains Schedule V forms ("Warrant of Imprisonment…"). — [CrPC CSV (range sample)](https://zenodo.org/api/records/20509007/files/Code_of_Criminal_Procedure_Structured%2520upto%252016%2520chapter.csv/content)
- **Row counts by Book in `Datatset For FAISS.csv`** (1,417 rows in total):

  | Book | Rows |
  |---|---|
  | Pakistan Penal Code | 502 |
  | "Code of Criminal Procedure, 1898" | 306 |
  | Police Law | 187 |
  | Qanun-e-Shahadat Order, 1984 | 165 |
  | Transfer of Property Act | 124 |
  | Limitation Act, 1908 | 28 |
  | Chatbot Info | 21 |
  | Muslim Family Laws Ordinance, 1961 | 11 |
  | CrPC rows mislabelled "Code of Criminal Procedure, 1899" through "…, 1939" | about 70 |

  Source: [Datatset For FAISS.csv](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content) (local analysis of the downloaded file).
- **Label corruption.**
  - CrPC Book labels increment year by year, "Code of Criminal Procedure, 1899", "…, 1900" … "…, 1939". This is a spreadsheet fill-down artefact.
  - MFLO "Chapter Title" increments "Muslim Family Laws Ordinance 1961" … "…1971" across sections 1–11.
  - Police Law section numbers appear as floats ("1.0", "2.0"), and the numbering restarts in forms.
  - Source: [Datatset For FAISS.csv](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content); [MFLO CSV sample](https://zenodo.org/api/records/20509007/files/Muslim_Family_Laws_Ordinance_1961.csv/content)
- **"Police law" is the Police Order, 2002**, not the Police Act, 1861. First row: "(1) This Order may be called the Police Order, 2002." The file's tail is a performance-evaluation form ("PART IV FIRST COUNTERSIGNING OFFICER'S EVALUATION…") parsed as a "section". — [Police_law.csv (range sample)](https://zenodo.org/api/records/20509007/files/Police_law.csv/content)
- **PPC coverage gaps.**
  - Section numbers run 1 to 511.
  - Only 6 lettered sections exist as rows: 310A, 365B, 371B, 496A, 496B and 496C.
  - Absent as separate rows: 295-A/B/C, 489-F and 337-A onward. Only "337" exists, alongside 302, 310, 311, 322, 324, 376, 420 and 506.
  - There are 4 duplicate section numbers.
  - Source: [Datatset For FAISS.csv](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content)
- **CrPC gaps.** Sections 154, 161, 173 and 497 are present. Sections 164, 498 and 561-A are not found as rows. — same source
- **Limitation Act gaps.** Only sections 1–27 and 29 are present (28 rows). The First Schedule, which sets the limitation periods, is not present. — same source
- **Currency indicators.**
  - Amending-statute years matching "Act/Ordinance, 20xx" in the text go no later than 2006 (2004 ×2, 2006 ×39).
  - The strings "2016" through "2024" never occur in the file.
  - The strings "pakistancode" and "Pakistan Code" never occur.
  - Source: same source
- **Extraction noise.**
  - Words are split: "wher e", "non -Muslim", "cont ained", "qatl -i-amd", "b eyond".
  - Footnote text is merged into section text. For example, a PPC row ends with "Substituted by Federal Laws (Revision and Declaration) Ordinance, 1981 (XXVII of 1981)…", and the Limitation Act s.2 row includes Gazette-of-India publication footnotes.
  - Curly quotes appear as U+FFFD replacement characters in several files.
  - Sources: [PPC sample](https://zenodo.org/api/records/20509007/files/Pakistan_Penal_Code.csv/content); [Limitation sample](https://zenodo.org/api/records/20509007/files/2-limitation-act-1908-pdf_extracted.csv/content)
- **Sample rows (truncated, verbatim):**
  - `Pakistan Penal Code,I,INTRODUCTION,1,Title and extent of operation of the Code.,"This Act shall be called the Pakistan Penal Code, and shall take effect throughout Pakistan."` — [PPC sample](https://zenodo.org/api/records/20509007/files/Pakistan_Penal_Code.csv/content)
  - `"Qanun-e-Shahadat Order, 1984",XIII,Miscellaneous,166,Repeal ,"The Evidence Act, 1872 (I of 1872), is hereby repealed."` — [QSO sample](https://zenodo.org/api/records/20509007/files/qanun-e-shahadat_1984.csv/content)
  - `"Muslim Family Laws Ordinance, 1961",I,Muslim Family Laws Ordinance 1961,1,"Short title, extent, application and commencement","(1) This Ordinance may be called the Muslim Family Laws Ordinance, 1961. (2) It extends to whole of Pakistan…"` — [MFLO sample](https://zenodo.org/api/records/20509007/files/Muslim_Family_Laws_Ordinance_1961.csv/content)
- **Source of the text.** The only statement is "parsed from official PDF versions". The record gives no URL, no portal name and no edition or "as amended up to" date. — [Zenodo record](https://zenodo.org/records/20509007)

### Inferences
- The "8 documents" are probably 7 statutes plus the lawyer Q&A file, or a miscount. No CPC 1908 data exists despite "Civil Procedure" in the description. The Limitation Act appears to have been counted as civil procedure.
- The footnote style ("Substituted by Federal Laws (Revision and Declaration) Ordinance, 1981") resembles consolidated texts on the federal Pakistan Code portal. This is not confirmed: the dataset never names its source.
- No amendment year after 2006 appears, and lettered PPC sections are missing. Two explanations fit: the PDFs pre-date later amendments, or amendments and inserted sections were lost in parsing. Either way, the text should be presumed **not current**. This matters because current-law answers depend on sections inserted after 2006, for example 489-F and the honour-crime and anti-rape amendments. This inference was not checked line by line against Pakistan Code.
- The only plausible reuse of the statute files is as a rough list of section numbers and headings for checking coverage, and the PJN official ingest would supersede even that.
- The lawyer Q&A file (about 44 KB) is the most distinctive asset. Its value is the realistic user questions, which can serve as eval prompts. Its answers are short and sometimes legally loose (for example "Inheritance Act, 1925"; the Pakistani statute is the Succession Act, 1925, which comes from background knowledge and was not verified here). It must not be used as gold answers.

### Gaps
- The text was not diffed against the current Pakistan Code PDFs, so the exact edition and date cannot be pinned.
- The parquet file was not opened, and its contents and row count are unknown.
- The full CrPC and combined files were not downloaded, so row-level counts for them come from the FAISS file only.
- The Q&A row count was not established without downloading the whole file. The file is 43,753 bytes.

---

## Q3. GitHub: what is SyedAhtsham/Pakistani-Law-Cases-Search-Engine?

### Takeaway
The repo is real but was abandoned after a final push on 8 May 2023, and it has no licence. It is a BSCS 7th-semester NLP group assignment submitted on 17 December 2021, a Flask BM25/TF-IDF search app.
- It contains **1,000 Supreme Court judgment PDFs**, committed twice: once in `myproject/AllCases/` and again in `myproject/static/AllCases/`.
- It has no structured metadata and no full-text extraction: only per-document lists of stemmed, deduplicated tokens.
- The README's claim to have "extracted all the decisions made by the Supreme Court of Pakistan till now" is false.

### Cited Findings
- **Repo metadata.**
  - Owner SyedAhtsham (User, id 49922045). The description is null.
  - Created 2022-12-10T23:15:23Z; pushed_at 2023-05-08T17:46:28Z.
  - 0 stars, 1 fork, 0 open issues, no topics; not archived; size 137,394 KB; default branch main.
  - Languages (bytes): Python 9,005,949, PowerShell 19,611, JS 10,521, CSS 9,339, HTML 5,887, Batchfile 1,403.
  - Sources: [GitHub API repo](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine); [languages](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/languages)
- **Licence.** `GET /license` returned 404 "Not Found" and the license field is null. No LICENSE file exists. — [GitHub API license](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/license)
- **Commit history** (5 commits in total):
  - 2022-12-10 "Initial commit"
  - 2022-12-10 "Update README.md"
  - 2022-12-10 "First commit"
  - 2022-12-11 "report of the project"
  - 2023-05-08 "Update README.md"
  - Source: [GitHub API commits](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/commits?per_page=100)
- **Fork.** The only fork is devinecomedy/Pakistani-Law-Cases-Search-Engine, created 2024-11-26, with no new pushes. — [GitHub API forks](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/forks)
- **README, quoted in full apart from the image links:** "Casearch – A web application that retrieves the Law cases' decisions on the basis of a given query and rank the resultant documents according to their weights for the given terms as query, it works like Google. We also generated the word cloud from the documents that came out for the given query. We extracted all the decisions made by the Supreme Court of Pakistan till now. Categorized all the cases, extracted the text from all the documents, generated a dictionary of the terms used in the documents, indexed them, and used the BM-25 and Log term frequency weighting measures to calculate the weight of the documents given a query term." — [README (raw)](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/README.md)
- **File tree** (recursive listing, 4,673 entries, not truncated):
  - 2,001 PDFs: 1,000 in `myproject/AllCases/` (144.8 MB) and the same 1,000 again in `myproject/static/AllCases/`, plus the report
  - 1,051 .txt files
  - 672 .py files and 655 .pyc files
  - 16 .exe files
  - A committed `myproject/venv` with 1,596 files
  - Large derived index files: bm25.txt (60.2 MB), tf_idf.txt (61.1 MB), logFrequency.txt (46.7 MB), vocabulary.txt (9.4 MB)
  - Source: [GitHub API tree](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/git/trees/main?recursive=1)
- **Corpus composition.**
  - Filename prefixes in AllCases: crl_ 192, c.p_ 174, p.c_ 154, m.c_ 152, c.a_ 128, s.m_ 82, h.r_ 67, f.c_ 51 (1,000 in total).
  - `categories.txt` gives: Civil Appeals 128, Civil Petetion [sic] 174, Criminal Cases 192, Family Cases 51, Human Rights 67, Murder Cases 152, Property Cases 153, Suo Moto 82.
  - Sources: [GitHub API tree](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/git/trees/main?recursive=1); [categories.txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/categories.txt)
- **No structured metadata.**
  - Documents are identified only by `category_index.pdf`; `documentIndex.txt` maps integers to filenames.
  - `abstracts.txt` has just 8 lines, one per category. Example: "c.a:CIVIL APPEAL NO.1474. OF 2015 (Against the judgment dated _16.12.2014 passed by the Peshawar High Court, Peshawar in Writ Petition No.162 of 2014)."
  - No files carry case number, date, bench, parties or citation fields.
  - Sources: [abstracts.txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/abstracts.txt); [documentIndex.txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/documentIndex.txt)
- **The "extracted text" is not full text.**
  - `CasesTokens.py` uses pdfplumber. It lowercases the text, strips punctuation, deletes words of 1–3 characters, removes stopwords, lemmatizes and Porter-stems, keeps only dictionary words, names or years 1947–2021, and writes each **unique** token once per document into `File cases tokens/*.txt`.
  - Sample output from `c.a_10.pdf.txt`: "court / appel / present / anwar / rahman / civil / appeal / 2000 / judgment …".
  - Sources: [CasesTokens.py](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/CasesTokens.py); [token sample](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/File%20cases%20tokens/c.a_10.pdf.txt)
- **Extraction failures.** Of 1,015 token files, 29 are empty (0 bytes) and 57 are under 100 bytes. — [GitHub API tree](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/git/trees/main?recursive=1)
- **Search quality reported by the project.** `evaluation(bm25).txt` gives precision 0.4–0.7 and recall 0.026–0.074 on 5 queries, and "Mean Average Precision for 5 queries = 0.003". The queries were bag-of-words strings such as "convict constitution". — [evaluation(bm25).txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/evaluation(bm25).txt); [queries(bm25).txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/queries(bm25).txt)
- **Unrelated code.** `myproject/Python Code.py` is a hospital Patient/Medicine class exercise. — [Python Code.py](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/Python%20Code.py)
- **Project report provenance.**
  - Cover page: "GROUP ASSIGNMENT BSCS 7th SEMESTER … Muhammad Faizan … Syed Ahtsham … Subject Title: Natural Language Processing; Submission Date: December 17, 2021; Submit To: Dr. Akmal Saeed Khattak".
  - Methodology: "For corpus of 1000 documents, we scraped website https://www.supremecourt.gov.pk/ and stored all the computer storage in 8 different categories".
  - Dataset chapter: "we needed a dataset containing judgment cases of different categories scraped from https://www.supremecourt.gov.pk. For this purpose we used: 1000 cases, 8 Categories".
  - Source: [CaSearch Report.pdf](https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf)
- **Sample PDFs (3 inspected).** All begin "IN THE SUPREME COURT OF PAKISTAN" and were produced by doPDF. None has headnotes or publisher citations on page 1.
  - **c.a_110.pdf:** Civil Appeals 149–150 of 2010, decided 21.08.2013, bench headed by Iftikhar Muhammad Chaudhry CJ. Ends "NOT APPROVED FOR REPORTING". PDF CreationDate 2013-08-22.
  - **crl_10.pdf:** Criminal Appeal No.6-P/2010, decided 29.04.2019. The order cites "(PLD 1996 SC 274)" within the judgment text.
  - **s.m_1.pdf:** Suo Motu Case No.3 of 2018 (dual nationality), 52 pages, announced 15.12.2018. Stamped "Approved for Reporting".
  - Sources: [c.a_110.pdf](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/AllCases/c.a_110.pdf); [crl_10.pdf](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/AllCases/crl_10.pdf); [s.m_1.pdf](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/AllCases/s.m_1.pdf)

### Inferences
- The judgments are court-issued PDFs of the kind the Supreme Court posts: official cause-title layout, approval-for-reporting stamps and doPDF producer strings. They are not PakistanLawSite or PLD/SCMR publisher copies. No publisher headnotes were seen.
- Internal citations such as "PLD 1996 SC 274" are part of the judges' own text. That is normal and is not publisher matter.
- From the three samples, the years covered appear to be roughly 2010s up to 2021: the scrape was done no later than December 2021, and the token filter caps years at 2021. The exact year range was not measured.
- 1,000 documents is a small fraction of the Supreme Court's output. The 8 categories look like the students' own grouping, for example "Murder Cases" and "Property Cases". They do not match the Court's own case-type taxonomy, though this was not verified against the SCP site.
- Without a licence, the code is all-rights-reserved by default. The judgments themselves are court documents rather than the students' work.

### Gaps
- The full year distribution and case-number list of the 1,000 PDFs were not measured, because that would need a bulk download.
- The exact SCP URLs or listing pages scraped are unknown. The report gives only the domain.
- The share of scanned or image-only PDFs is unknown beyond the 29 empty and 57 near-empty token files.
- The students' university is not stated in the report. Do not assume it.

---

## Q4. Provenance against PJN constraints, and a recommendation for each dataset

### Takeaway
**Neither dataset can be cited as evidence.**
- **Zenodo record 20509007:** at most a non-authoritative coverage hint. Its lawyer-written questions (also in 20509273) could serve as eval prompts under CC-BY-4.0 with attribution, but not its answers.
- **GitHub repo:** not usable as a data source. Its only value is a list of about 1,000 SCP judgments that PJN could re-fetch from the Supreme Court itself, within the Court's terms, as an ingestion or coverage test set.

### Cited Findings
- **Zenodo provenance.**
  - The record says only "parsed from official PDF versions", with no URL or edition date. — [Zenodo record](https://zenodo.org/records/20509007)
  - The record is licensed CC-BY-4.0. — [Zenodo API record](https://zenodo.org/api/records/20509007)
- **GitHub provenance.**
  - The report states the corpus was "scraped [from] website https://www.supremecourt.gov.pk/". — [CaSearch Report.pdf](https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf)
  - The repo has no licence. — [GitHub API license 404](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/license)
- **Constraints established earlier in this research effort; not re-fetched here, so treat them as inputs:**
  - The Supreme Court's robots.txt (supremecourt.gov.pk / scp.gov.pk) declares "Content-Signal: search=yes,ai-train=no,use=reference" and blocks AI crawlers.
  - Copyright Ordinance 1962 s.57(1)(q)(ii) permits reproduction and publication of court judgments, but not publisher headnotes or editorial matter.

### Inferences

**Zenodo record 20509007**
- **Citable evidence: no.**
  - It is a third-party derivative and does not identify its source or edition.
  - It shows label corruption, merged footnotes, missing sections (PPC 295-A/B/C, 489-F, 337-A ff; CrPC 164, 498, 561-A; the Limitation First Schedule) and likely staleness after 2006.
  - PJN policy requires official government sources, and statute text should come from Pakistan Code or the provincial portals.
- **Copyright and ToS.** Statute text is government law, and the CC-BY-4.0 licence covers the compilation, so no copyright barrier stands in the way of internal use. Attribution to Umair Ahmed and the DOI is required if any part is redistributed.
- **Coverage cross-check: weak.** Section and heading lists could flag gross ingest gaps in the 7 statutes. But the dataset is itself incomplete, so a "missing in PJN" signal must always be confirmed against Pakistan Code. A better coverage oracle is PJN's own table of contents parsed from official PDFs.
- **Eval/test data: limited but plausible.**
  - Use the lawyer-written **questions** in Legal_QA_dataset_From_lawyers.csv (also record 20509273) as realistic user prompts, for example on family, inheritance and custody.
  - Do not use its **answers** as ground truth: they are short, informal and sometimes imprecise.
  - The generated "What does Section X say?" prompts in combined_legal_dataset.csv could seed retrieval tests, but the answers must be re-grounded on official text.
  - Exclude the "Chatbot Info" identity rows.
- **Fine-tuning/RAG corpus: not recommended**, because of the quality defects and possibly stale law.

**GitHub repo SyedAhtsham/Pakistani-Law-Cases-Search-Engine**
- **Citable evidence: no.** It is an unlicensed student mirror with no metadata. Any judgment PJN cites should be fetched from the Supreme Court's official site so the citation URL is official.
- **Provenance against the constraints:**
  - The PDFs appear to be official SCP copies, not PakistanLawSite or PLD/SCMR publisher works, so the headnote and publisher-copyright concern does **not** appear to apply. Publication of the judgment text itself falls within s.57(1)(q)(ii) as previously established.
  - However, the corpus was produced by scraping supremecourt.gov.pk. Using this mirror for AI training would conflict with the Court's "ai-train=no" signal, and using it as a backdoor around the Court's crawler policy would be poor practice.
  - Whether the Content-Signal existed in 2021 is unknown, but PJN's use would happen now.
  - "use=reference" suggests reference/RAG-style use of SCP content fetched in line with the site's terms is the permissible route.
- **Coverage cross-check / eval: marginal.** The 1,000 judgments are known SCP decisions across 8 informal categories, roughly 2010s to 2021. After re-fetching from the official source, they could form a small regression set ("can PJN find CA 149/2010?"). The tokens and BM25 artefacts are useless.
- **Code reuse: no.** There is no licence, the code is trivial BM25/TF-IDF, it includes a committed venv and executables, and its MAP is 0.003.

**Better alternatives seen in passing (not vetted in depth)**
- Zenodo 21671415 (Ul-Hasan and Shafait) packages 214 English SCP civil-appeal judgments with token-level NER labels under CC-BY-4.0. Its source is "publicly available records of the Supreme Court of Pakistan". It could be a citation and party-extraction eval set. — [Zenodo API record 21671415](https://zenodo.org/api/records/21671415)
- Several 2025–2026 Hugging Face "Pakistan laws" datasets exist, for example AyeshaJadoon/Pakistan_Laws_Dataset and justicedao/ipfs_pakistan_laws_ir. They are not vetted. — [HF API search](https://huggingface.co/api/datasets?search=pakistan%20law)

### Gaps
- The current wording of the SCP robots.txt and terms was not re-verified in this pass.
- Whether SCP terms of use say anything specific about bulk mirroring was not checked.
- Zenodo 21671415 and the HF datasets were not vetted. Their file contents and provenance would need a separate review.

---

## Q5. The user's descriptions compared with what was found

### Takeaway
The Zenodo description is mostly accurate, but it misses the record's defects and the fact that the paper is unpublished. The GitHub description is materially wrong on scope and content: only 1,000 judgments, no full extracted text, and no metadata.

### Cited Findings: claims vs reality

| # | User's claim | Reality (verified) | Verdict | Source |
|---|---|---|---|---|
| Z1 | Exists on Zenodo as a "Pakistani Law Dataset" | Record 20509007, "Pakistani Law Dataset: Structured Legal Acts of Pakistan (Criminal, Family, and Property Law)", DOI 10.5281/zenodo.20509007, 2026-06-02, CC-BY-4.0 | True | [API](https://zenodo.org/api/records/20509007) |
| Z2 | Created for academic LLM fine-tuning research | Description says it was "Designed for use in legal AI, RAG pipelines, and LLM fine-tuning" and built for a paper "submitted to PLOS ONE, 2025". The paper is not found in PLOS, Crossref or the author's ORCID; it is an undergraduate project at Sukkur IBA per in-data rows | Partly true: research purpose real, paper unpublished/unverified | [Record](https://zenodo.org/records/20509007); [PLOS API](https://api.plos.org/search); [ORCID](https://pub.orcid.org/v3.0/0009-0009-3291-0686/works) |
| Z3 | Parses 8 foundational statutes | 7 statutes: PPC, CrPC 1898, QSO 1984, MFLO 1961, TPA 1882, Police Order 2002, Limitation Act 1908. The record's "8 documents" likely counts the lawyer Q&A file. The description mentions "Civil Procedure" but no CPC file exists | False / overstated | [API files](https://zenodo.org/api/records/20509007); [FAISS CSV](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content) |
| Z4 | Covers PPC, CrPC, QSO 1984, MFLO 1961 | All present. CrPC filename says "upto 16 chapter", has mislabelled rows, and lacks e.g. s.164, 498, 561-A. PPC lacks most lettered sections, e.g. 295-A/B/C and 489-F | True but incomplete | [FAISS CSV](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content) |
| Z5 | "property and police laws" | Transfer of Property Act 1882 and the Police Order 2002 (with ACR forms parsed as sections) | True (unspecified in claim) | [Police sample](https://zenodo.org/api/records/20509007/files/Police_law.csv/content) |
| Z6 | Structured CSVs | Statute CSVs share the schema Book / Chapter Number / Chapter Title / Section / Heading / "Defination" [sic]. combined_legal_dataset.csv is Query/Response, and one parquet file exists. The CrPC CSV has hundreds of empty trailing columns | Partly true | [PPC sample](https://zenodo.org/api/records/20509007/files/Pakistan_Penal_Code.csv/content); [combined sample](https://zenodo.org/api/records/20509007/files/combined_legal_dataset.csv/content) |
| Z7 | (Implicit) official/current text | Says "official PDF versions" but gives no URL or edition. No amendment years after 2006 appear, and the text has extraction noise and merged footnotes | Not supported | [FAISS CSV](https://zenodo.org/api/records/20509007/files/Datatset%2520For%2520FAISS.csv/content) |
| G1 | Repo exists at SyedAhtsham/Pakistani-Law-Cases-Search-Engine | Exists. Created 2022-12-10, last push 2023-05-08, 5 commits, 0 stars, 1 fork, no licence, no description | True | [GitHub API](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine) |
| G2 | Indexes SCP decisions | 1,000 SCP judgment PDFs (stored twice) in 8 informal categories, scraped from supremecourt.gov.pk by Dec 2021. README's "all the decisions … till now" is false | Partly true; scope grossly overstated in README | [Tree](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/git/trees/main?recursive=1); [Report](https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf) |
| G3 | Extracted text | Only per-document lists of unique, stemmed, filtered tokens. 29 token files empty and 57 under 100 bytes. Full text exists only inside the PDFs | Misleading | [CasesTokens.py](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/CasesTokens.py) |
| G4 | Metadata | None structured: filename = category + index. No case number, date, bench or citation fields; abstracts.txt has 8 lines | False | [abstracts.txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/abstracts.txt) |
| G5 | BM25 search scripts | Yes: BM25.py, TF_IDF.py, CosineSimilarity(BM25).py and a Flask app.py. Self-reported MAP 0.003 on 5 queries | True (low quality) | [evaluation(bm25).txt](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/evaluation(bm25).txt) |
| G6 | (Concern) Sourced from PakistanLawSite / publisher headnotes | No evidence. The report names supremecourt.gov.pk, and the sampled PDFs are court-issued copies with no headnotes | Concern not borne out (on samples) | [Report](https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf); [c.a_110.pdf](https://raw.githubusercontent.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/main/myproject/AllCases/c.a_110.pdf) |

### Inferences
- The user's Zenodo description is a fair paraphrase of the record's own blurb. It inherits the blurb's errors: the "8" statute count and the missing "Civil Procedure".
- The GitHub description repeats the README's overstatement. Anyone using this repo should treat it as a 1,000-document 2021 student snapshot.

### Gaps
- No independent review, citation or download feedback exists for either dataset beyond the Zenodo download counters.
