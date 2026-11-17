# Official judgment publishing: Lahore High Court (LHC) and Sindh High Court (SHC)

Research date: 12 November 2026. All "fetched" items were retrieved live on that date with curl or WebFetch, from a Windows client, using a browser User-Agent and gaps of 1-3 seconds between requests. No CAPTCHA, login or access control was bypassed. Totals in this note are those shown on official listings on 12 Nov 2026. Sample PDFs downloaded: 2 from LHC and 1 from SHC, to test text extraction only.

Conventions: "Cited Findings" holds raw facts and quotes taken from the source. "Inferences" holds my analysis. Items marked [snippet-only] were not fetched. Items marked [secondary] are news reports.

---

## 0. Source inventory

| # | Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|---|
| 1 | LHC robots.txt | https://www.lhc.gov.pk/robots.txt (same file at https://lhc.gov.pk/robots.txt) | LHC | robots | live 12-11-2026 | Primary | fetched, 200 |
| 2 | data.lhc.gov.pk robots.txt | https://data.lhc.gov.pk/robots.txt | LHC | robots | live | Primary | inaccessible: **HTTP 403 Forbidden** |
| 3 | sys.lhc.gov.pk robots.txt | https://sys.lhc.gov.pk/robots.txt | LHC (IIS host for PDFs) | robots | live | Primary | inaccessible: **HTTP 404** (IIS "File or directory not found"). The root https://sys.lhc.gov.pk/ returns **HTTP 500** |
| 4 | LHC "Reported Judgments" landing page | https://lhc.gov.pk/reported_judgments | LHC | judgment index | live | Primary | fetched, 200 |
| 5 | LHC "Judgments Approved for Reporting" (sitting judges) | https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting | LHC | judgment search/listing | latest upload shown: 12-11-2026 | Primary | fetched, 200. The first attempt timed out (curl code 000); the retry succeeded |
| 6 | LHC AFR result endpoint (sitting judges) | https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=…&courtName=All%20Courts&… | LHC | HTML fragment (AJAX GET) | live | Primary | fetched for year=2010, 2015 and 2025 |
| 7 | LHC "Judgments Approved for Reporting by Former Judges" | https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting_by_former_judges | LHC | judgment search/listing | live | Primary | fetched, 200 |
| 8 | LHC AFR result endpoint (former judges) | https://data.lhc.gov.pk/dynamic/approved_judgments_result_former_judges.php?year=… | LHC | HTML fragment | live | Primary | fetched for year=2010, 2020 and 2025 |
| 9 | LHC sample judgment PDF | https://sys.lhc.gov.pk/appjudgments/2026LHC8763.pdf | LHC | judgment PDF | Last-Modified 12-11-2026 | Primary | fetched, 200, application/pdf, 362,580 bytes |
| 10 | LHC sample order PDF | https://sys.lhc.gov.pk/appjudgments/2019LHC5273.pdf | LHC | judgment PDF | 2019 decision | Primary | fetched, 200, application/pdf, 175,920 bytes |
| 11 | LHC home page | https://www.lhc.gov.pk/ | LHC | portal | live | Primary | fetched, 200 |
| 12 | LHC Case Management page | https://lhc.gov.pk/case_management | LHC | portal | live | Primary | fetched, 200 |
| 13 | LHC Regular Cause List | https://data.lhc.gov.pk/case_management/regular_cause_list | LHC | cause list | live | Primary | fetched, 200 |
| 14 | LHC Research Center | https://researchcenter.lhc.gov.pk/ | LHC | research portal | live | Primary | fetched, 200. robots.txt returns 404 |
| 15 | LHC Annual Reports page; Annual Report 2025 PDF | https://lhc.gov.pk/annual_reports ; https://lhc.gov.pk/system/files/Annual%20Report%202025.pdf | LHC | annual report | 2025 | Primary | fetched (PDF 5.19 MB, text-extractable) |
| 16 | SHC caselaw robots.txt | https://caselaw.shc.gov.pk/robots.txt | SHC (Cloudflare) | robots | live | Primary | fetched, 200 |
| 17 | SHC main-site robots.txt | https://sindhhighcourt.gov.pk/robots.txt (shc.gov.pk and www.shc.gov.pk 301-redirect here) | SHC | robots | live | Primary | fetched, 200 |
| 18 | digital.shc.gov.pk robots.txt | https://digital.shc.gov.pk/robots.txt | SHC | robots | live | Primary | fetched, 200 |
| 19 | cases.shc.gov.pk robots.txt | https://cases.shc.gov.pk/robots.txt | SHC | robots | live | Primary | fetched, 200 (byte-identical to #16) |
| 20 | SHC Caselaw Advance Search | https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search | SHC | judgment search | live | Primary | fetched, 200 (1.22 MB page) |
| 21 | SHC search JS | https://caselaw.shc.gov.pk/caselaw/theme/js/search.js | SHC | technical | live | Primary | fetched, 200 |
| 22 | SHC search AJAX endpoint | https://caselaw.shc.gov.pk/caselaw/AJAX_PUBLIC.php (POST, opt=search_judgement) | SHC | JSON (contains an HTML table) | live | Primary | fetched once (AFR, Karachi, Criminal Appellate, 01-Oct-26 to 31-Oct-26) |
| 23 | SHC sample judgment PDF | https://caselaw.shc.gov.pk/caselaw/view-file/MzI4NzczY2Ztcy1kYzgz | SHC | judgment PDF | judgment dated 26.10.2026 | Primary | fetched, 200, application/pdf, 176,330 bytes, 12 pages |
| 24 | SHC Caselaw home ("Latest Case Law (Approved For Reporting)") | https://caselaw.shc.gov.pk/caselaw/public/home | SHC | listing | live | Primary | fetched, 200 (1.35 MB) |
| 25 | SHC Report-002 A.F.R. | https://caselaw.shc.gov.pk/caselaw/public/rpt-afr | SHC | statistics | live | Primary | fetched, 200 |
| 26 | SHC Report-005 Judgement/Order wise | https://caselaw.shc.gov.pk/caselaw/public/rpt-jo | SHC | statistics | live | Primary | fetched, 200 |
| 27 | SHC Report001 Seat/Bench Wise | https://caselaw.shc.gov.pk/caselaw/public/reported-judgements | SHC | statistics | live | Primary | inaccessible: the page body is an embedded **404**, "The requested URL /caselaw/public/rpt_judgement.php was not found on this server" (Apache/2.4.39 Win64, PHP/7.2.18) |
| 28 | SHC main site home | https://sindhhighcourt.gov.pk/ | SHC | portal | live | Primary | fetched, 200 |
| 29 | SHC Disclaimer | https://sindhhighcourt.gov.pk/disclaimer.php | SHC | terms | text says "© Sindh High Court: 2001-2002" | Primary | fetched, 200 |
| 30 | SHC Cause List page | https://sindhhighcourt.gov.pk/causelist.php | SHC | cause list | live | Primary | fetched, 200 |
| 31 | SHC Digital Copy / eCTC portal; Search Citation | https://digital.shc.gov.pk/ ; https://digital.shc.gov.pk/search-citation | SHC | e-services | "© 2026" | Primary | fetched, 200 |
| 32 | "SHC launches AI-enabled search engine, mobile app" | https://www.thenews.pk/print/1415951-shc-launches-ai-enabled-search-engine-mobile-app | The News | news [secondary] | 17 May 2026 | Medium-high | fetched (WebFetch) |
| 33 | "SHC chief justice inaugurates project to digitise judicial process" | https://www.dawn.com/news/1941060/shc-chief-justice-inaugurates-project-to-digitise-judicial-process | Dawn | news [secondary] | 11 Sep 2025 | Medium-high | fetched (WebFetch) |
| 34 | "LHC CJ launches digital systems to modernise judiciary" | https://www.dawn.com/news/1964198/lhc-cj-launches-digital-systems-to-modernise-judiciary | Dawn | news [secondary] | 31 Dec 2025 | Medium-high | fetched (WebFetch) |
| 35 | Express Tribune, "Lahore High Court pushes forward with case record digitalisation" | https://tribune.com.pk/story/2578873/lahore-high-court-pushes-forward-with-case-record-digitalisation | Express Tribune | news [secondary] | ~16 Dec 2025 (per search listing) | Medium | snippet-only |
| 36 | SHC Press Release May 2026 | https://sindhhighcourt.gov.pk/news_notifications/source_files/Press_Release/SHC_Press_Release_may_2026.pdf | SHC | press release | May 2026 | Primary | snippet-only (search result; not fetched) |
| 37 | Third-party aggregator showing "LHC" citations | https://pakcaselaw.duckdns.org/browse/court/lahore-high-court | unofficial | aggregator | n/a | Low (unofficial; not a permitted source for this corpus) | snippet-only |

---

## 1. LHC: official judgment search and listing URLs (verified)

### Takeaway
LHC publishes only judgments **"Approved for Reporting"**. They appear in two official listings on data.lhc.gov.pk, one for sitting judges and one for former judges. Each item links to a PDF at a predictable URL, `https://sys.lhc.gov.pk/appjudgments/{YYYY}LHC{N}.pdf`, where `{YYYY} LHC {N}` is the court's own neutral citation. lhc.gov.pk is a Drupal front end that links to these pages. sys.lhc.gov.pk is a bare IIS file host.

### Cited Findings
- The "Reported Judgments" menu on lhc.gov.pk links to four pages: `http://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting`, `https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting_by_former_judges`, `.../green_bench_orders` and `.../school_security_orders`. The menu labels are "Judgments Approved for Reporting by Sitting Judges", "Judgments Approved for Reporting by Former Judges", "Green Bench Orders", "School Security Orders" and "Green Bench Notifications" — [LHC Reported Judgments](https://lhc.gov.pk/reported_judgments)
- The bare root `https://data.lhc.gov.pk/` returns a 302 redirect to `https://lhc.gov.pk/`. The http:// listing URL returns a 302 to its https:// form — [data.lhc.gov.pk](https://data.lhc.gov.pk/)
- The sitting-judges page opens with a "Latest Reported Judgments" list. The first item on 12-11-2026 read: "1. Jail Revision 383/25 (Shah Nawaz Vs The State) by Mr. Justice Tariq Saleem Sheikh uploaded on: 12-11-2026", linked to `https://sys.lhc.gov.pk/appjudgments/2026LHC8763.pdf` — [LHC AFR](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting)
- The search form calls the endpoint via jQuery `$.get`: `$.get('https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year='+year+'&debug='+debug+'&courtName='+courtName+'&caseNumber='+caseNumber+'&citationTag='+citationTag+'&partyName='+partyName+'&decisionDate0='+...+'&uploadDate1='+uploadDate1 ...)` — [LHC AFR page source](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting)
- The former-judges page uses the same pattern against `https://data.lhc.gov.pk/dynamic/approved_judgments_result_former_judges.php?year=...`. Its judge dropdown has 86 options — [LHC AFR former judges](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting_by_former_judges)
- Each result row contains a direct PDF link and a commented-out alternative: `<a href='https://sys.lhc.gov.pk/appjudgments/2025LHC8083.pdf' ...>` and `<!-- <a href='https://data.lhc.gov.pk/reported_judgments/download_file/10366/2025LHC8083' ...> -->` — [LHC result endpoint, year=2025](https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2025&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=)
- sys.lhc.gov.pk sends PDFs with `Server: Microsoft-IIS/8.5`, `Content-Type: application/pdf`, and a `Last-Modified` header (for example "Thu, 12 Nov 2026 12:51:46 GMT") — [sample PDF](https://sys.lhc.gov.pk/appjudgments/2026LHC8763.pdf)
- Other official LHC hosts linked from the home page: `https://researchcenter.lhc.gov.pk` (research memoranda, bulletins, "CITATORS" menu), `https://data.lhc.gov.pk/certified_copy_status`, and a PITB Android app `pk.gov.pitb.lhccasemanagement` — [LHC home](https://www.lhc.gov.pk/)

### Inferences
- **Hosts to configure:** data.lhc.gov.pk (listings), sys.lhc.gov.pk (PDFs) and lhc.gov.pk (navigation only). researchcenter.lhc.gov.pk is a separate research host, not a judgment repository.
- The `download_file/{id}/{citation}` route is commented out in the HTML. Do not rely on it. The `sys.lhc.gov.pk/appjudgments/` pattern is the live canonical PDF URL.

### Gaps
- I did not fetch the Green Bench Orders or School Security Orders pages. They are thematic order sets, likely small.
- I did not check whether `researchcenter.lhc.gov.pk` hosts any judgment full texts. Its "JUDICIAL WORK", "BULLETIN" and "CITATORS" menus were seen but not opened.

---

## 2. LHC: what is published, coverage, counts, citation format

### Takeaway
Only judgments that judges approve for reporting ("AFR") are published, from **2010 to the present**. They are split between sitting and former judges. Each carries an LHC neutral citation ("2025 LHC 8083"), cross-references to commercial reporters, and an optional "Tag Line" summary. Volume is small next to disposals: about **763 AFR judgments for 2025**, against **173,229 cases disposed** in 2025. Bench (Rawalpindi/Multan/Bahawalpur) is not a filter. It appears only in the PDF caption and in reporter citations such as "[Lahore(Multan Bench)]".

### Cited Findings
- The year filter offers "Any Year 2026 2025 … 2011 2010" on both the sitting-judges and the former-judges pages — [LHC AFR](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting); [former judges](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting_by_former_judges)
- Result columns: "Sr.# | Case # | Title | Judge | Decision Date | LHC Citation | Other Citations | Judgment". A "Total Downloads" column is commented out — [result endpoint](https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2025&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=)
- Example row (2025): "Civil Revision-Civil Revision (Against Interim Order)-Specific Performance 1594-25 | MUHAMMAD ASIF VS MUHAMMAD ARSHAD ETC | Mr. Justice Muzamil Akhtar Shabir | 26-12-2025 | 2025 LHC 8083 | 2026 CLC 1570 [Lahore(Multan Bench)] | Tag Line: Powers of Appellate Court to reframe issues at appellate stage discussed." — same source
- Example row (2015): "WP- Income Tax 5832-09 M/S. BISMA TEXTILE MILLS LTD VS F.O.P. ETC. … 29-12-2015 | 2015 LHC 8064 | PLJ 2016 Lah. 503,(2016) 113 Tax 69 (H.C. Lah.),2016 PCTLR 295,2016 PTD 1790" — [result endpoint year=2015](https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2015&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=)
- Example row (former judge, 2010): "Criminal Appeal 1507-04 NABEEL AHMAD VS THE STATE Mr. Justice Manzoor Ahmad Malik 22-12-2010 2010 LHC 1558 … Tag Line: Mere relationship of a witness with the deceased is no ground to discard his statement…" — [former-judges endpoint year=2010](https://data.lhc.gov.pk/dynamic/approved_judgments_result_former_judges.php?year=2010&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=)
- Totals shown by the endpoints on 12-11-2026 (the endpoint prints "Total Judgments (n)"):
  - Sitting judges: 2010 = **0**; 2015 = **205**; 2025 = **704**
  - Former judges: 2010 = **164**; 2020 = **141**; 2025 = **59**
  - Sources: endpoint queries above. The row count of PDF links matched each total.
- PDF filenames encode the LHC citation: row "2025 LHC 8083" links to `appjudgments/2025LHC8083.pdf`. All 704 links in the 2025 sitting-judges result follow the `2025LHC{N}.pdf` pattern — same source
- The latest LHC citation number seen in Nov 2026 is 2026 LHC 8763. Numbers are sparse: the 2025 sitting list has 704 items, yet citation numbers run to at least 8203 ("2025 LHC 8203") — [LHC AFR](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting); [2025 result](https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2025&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=)
- LHC Annual Report 2025: "A total of 145,876 cases were instituted during the reported year … 173,229 cases were disposed of during the reported year, leaving a Balance Pendency of 169,035 cases as on 31st December, 2025." — [LHC Annual Report 2025](https://lhc.gov.pk/system/files/Annual%20Report%202025.pdf)
- The cause-list "location" filter lists LHC's seats: "Principal Seat", "Bahawalpur Bench", "Multan Bench", "Rawalpindi Bench". The judgments search has no such filter. Its fields are Year, Hon'ble Judge, Citation/Tag Line, Case #, Title, Decision Date From/To, and Uploaded Date From/To — [LHC regular cause list](https://data.lhc.gov.pk/case_management/regular_cause_list); [LHC AFR](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting)
- Language: every listing and both sample PDFs were in English. I saw no Urdu judgments.

### Inferences
- **Neutral citation:** "YYYY LHC N" is an official LHC citation that appears in the court's own listing column "LHC Citation". The number looks like a court-wide running number, possibly assigned to all uploaded or decided judgments, of which only AFR ones are listed. This explains why numbers run far past the listed counts. Not confirmed. The citation is **not printed inside the PDF text** (no "LHC NNNN" string was found in either sample), so it must be captured from listing metadata or the filename.
- **Partial historical coverage:** the 2010 sitting-judges count is 0 because 2010 judges have since retired and moved to the former-judges list. Both lists must be harvested for complete coverage. Coverage before 2010 appears absent from the official site.
- Approximate total corpus: hundreds to under 1,000 AFR items per year since 2010, so likely on the order of 10,000–15,000 PDFs in all. This is a rough extrapolation from 5 year-samples, not a stated figure.
- This is a reported-judgment corpus, not a complete one. Unreported orders (the vast majority of 173k disposals a year) are not published on these pages.

### Gaps
- No official statement was found on when the LHC neutral citation was introduced, or how numbers are assigned. A web search returned only unofficial aggregator listings ([snippet-only](https://pakcaselaw.duckdns.org/browse/court/lahore-high-court)).
- No official total count across all years is published. I did not query every year.
- Whether `sys.lhc.gov.pk/appjudgments/{YYYY}LHC{N}.pdf` resolves for citation numbers *not* in the AFR listing (i.e. non-AFR judgments) was **deliberately not probed**, because of the copyright notice in §5.

---

## 3. LHC: document format

### Takeaway
LHC PDFs are **born-digital, text-extractable** files generated from Microsoft Word. They use numbered paragraphs, footnotes, and the court's official form headers. They have no headnotes: the only summary is the listing's "Tag Line", when one is given. The "Approved for reporting" endorsement is printed at the end.

### Cited Findings
- 2026LHC8763.pdf: `pdftotext` extracted 5,143 words of clean text. The opening reads: "Stereo. HCJDA 38 / JUDGMENT SHEET / LAHORE HIGH COURT, LAHORE / JUDICIAL DEPARTMENT / Criminal Revision No. 383/J/2025 / Shah Nawaz Vs. The State / JUDGMENT / Date of hearing 12.05.2026 …". Paragraphs are numbered "2.", "3.", "4.". It has footnotes, for example "7 Tariq Pervez v. The State (1995 SCMR 1345)…". It ends "(Tariq Saleem Sheikh) Judge … Approved for reporting". PDF metadata: Title "Form No:HCJD/C-121", Author "IT_Section" — [2026LHC8763.pdf](https://sys.lhc.gov.pk/appjudgments/2026LHC8763.pdf)
- 2019LHC5273.pdf: 1,089 words extracted. It is a short order on the "FORM No. HCJD/C-121 ORDER SHEET IN THE LAHORE HIGH COURT, LAHORE JUDICIAL DEPARTMENT W.P.No. 945 of 2019" template, a two-column order-sheet layout with numbered paragraphs. XMP Producer is "Microsoft…". CreationDate is 2026-11-03, which suggests the file was regenerated or re-uploaded recently — [2019LHC5273.pdf](https://sys.lhc.gov.pk/appjudgments/2019LHC5273.pdf)

### Inferences
- OCR is not needed for the sampled items. However, the order-sheet template's two-column layout adds left-margin whitespace and "Sr. No./Date of order" columns, so the parser should normalise layout. The header metadata (court, case number, parties, hearing date, judge) is semi-structured and regex-friendly.
- Older items (2010–2014) were not sampled and may include scanned PDFs (see Gaps).

### Gaps
- Not checked: whether pre-2015 former-judge PDFs are scans. Sampling one 2010 PDF would settle it, subject to the permission issue in §5.

---

## 4. LHC: search mechanics and programmatic feasibility

### Takeaway
Programmatic access is **technically trivial**: a plain HTTP GET returns an HTML fragment listing every item for a year, with no pagination, CAPTCHA, login or token. PDFs sit at stable, citation-derived URLs. The obstacles are permission, not technology (§5).

### Cited Findings
- The search is a client-side jQuery GET to a PHP endpoint, not an ASP.NET postback. Inputs: `year`, `courtName` (judge name string; default "All Courts"), `caseNumber`, `citationTag`, `partyName`, `decisionDate0/1` and `uploadDate/uploadDate1` (datepicker format `yy-mm-dd`) — [LHC AFR page](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting)
- The year=2025 response (1.36 MB) returned all 704 rows in a single HTML response in about 2.5 s. The year=2015 response (205 rows) took 0.44 s. There was no pagination — [endpoint](https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2025&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=)
- The page sets a `PHPSESSID` cookie (2-hour expiry). The endpoint answered without it. No "captcha" string appears in the AFR or cause-list page source.
- One request to the AFR page timed out on the first attempt and succeeded on retry. The server can be slow or unreliable.

### Inferences
- A polite harvester would make roughly 34 GET requests (17 years × 2 lists), then download PDFs by URL. It can update incrementally using `uploadDate` ranges or the "Latest Reported Judgments" block.
- Use "Uploaded Date" filters for deltas, and keep `Last-Modified` and a hash, since files can be regenerated (see the 2019 PDF with a 2026 CreationDate).

### Gaps
- Rate limits are not documented. No 429s or blocks were observed at my request volume (about 10 requests to data.lhc.gov.pk and 2 to sys.lhc.gov.pk).

---

## 5. LHC: robots.txt and terms/copyright (permission to collect)

### Takeaway
robots.txt on lhc.gov.pk does not block the judgment paths. However, the data host's robots.txt is **403** and the PDF host has **none** (404). More importantly, every LHC page carries a footer saying material **"should not be downloaded without prior agreement"**. Bulk collection for a commercial AI corpus should therefore go through **written permission from the LHC Registrar or IT wing** before scaling.

### Cited Findings
- lhc.gov.pk robots.txt (Drupal default): `User-agent: *` … `Disallow: /core/` `Disallow: /profiles/` … `Disallow: /admin/` `Disallow: /search/` `Disallow: /user/login` … `Disallow: /index.php/search/`. Nothing addresses `/reported_judgments` — [lhc.gov.pk/robots.txt](https://www.lhc.gov.pk/robots.txt)
- data.lhc.gov.pk/robots.txt returns "403 Forbidden – You don't have permission to access this resource." — [data.lhc.gov.pk/robots.txt](https://data.lhc.gov.pk/robots.txt)
- sys.lhc.gov.pk/robots.txt returns "404 - File or directory not found." — [sys.lhc.gov.pk/robots.txt](https://sys.lhc.gov.pk/robots.txt)
- Footer on lhc.gov.pk pages: **"© All photos, graphics and material on this site remain the copyright of Lahore High Court and should not be downloaded without prior agreement"** — [LHC Reported Judgments](https://lhc.gov.pk/reported_judgments); [LHC home](https://www.lhc.gov.pk/); [LHC Case Management](https://lhc.gov.pk/case_management). The data.lhc.gov.pk AFR page has the same copyright footer block (`class="col-sm-8 copyRights"`) — [LHC AFR](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting)
- I found no separate "Terms of Use" or "Disclaimer" page link on lhc.gov.pk. The link scan of the home and Reported Judgments pages found none.

### Inferences
- Under robots.txt alone, collection would not be prohibited: no rule covers the judgment paths, and a 403 or 404 robots file is conventionally treated as "no restriction". The footer, though, is an express reservation against downloading. Whether copyright subsists in judgments under Pakistan's Copyright Ordinance 1962 is a separate legal question (see the copyright_open_data_landscape note). The cautious reading: the LHC has not granted permission for bulk download and has said it should not happen "without prior agreement".
- Recommendation: (a) seek written agreement from the LHC (Registrar or Director IT) before production harvesting; (b) meanwhile, link out to official PDFs rather than mirroring them, or limit any pilot to small-scale, rate-limited retrieval with attribution.

### Gaps
- No LHC open-data or re-use policy was found. It is not known whether LHC has licensed bulk data to commercial reporters (PLD/PLJ/CLC publishers) or to PITB.

---

## 6. LHC: cause lists (for hearing-date features)

### Takeaway
LHC cause lists (Urgent, Regular, Supplementary) are HTML pages on data.lhc.gov.pk. They are filtered by judge, bench type, seat (Principal, Bahawalpur, Multan, Rawalpindi), case number, lawyer or party, and are loaded via GET to a PHP endpoint. The "Export to PDF" button is generated client-side with jsPDF.

### Cited Findings
- Cause-list pages: `http://data.lhc.gov.pk/case_management/urgent_cause_list`, `/regular_cause_list`, `/supplementary_cause_list`, `/urgent_cause_list_final`, `/roster_of_sittings`, `/last_hearing_status`, `/diary_objection_cases`, `/court_map` — [LHC Case Management](https://lhc.gov.pk/case_management)
- The Regular Cause List AJAX call is `dynamic/cause_list_regular_result.php?weekDay=…&courtName=…&color=…&location=…&bench=…&caseNumber=…&lawyerCode=…&lawyerName=…&partyName=…&lawyer_cnic=…&lawyer_mobile=…`. Location options: "Principal Seat", "Bahawalpur Bench", "Multan Bench", "Rawalpindi Bench". Bench options: "Single Bench", "Division Bench", "Full Bench", "Larger Bench", "Ehtisab Bench". The page loads `jspdf.min.js` for "Export to PDF" — [LHC Regular Cause List](https://data.lhc.gov.pk/case_management/regular_cause_list)
- Also offered: "Live Proceedings" on the menu, and an Android app `pk.gov.pitb.lhccasemanagement` — [LHC home](https://www.lhc.gov.pk/)

### Inferences
- Cause-list data is structurally scrapeable per seat and weekday. It contains personal data (lawyer CNIC and mobile are search keys), so handle with care. The same copyright footer applies.

### Gaps
- I did not call the cause-list result endpoint, so the row format is unverified.

---

## 7. LHC: digitisation / e-court / AI initiatives (dated)

### Takeaway
Recent LHC announcements are about administrative and financial digitisation, case-record digitisation and AI training. I found **no announced open-judgments or public AI case-law initiative** for LHC.

### Cited Findings
- 31 Dec 2025 [secondary]: LHC CJ Aalia Neelum inaugurated three digital systems for judicial and financial management, linked to the courts' Case Management System and the National Bank of Pakistan. Dawn called them a first in the judiciary's "150-year-history" — [Dawn](https://www.dawn.com/news/1964198/lhc-cj-launches-digital-systems-to-modernise-judiciary)
- ~16 Dec 2025 [secondary, snippet-only]: "Lahore High Court pushes forward with case record digitalisation". The search snippet says the court directed the Attorney General and Punjab Advocate General to take steps toward legislation for digitalising case records — [Express Tribune](https://tribune.com.pk/story/2578873/lahore-high-court-pushes-forward-with-case-record-digitalisation)
- June 2026 [secondary, snippet-only, URL not isolated]: the search summary reported a Punjab Judicial Academy five-day course for LHC staff, "Generative Artificial Intelligence and its application in the Judiciary". Not verified.
- The LHC Research Center (inaugurated 27 Jan 2012) answers judges' queries "through memoranda prepared by the Research Officers" — [LHC Research Center](https://researchcenter.lhc.gov.pk/)

### Gaps
- The LHC Annual Report 2025 text I scanned is statistics-only. It has no IT or judgment-publication chapter that I found by keyword search for "citation", "digit", "artificial", "cause list".

---

## 8. SHC: official judgment search and listing URLs (verified)

### Takeaway
The main official host is **caselaw.shc.gov.pk** ("CASELAW FOR SINDH HIGH COURT – Search / Upload / View / Download Judgements/Orders"). It runs PHP behind Cloudflare. It covers the Karachi principal seat, the Sukkur Bench, and the Hyderabad, Larkana and Mirpurkhas circuit courts. Unlike LHC, it publishes **judgments and orders, AFR and non-AFR**. The SHC main site also links several legacy and raw-IP caselaw hosts (JSF apps on 43.245.130.98:8056, 202.61.43.40:8055/8056) and a new **digital.shc.gov.pk** eCTC/"Search Citation" portal.

### Cited Findings
- Page header: "CASELAW FOR SINDH HIGH COURT Search / Upload / View / Download Judgements/Orders". Menu: "Report001 - Seat/Bench Wise; Report002 - A.F.R.; Report003 - Consolidated Category wise Judgement/Orders; Report004 - S.B / D.B Category Wise; Report005 - JUDGEMENT/ORDER WISE; Report006 - Bench Wise; Advance Search; Search By Keyword/Statutes-Acts/Ordinance (`pview.php?rpt=topic_search`); Top Searched Judgements/Order; Login" — [SHC Advance Search](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search)
- "Court" select options: "Sindh High Court, Karachi; Sindh High Court, Bench at Sukkur; Sindh High Court, Circuit at Hyderabad; Sindh High Court, Circuit at Larkana; Apellate Tribunal In Land Revenue, Karachi (ATIRK); Sindh High Court, Circuit Court, Mirpur Khas" — same source
- Judgment file URL pattern: `https://caselaw.shc.gov.pk/caselaw/view-file/{token}`. The token is base64 of `{docId}cfms-dc83`; for example `MzI4NzczY2Ztcy1kYzgz` decodes to "328773cfms-dc83". A commented-out older form exists: `rpt_file.php?ax=328773`. Cross-link from the home page: `http://shc.gov.pk/caselaw/hc-link.php?link=caselaw.shc.gov.pk/caselaw/&hash=MzI3OTE3Y2Ztcy1kYzgz` — [SHC search result](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search); [SHC Caselaw home](https://caselaw.shc.gov.pk/caselaw/public/home)
- Each result row also deep-links to the case-flow system on a raw IP, e.g. `http://43.245.130.107:8082/cfms-hc-search/web/index.php?r=cases%2Fsearch-result&…CASENO=556…` — same source
- The SHC main site "CaseLaw" menu includes: "Caselaw Site Home", "Reported Judgments-Sitting Judges", "Reported Judgments-Sitting Judges V2.0 (Beta)", "Seat/Bench/Court Wise Judgment/Orders V2.0", "Search Judgments", "Digital Copy / Apply for eCTC", "Search Citation". Its links include `https://caselaw.shc.gov.pk/caselaw/public/home`, `https://caselaw.shc.gov.pk/caselaw/search-all/search`, `https://digital.shc.gov.pk/search-citation`, `http://202.61.43.40:8056/caselaw/reported-judgements-search/search`, `http://43.245.130.98:8056/caselaw/public/reported-judgements`, `http://43.245.130.98:8056/caselaw/reported-judgements/afr`, and JSF links with embedded public credentials such as `http://43.245.130.98:8056/caselaw/faces/pub/Login.jsp?u=shc&p=shc&a=caselaw-%09shc&afr=y&rp=/caselaw/faces/pub/SearchCaseAdvance.jsp` — [SHC home](https://sindhhighcourt.gov.pk/)
- The domains shc.gov.pk and www.shc.gov.pk 301-redirect to sindhhighcourt.gov.pk — [shc.gov.pk/robots.txt](https://shc.gov.pk/robots.txt)

### Inferences
- **Canonical host for the corpus:** caselaw.shc.gov.pk (HTTPS, Cloudflare). Avoid the raw-IP and http:// legacy hosts: they have no TLS, may be unstable, and the JSF links pass shared credentials in the URL (do not use them, even though the court itself publishes them).
- The view-file token is plain base64 of the numeric ID plus a constant suffix, so URLs are stable and derivable from document IDs. Enumerating IDs outside search results would be "guessing" URLs, though. Prefer IDs obtained from search results.

### Gaps
- Not fetched: `https://caselaw.shc.gov.pk/caselaw/search-all/search` (linked as "Search Judgments") and the "V2.0 (Beta)" pages.
- `public/reported-judgements` (Report001) returned an embedded 404 for `rpt_judgement.php`, so seat/bench totals were unavailable.

---

## 9. SHC: what is published, coverage, counts, citation format

### Takeaway
SHC publishes **both judgments and orders**, each flagged **A.F.R. Yes/No**. Its own neutral citations are **seat-coded**: "2026 SHC KHI 2016", "SHC HYD", "SHC SUK", "SHC LAR", "SHC MPK". Records also carry an internal "SHC Citation: SHC-{id}", topics or head notes, advocates, the authoring judge, and apex-court status. Sitting judges alone account for about **77,258 uploaded judgments/orders, of which about 13,274 are AFR**. These counts are uploads chosen by judges' staff, not total disposals.

### Cited Findings
- Search result columns: "Code | S.No. | Citation | Topic | Case No. | Case Year | Parties | Bench | Order Date | A.F.R | Head Notes | Advocates. | Hon'ble Judge/Bench | Apex Court | Apex Status" — [SHC AJAX result](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search)
- Example row: "328773 | 1 | **2026 SHC KHI 2016** | | Criminal Appeal 556/2023 (D.B.) Sindh High Court, Karachi | 2023 | AURANGZEB S/O ZAHIR SHAH & ANOTHER (Appellant) VS THE STATE THROUGH ANF (Respondent) | D.B. | 26-OCT-26 | **Yes** | | Muhammad Farooq(ADVO-6839-SBC-KHI),Spl. Prosecutor Sindh (ANF)(SpPANF) | Hon'ble Mr. Justice Shamsuddin Abbasi(Author), Hon'ble Mr. Justice Miran Muhammad Shah." — same
- The "Judgement/Order" filter has "All, Judgment, Order, Adjournment/Short Order". There is an "AFR" checkbox. Other filters: case number, year, category (~120 case types), S.B./D.B./F.B., court/seat, party name, advocate (multi-select), topic/statute (multi-select, e.g. "Section 489-F, PPC(…Bail After Arrest---497)"), judge (single or multi), order date from/to, and case group ("Criminal Appellate Jurisdictions; Original Side; Civil Appellate Jurisdictions; Writ Jurisdictions; …") — [SHC Advance Search](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search)
- Home page entry: "Criminal Appeal 22/2026 (S.B.) Hassan Ali V/S The State Sindh High Court, Circuit Court, Mirpur Khas CITATION:2026 SHC MPK 1991, 2026 SHC MPK 2132 **SHC Citation: SHC-327917** Bench: Hon'ble Mr. Justice Nisar Ahmed Bhanbhro(Author) Source: http://shc.gov.pk/caselaw/ … Downloads 54 Order Date: 30-NOV-30 Approved for Reporting". Another entry shows a headnote-style summary: "Protective/Transitory Bail ??? Sections 5 and 23 of the Foreign Exchange Regulation Act, 1947…". The "???" are mis-encoded dashes in the source — [SHC Caselaw home](https://caselaw.shc.gov.pk/caselaw/public/home)
- Seat codes counted on the home page's "Latest Case Law (Approved For Reporting)" block: 2026 KHI 256, MPK 108, LAR 31, HYD 27, SUK 19; 2025 KHI 25, SUK 7, HYD 5, MPK 5, LAR 2; plus 2024 SUK 2 and 2020 HYD 1. These are occurrences of citation strings, not unique documents — same source
- Report-002 A.F.R. note: **"The Figures in the Following table only show the number of Judgments/Orders that attached staff of the Judges chosen to upload. It does not reflect the total disposal of the Hon'ble Judges."** Per-judge "Total / A.F.R." rows, for example: Chief Justice Zafar Ahmed Rajput 3738 / 128; Justice Adnan-ul-Karim Memon 9494 / 4340; Justice Agha Faisal 8500 / 465. My sums over the 34 listed sitting judges: Total 77,258; AFR 13,274 — [SHC Report-002](https://caselaw.shc.gov.pk/caselaw/public/rpt-afr)
- Report-005 note: "The figures in the following table only show the number of important Judgments/Orders uploaded on this site." It gives per-judge Judgement / Order splits, e.g. Chief Justice 191 / 3547; Justice Muhammad Iqbal Kalhoro 720 / 5567 — [SHC Report-005](https://caselaw.shc.gov.pk/caselaw/public/rpt-jo)
- The sample AFR search (Karachi, Criminal Appellate, AFR, Judgments, 01–31 Oct 2026) returned 6 rows, with document codes 326533–329549 — [SHC AJAX endpoint](https://caselaw.shc.gov.pk/caselaw/AJAX_PUBLIC.php)
- digital.shc.gov.pk "Search Citation" lists journals including "SHC, PLD, SCMR, CLC, PCr.LJ, PTD, PLC, CLD, YLR, … MLD, … PLJ, SLJ, SLR …" with fields Citation Year, Journal, Journal Part and Page No. The portal reports "17,441 Certified Copies Issued" and "27,777 Applications Entertained" across "Karachi (Principal Seat), Bench at Sukkur, Circuit Court Larkana, Circuit Court Mirpur Khas and Circuit Court Hyderabad" — [digital.shc.gov.pk](https://digital.shc.gov.pk/); [Search Citation](https://digital.shc.gov.pk/search-citation)

### Inferences
- **SHC neutral citation format:** `YYYY SHC {KHI|HYD|SUK|LAR|MPK} N`. Numbering appears to be per year and per seat. One item can carry two citations (e.g. "2026 SHC MPK 1991, 2026 SHC MPK 2132"), so the model must allow several citations per document. "SHC-{id}" matches the document code, an internal stable ID.
- The SHC corpus is much richer than LHC's for an AI product. It includes non-AFR orders, which are useful for procedural and bail patterns, and metadata (advocates, topics, apex status). The AFR flag gives a clean "reported" subset.
- Document codes near 329,549 suggest the database holds hundreds of thousands of records over all time, including former judges and adjournment orders. This is inferred from IDs and is not a stated count.
- Data-quality issues to handle: the "Order Date: 30-NOV-30" artefact, "???" encoding errors, and a broken Report001.

### Gaps
- The earliest year of coverage on caselaw.shc.gov.pk is not stated. I did not query old date ranges.
- Totals for former judges were not shown; Reports 002 and 005 list sitting judges only.
- No official notice was found on when the "SHC KHI/HYD/…" neutral citation was introduced (search: no result).

---

## 10. SHC: document format

### Takeaway
The sampled SHC judgment is a **born-digital, tagged PDF**, text-extractable, with numbered paragraphs and a standard caption. The neutral citation is not printed in the text. Headnotes, where present, live in the database "Head Notes" field, not in the PDF.

### Cited Findings
- View-file 328773 (Crl. Appeals 554–556/2023): "PDF document, version 1.5, 12 page(s)". It is a tagged PDF (`/Lang(en-US) /StructTreeRoot … /MarkInfo<</Marked true>>`). `pdftotext` extracted 4,565 words. The opening reads: "IN THE HIGH COURT OF SINDH AT KARACHI / PRESENT:- Mr. Justice Shamsuddin Abbasi / Mr. Justice Miran Muhammad Shah … Date of hearing 21.10.2026 / Date of Judgment 26.10.2026 … JUDGMENT / Shamsuddin Abbasi, J.- The instant three appeals arise out of …", followed by "2. The prosecution case …". The running header reads "Crl. Appeals 554, 555 & 556 of 2023 2". No "SHC KHI" string or "Approved for reporting" stamp was found in the text — [SHC view-file](https://caselaw.shc.gov.pk/caselaw/view-file/MzI4NzczY2Ztcy1kYzgz)

### Gaps
- Only one SHC PDF was sampled. Older or circuit-bench uploads, and "Adjournment/Short Order" items, may be scans.

---

## 11. SHC: search mechanics and programmatic feasibility

### Takeaway
Search is a jQuery **POST to `AJAX_PUBLIC.php`**. It returns JSON `{"Status":1,"msg":"<table…>"}` with the whole result table, which is paged client-side by DataTables. It needs **no login and no CAPTCHA**: the "Login/Sign Up" menu exists but search and view-file work anonymously. The site is fronted by **Cloudflare** (`Server: cloudflare`, `cf-cache-status: DYNAMIC`), which may challenge automated traffic at volume. The separate digital.shc.gov.pk citation search uses **Google reCAPTCHA v3** and must not be automated.

### Cited Findings
- search.js: `$.post("AJAX_PUBLIC.php",{STD_JUDGES, ALL_JUDGES_M_SELECT, ALL_ADVOCATES_M_SELECT, ALL_TOPICS_M_SELECT, STD_COURTS, CASENO, CASEYEAR, STD_CASETYPES, STD_BENCHTYPES, STD_DOCUMENTTYPES, AFR_TF, ADVOCATENAME, PARTYSIDE1_NAMES, TAGJUDGES, DATE_ORDER_JUDGMENT, DATE_ORDER_JUDGMENT2, CASEGROUP, opt:'search_judgement'}, "json")`, then `$("#pendency").html(obj.msg)` on `obj.Status == 1`, else `alert("No Record Found")`. Date format is `dd-M-yy` (e.g. 01-Oct-26). A second call `opt:'search_all_judges'` returns a JSON judge list — [search.js](https://caselaw.shc.gov.pk/caselaw/theme/js/search.js)
- The response came back in about 1.07 s with HTTP 200. The body was JSON with keys `Status`, `msg` (Content-Type text/html) — [AJAX_PUBLIC.php](https://caselaw.shc.gov.pk/caselaw/AJAX_PUBLIC.php)
- view-file returned `Content-Type: application/pdf` directly, with no session requirement beyond the cookie already held — [view-file](https://caselaw.shc.gov.pk/caselaw/view-file/MzI4NzczY2Ztcy1kYzgz)
- digital.shc.gov.pk/search-citation loads `https://www.google.com/recaptcha/api.js?render=6LeoZy4rAAAAAP2fu1pEuDwACu4yQwxk5nhLvrLf` — [Search Citation](https://digital.shc.gov.pk/search-citation)
- The Advance Search page is 1.22 MB, because it embeds full advocate, topic and judge option lists. Those lists double as useful controlled vocabularies — [SHC Advance Search](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search)

### Inferences
- Feasible without bypassing anything: slice requests by seat × month × document type (and optionally AFR), POST, parse the HTML table, then fetch the view-file PDFs. Keep request rates low to avoid Cloudflare bot mitigation. If a Cloudflare challenge appears, stop and seek permission rather than solving it.
- digital.shc.gov.pk citation lookup is out of scope for automation because of reCAPTCHA.

### Gaps
- No maximum result size was observed. It is unknown whether very broad queries are truncated.
- No documented API or bulk-data offer was found.

---

## 12. SHC: robots.txt and terms/copyright (permission to collect)

### Takeaway
caselaw.shc.gov.pk's robots.txt contains **only the Cloudflare "content signals" preamble, with no actual `Content-Signal:` line and no `User-agent`/`Disallow` rules**. By its own wording, that "neither grants nor restricts" search, ai-input or ai-train use. The SHC **Disclaimer** forbids copying or re-publishing the site "in whole or in part" without **written consent from the Registrar**. The main site's robots.txt disallows `/causelist/`.

### Cited Findings
- caselaw.shc.gov.pk/robots.txt is 24 lines, 1,248 bytes, served by Cloudflare. It contains only comments: "# As a condition of accessing this website, you agree to abide by the following content signals: (a) If a content-signal = yes, you may collect content for the corresponding use. (b) If a content-signal = no, you may not collect content for the corresponding use. (c) If the website operator does not include a content signal for a corresponding use, the website operator neither grants nor restricts permission via content signal with respect to the corresponding use. … search: … ai-input: inputting content into one or more AI models (e.g., retrieval augmented generation, grounding…) ai-train: training or fine-tuning AI models. ANY RESTRICTIONS EXPRESSED VIA CONTENT SIGNALS ARE EXPRESS RESERVATIONS OF RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION DIRECTIVE 2019/790…". There are **no directive lines** — [caselaw.shc.gov.pk/robots.txt](https://caselaw.shc.gov.pk/robots.txt). cases.shc.gov.pk/robots.txt is byte-identical — [cases.shc.gov.pk/robots.txt](https://cases.shc.gov.pk/robots.txt)
- sindhhighcourt.gov.pk/robots.txt: `User-agent: *` / `Disallow: /causelist/` — [SHC robots](https://sindhhighcourt.gov.pk/robots.txt)
- digital.shc.gov.pk/robots.txt: `User-agent: *` / `Disallow:` (everything allowed) — [digital robots](https://digital.shc.gov.pk/robots.txt)
- SHC Disclaimer: "This web site provides general information only. … You are responsible for obeying all applicable copyright laws. We permit you to make copies of this site as necessary incidental acts during your viewing of it; and you may take a print for your personal use of so much of the site as is reasonable for private purposes, but **you must not otherwise copy it, use it or re-publish it in whole or in part without this "Disclaimer" section nor without first obtaining written consent from the Registrar of this court (which consent may be refused without giving a reason).** © Sindh High Court: 2001-2002. All rights reserved, and all moral rights are asserted and reserved" — [SHC Disclaimer](https://sindhhighcourt.gov.pk/disclaimer.php)
- caselaw.shc.gov.pk footer: "© Copyright High Court of Sindh, Karachi | Powered by Sindh High Court,Karachi" — [SHC Advance Search](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search)

### Inferences
- robots.txt does not block collection from caselaw.shc.gov.pk, but the Disclaimer on the parent site is an express reservation requiring the Registrar's written consent for copying or re-use beyond personal viewing. It is dated 2001-02 and is arguably directed at the website, but it is the only terms document. As with LHC, **obtain written consent from the SHC Registrar** before building a production corpus. The Cloudflare content-signal framework means SHC could switch on `ai-train=no` or `ai-input=no` at any time. Re-check robots.txt before each harvest run.

### Gaps
- Not found: an SHC-specific open-data, re-use or API policy, or any statement that judgments are public domain.

---

## 13. SHC: cause lists (for hearing-date features)

### Takeaway
SHC cause lists are published as **PDFs under `/causelist/causelist_files/`, which robots.txt disallows**. They are also available as HTML through the case-flow apps on cases.shc.gov.pk (per seat: khi, hyd, suk, lar, mpkhas) and the SHC mobile apps.

### Cited Findings
- causelist.php links to PDFs such as `causelist/causelist_files/20-MAY-24.pdf`, `22-APR-24.pdf` and `30-SEP-24.pdf` (dated filenames, 2024). It also links to advocate cause lists: `https://cases.shc.gov.pk/khi/web/index.php?r=site/advocate-cause-list` (and `/hyd/`, `/suk/`, `/lar/`), plus `http://202.61.43.37:8081/nms/causelist.php`. The page note reads: "Advocates and litigants are advised to use Sindh High Court Mobile App (New Version) from play store (Android), Advance Case search, Advocate-Wise Search and Cause List for case information." — [SHC Cause List](https://sindhhighcourt.gov.pk/causelist.php)
- Other links: `https://cases.shc.gov.pk/khi/web/index.php?r=ocp/index` (and hyd, suk, lar), `https://cases.shc.gov.pk/mpkhas/web`, an iOS app `https://apps.apple.com/us/app/shc-case-flow-management/id6766609633`, and district courts at `https://cases.districtcourtssindh.gos.pk/causelist` — [SHC home](https://sindhhighcourt.gov.pk/)

### Inferences
- Do not crawl `/causelist/` PDFs (robots disallow). For hearing dates, use cases.shc.gov.pk HTML views, which have no disallow but carry the same Disclaimer caveat. Better still, seek an agreed feed.

### Gaps
- I did not fetch the cases.shc.gov.pk cause-list views, so their format is unverified.

---

## 14. SHC: digitisation / e-court / AI initiatives (dated)

### Takeaway
SHC is the more active of the two courts. Its "E-Courts Vision 2030 – Go Green" programme (launched Sept 2025) includes instant upload of orders and judgments. In May 2026 it launched an **internal AI legal-research tool ("LRC-Assistant")** and an iOS CFMS app. Neither is a public or open-judgment API.

### Cited Findings
- 11 Sep 2025 [secondary]: SHC CJ Muhammad Junaid Ghaffar inaugurated projects under "E-Courts Vision 2030 — Go Green". They include online filing, e-certified true copies for pending and decided cases, e-kiosks, paperless courtrooms, and orders and judgments "uploaded instantly". The online payment and issuance facility was "in the pipeline" — [Dawn](https://www.dawn.com/news/1941060/shc-chief-justice-inaugurates-project-to-digitise-judicial-process)
- 17 May 2026 [secondary]: SHC launched "LRC-Assistant", an AI search engine "designed to assist high court judges and research officers". It uses "trained machine learning models and indexed judicial data repositories" and enables "advanced query-based retrieval of judgments and orders". SHC also launched an iOS CFMS app with cause lists and case schedules. Both were built in-house — [The News](https://www.thenews.pk/print/1415951-shc-launches-ai-enabled-search-engine-mobile-app)
- digital.shc.gov.pk is branded "Digital Copy/CaseLaw e-Courts Project Vision 2030 Go-Green" and offers eCTC, "Copy Ready" and "Search Citation" — [digital.shc.gov.pk](https://digital.shc.gov.pk/)
- SHC Press Release May 2026 [snippet-only]: https://sindhhighcourt.gov.pk/news_notifications/source_files/Press_Release/SHC_Press_Release_may_2026.pdf

### Gaps
- The press release PDF was not fetched, so the exact official wording of the May 2026 launch is unverified.
- No neutral-citation or open-data policy announcement was found for SHC, LHC, or the LJCP/NJPMC. The search found only NJPMC harmonisation items (July 2025) with no citation content.

---

## 15. Cross-court analysis (for the corpus build)

### Takeaway
Both courts publish born-digital, text-extractable official PDFs at stable URLs, with their own neutral citations, and both can be collected technically without bypassing any control. **Both reserve rights**: LHC through "should not be downloaded without prior agreement", SHC through "written consent from the Registrar". Formal permission requests are therefore the gating item, LHC first.

### Inferences
- **LHC (priority):** corpus = AFR only, 2010→present, roughly 700–800 a year recently. Harvest metadata from 2 endpoints × years. Key the PDF by `{YYYY}LHC{N}`. Capture the "LHC Citation", "Other Citations" (reporter cross-refs useful for citation resolution) and "Tag Line" from the listing, because the PDF lacks them. Bench is not structured, so derive it from the PDF caption or reporter strings.
- **SHC:** corpus = judgments plus orders (≈77k for sitting judges alone), with an AFR flag, seat-coded neutral citations (with possible multiples), and rich metadata. Harvest via the POST endpoint sliced by seat and date. Key by document code. Exclude cause-list PDFs (robots).
- Manifest check: the hosts `caselaw.shc.gov.pk`, `lhc.gov.pk` and `data.lhc.gov.pk` are confirmed official. **Add `sys.lhc.gov.pk`** (the PDF host). The `https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search` URL is correct and live. Consider `digital.shc.gov.pk` as official but CAPTCHA-protected, and do not automate it. Treat raw-IP SHC hosts as official-but-legacy and avoid them.
- Suggested action: send formal permission letters to the LHC Registrar or Director (IT) and to the SHC Registrar. Cite the footer and Disclaimer language, describe the purpose (attribution, link-back, no alteration), and request a bulk feed or API if available.

### Gaps
- Legal status of judgments under Pakistani copyright law, and whether website notices bind the judgments themselves (outside this note's scope; see copyright_open_data_landscape.md).
- Whether either court will offer a bulk or API arrangement. No public statement was found.
