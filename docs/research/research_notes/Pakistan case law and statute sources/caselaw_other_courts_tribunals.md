# Official judgment/decision publishing: PHC, BHC, GB courts, AJK courts and key federal tribunals

Research date: 12 November 2026. Unless marked otherwise, every page below was fetched directly by HTTP on that date (curl or WebFetch), and the facts were taken from the raw HTML or PDF bytes. "Snippet only" means the item was seen only in a search-engine result. No CAPTCHA, login or rate limit was bypassed. One attempted direct call to the BHC portal's JSON API was stopped (see BHC), and BHC judgment PDFs were not downloaded because robots.txt disallows the folder they sit in.

Method notes for the report writer:
- Sample PDFs were checked with `pdftotext -layout`. I counted non-whitespace characters, and searched the raw bytes for `/Subtype /Image` objects and `/Producer`/`/Creator` strings.
- "Scanned" means one image object per page and no usable text. "Scanned + OCR" means one image per page plus an invisible text layer, typical of copier or scanner OCR.
- Counts come from parsing the official listing pages on the research date.

## Source inventory

| Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| PHC home page | https://peshawarhighcourt.gov.pk/app/site/ | Peshawar High Court | Official court site | Footer "2010-2026"; shows judgments dated Oct-Nov 2026 | Primary | Fetched (200) |
| PHC Reported Judgments search | https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php | PHC | Official judgment database | Records to 2026 | Primary | Fetched (200); POST search run for 2025 and for "All Years" |
| PHC "All the Referred, Reported Judgments" | https://peshawarhighcourt.gov.pk/app/site/47/c/All_the_Referred,Reported_Judgments.html | PHC | Redirect page | n/a | Primary | Fetched (200) |
| PHC "Case Law" publications | https://peshawarhighcourt.gov.pk/app/site/108/c/Case_Law.html | PHC | Case-law digest PDFs | Latest issue listed: Vol-4 Issue-I Jan-Mar 2023 | Primary | Fetched (200) |
| PHC robots.txt | https://peshawarhighcourt.gov.pk/robots.txt | PHC | robots | n/a | Primary | Fetched: 200, but the body is a JS redirect to `app/site/`, not a robots file |
| BHC home page | https://bhc.gov.pk/ | High Court of Balochistan | Official court site | "© 2026" | Primary | Fetched (200) |
| BHC Judgments (per-judge index) | https://bhc.gov.pk/resources/judgments | BHC | Official judgment listing | 2026 | Primary | Fetched (200), plus the per-judge sub-pages |
| BHC portal judgments (SPA) | https://portal.bhc.gov.pk/judgments | BHC | Judgment search app (Nuxt) | n/a | Primary | Fetched the app shell and JS bundles. A direct call to its API `https://api.bhc.gov.pk/v2/judgments` returned 302 to `/login` and was not pursued |
| BHC robots.txt | https://bhc.gov.pk/robots.txt | BHC | robots | n/a | Primary | Fetched (200) |
| api.bhc.gov.pk robots.txt | https://api.bhc.gov.pk/robots.txt | BHC | robots | n/a | Primary | Fetched (200) |
| GB Chief Court home | https://gbcc.gov.pk/index.aspx | Chief Court Gilgit-Baltistan | Official court site | n/a | Primary | Fetched (200) |
| GBCC Reported Judgments | https://gbcc.gov.pk/ReportedJudgments.aspx | GBCC | Judgment search (ASP.NET WebForms) | Decision dates listed 2015-2020 | Primary | Fetched (200); two form postbacks run |
| GBCC robots.txt | https://gbcc.gov.pk/robots.txt | GBCC | robots | n/a | Primary | 404 |
| SAC GB Judgments | https://sacgb.gov.pk/Judgments.html | Supreme Appellate Court GB | Static judgment list | "Copyright © 2025"; entries to 2025 case numbers | Primary | Fetched (200) |
| SAC GB Latest Judgements | https://sacgb.gov.pk/Latest%20Judgements.html | SAC GB | Static list | Uploads dated Nov 2022 | Primary | Fetched (200) |
| SAC GB robots.txt | https://sacgb.gov.pk/robots.txt | SAC GB | robots | n/a | Primary | 404 |
| AJK High Court judgments | https://ajkhighcourt.gok.pk/important-judgments (alias https://ajkhighcourt.gok.pk/Userside/Judgement) | High Court of AJ&K | Judgment search | Footer "Copy Right @ 2017-2025"; records 2022-2026 | Primary | Fetched (200); POST searches run. Note: https://ajkhighcourt.gok.pk/judgements returns 404 |
| AJK HC robots.txt | https://ajkhighcourt.gok.pk/robots.txt | AJK HC | robots | n/a | Primary | 404 |
| AJK Supreme Court Judgements/Orders | https://ajksupremecourt.gok.pk/judgements-orders/ | Supreme Court of AJ&K | WordPress listing | Latest post 28-10-2026 | Primary | Fetched. **HTTP 500**: the content renders, then the page ends with "There has been a critical error on this website." |
| AJK SC WP REST API | https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts , /wp-json/wp/v2/categories | AJK SC | Public WordPress JSON | Live | Primary | Fetched (200) |
| AJK SC robots.txt + sitemap | https://ajksupremecourt.gok.pk/robots.txt ; https://ajksupremecourt.gok.pk/sitemap.xml | AJK SC | robots / sitemap | sitemap lastmod 2025-09-01 | Primary | Fetched (200) |
| FST site | https://fst.gov.pk/ , https://www.fst.gov.pk/ | Federal Service Tribunal | Official site | Live site: "Account Suspended" (12 Nov 2026) | Primary | curl: TLS handshake failed (schannel SEC_E_UNSUPPORTED_FUNCTION). HTTP 301 redirects to https. WebFetch returned an "Account Suspended" hosting page |
| FST Wayback snapshot | http://web.archive.org/web/20260716134606/https://fst.gov.pk/ | Internet Archive copy of FST | Archived official site | 16 Jul 2026 | Secondary copy of a primary page | Fetched (200) |
| FST Report 2017-2018 | https://fst.gov.pk/fst-panel/uploads/forms/file_1543921561.pdf | FST | Annual report | 2018 | Primary | Snippet only |
| ATIR site, Judgements page | https://atir.gov.pk/Judgements | Appellate Tribunal Inland Revenue | Tribunal site | Footer "© 2023" | Primary (but see notes on provenance) | Fetched (200): "No Record Found In Database" |
| ATIR Wayback snapshot | http://web.archive.org/web/20260118080836/https://atir.gov.pk/Judgements/ | Internet Archive | Archived page | 18 Jan 2026 | Secondary copy | Fetched (200): same "No Record Found" |
| ATIR robots.txt | https://atir.gov.pk/robots.txt | ATIR | robots | n/a | Primary | Returns the HTML home page (200), not a robots file |
| CCP Orders | https://cc.gov.pk/home/orders | Competition Commission of Pakistan | Orders listing | Latest order 11 Sep 2026 | Primary | Fetched (200) |
| CAT orders (hosted by CCP) | https://cc.gov.pk/home/decidedcatcases (+ _section3, _section4, _section10, _section39) | CCP / Competition Appellate Tribunal | Tribunal orders listing | Latest CAT order 06-07-2026 | Primary (CCP-hosted) | Fetched (200) |
| CCP robots.txt | https://www.cc.gov.pk/robots.txt ; http://appadminccp.cc.gov.pk/robots.txt | CCP | robots | n/a | Primary | 404 on both |
| FTO Reported/Latest Decisions | https://www.fto.gov.pk/decisions.aspx | Federal Tax Ombudsman | Selected decisions | 2022-2026 | Primary | Fetched (200) |
| FTO "Signed Decisions" (rolling 15 days) | http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions | FTO (linked from the FTO menu as "Latest Decisions") | All signed findings, 15-day window | 29/10/2026-12/11/2026 | Primary (third-party DNS host; see analysis) | Fetched (200) |
| FTO robots.txt | https://fto.gov.pk/robots.txt ; http://ftocmis.fto.gov.pk/robots.txt ; http://onlinecomplaints.cloudns.asia:4041/robots.txt | FTO | robots | n/a | Primary | All 404 |
| Wafaqi Mohtasib "Findings" | https://mohtasib.gov.pk/Publications | Wafaqi Mohtasib (Federal Ombudsman) | Selected findings | Newest 18/12/2020 | Primary | Fetched (200) |
| Wafaqi Mohtasib robots.txt | https://mohtasib.gov.pk/robots.txt | WMS | robots | n/a | Primary | 404 |
| LJCP Administrative Tribunals & Special Courts report 2024 | https://ljcp.gov.pk/SiteImage/Misc/files/ATSC%202024%20(20-06-25).pdf | Law & Justice Commission of Pakistan | Statistical report | 20-06-2025 | Primary | Snippet only |
| MoLaw ATIR page | https://molaw.gov.pk/Detail/Nzc3YzZmMmUtNTI2NS00NTIwLWIzNWQtNzA5MmI3MDU5MDAz | Law & Justice Division | Ministry page on ATIR | n/a | Primary | Snippet only |
| Customs Today: MTBA launches appeal management software at ATIR | https://customstoday.media/mtba-launches-appeal-management-software-at-atir/ | Trade press | News | undated in snippet | Secondary | Snippet only |
| pakcaselaw.duckdns.org | https://pakcaselaw.duckdns.org/browse/court/competition-appellate-tribunal | Unofficial aggregator | Third-party | n/a | Low (unofficial) | Snippet only; listed only so it can be excluded |

---

## Q1. Official websites and exact judgment/decision URLs (verified)

### Takeaway
Every body in scope has an official site. As of 12 Nov 2026, fetchable decision listings existed for:
- PHC, BHC, GBCC, SAC GB, AJK HC and AJK SC
- CCP and CAT (both on cc.gov.pk)
- FTO
- Wafaqi Mohtasib (stale since 2020)

Two bodies publish no decisions:
- **ATIR's page is empty** ("No Record Found In Database").
- **FST's site is suspended**. Even its July 2026 archived version had no judgments section.

### Cited Findings

**Peshawar High Court (PHC), including the Mingora, Abbottabad, Bannu and D.I. Khan benches**
- The main judgment database is `https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php`. Its HTML form posts to `reportedJudgments.php?action=search` with these fields:
  - `year`: 0 = All Years, or 2010-2026
  - `judge`: id
  - `category`: 0 = All, 1 Criminal, 2 Civil, 3 Revenu, 4 Constitutional, 5 Service, 6 Corporate
  - `txtsearchbyremarks`: free-text search on the remarks
  - Source: [PHC Reported Judgment](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php)
- The PHC home page links to that database ("All the Referred, Reported Judgments", plus "Reported Judgments of Former Chief Justices" and "Reported Judgments of Retired Judges"). It also shows a "Recent Judgments" strip with direct PDF links, for example `https://peshawarhighcourt.gov.pk/PHCCMS/judgments/WP-No.6226-P-of-2026-Ayesha-Jameel-etc-vs.pdf` — [PHC home](https://peshawarhighcourt.gov.pk/app/site/)
- The benches have no separate judgment sites. One database holds every bench. In case numbers, the suffix -P is Peshawar, -M Mingora, -A Abbottabad, -B Bannu and -D D.I. Khan. My "All Years" pull split as follows:
  - P: 2,283
  - M: 967
  - A: 808
  - B: 692
  - D: 404
  - no parseable suffix: 795
  - Source: [PHC Reported Judgment search, All Years](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search)
- PHC also publishes a quarterly "Case Law" digest as PDFs. The newest issue listed is "Case Law Vol-4 Issue-I Jan-Mar(2023)", and the first is "Case_Law_Vol-1_Issue-I_Oct-Dec(2020)" at `/image_bank/Publications/Case_Law/Case_Law_Vol_1_Issue_I.pdf` — [PHC Case Law](https://peshawarhighcourt.gov.pk/app/site/108/c/Case_Law.html)

**High Court of Balochistan (BHC), including the Sibi, Turbat, Loralai and Khuzdar benches**
- The judgment index is `https://bhc.gov.pk/resources/judgments`. It links 24 judges × 2 lists (48 pages) with the pattern `https://bhc.gov.pk/resources/judgments/<judge-slug>/reported-judgments` and `/significant-judgments` — [BHC Judgments](https://bhc.gov.pk/resources/judgments)
- Each entry has the case title, a law-report citation and a "View Judgment" link with the pattern `data-src="https://bhc.gov.pk/media/judgments/<numeric id>.pdf"`. Example: "Zainullah V. Hizbullah and others, PLD 2022 Balochistan 81" → `https://bhc.gov.pk/media/judgments/1333.pdf` — [BHC, Justice Abdul Hameed Baloch, Reported Judgments](https://bhc.gov.pk/resources/judgments/justice-abdul-hameed-baloch/reported-judgments)
- The home page also links a separate "Judgments" search at `https://portal.bhc.gov.pk/judgments` — [BHC home](https://bhc.gov.pk/)
  - It is a Nuxt single-page app. Its JS bundle posts JSON to `https://api.bhc.gov.pk/v2/judgments` with fields `searchBy` (Case Id / Case Info / Judge), `caseId`, `caseNumber`, `caseYear`, `courtId` (bench), `categoryId`, `judgeId`, `sDate` and `eDate` (default: the last 30 days).
  - Downloads go through `/v2/downloadpdf/<a>/<b>.<ext>` — [portal.bhc.gov.pk JS chunk bb8c782.js](https://portal.bhc.gov.pk/_nuxt/bb8c782.js)

**Chief Court Gilgit-Baltistan (GBCC)**
- The judgment page is `https://gbcc.gov.pk/ReportedJudgments.aspx`, titled "Reported Judgments & Orders – Search Precedents, Landmark Judgments, and Judicial Determinations of Chief Court" — [GBCC Reported Judgments](https://gbcc.gov.pk/ReportedJudgments.aspx)
  - Filters: free text (case number, bench, parties or citation), a bench dropdown and a "Decision Year" dropdown.
  - The dropdown actually lists 17 specific decision dates, from 2015-06-26 to 2020-10-01.
  - Result columns: Sr #, CASE NO, RESPECTED BENCH, AUTHOR JUDGE, PARTIES, CITATION, DOCUMENT.
- Each "View PDF" button is an ASP.NET postback. It returns a 302 to a static file under `/attach/judgements/`, for example `https://gbcc.gov.pk/attach/judgements/file-a2ecbae7-848c-4c86-b758-6d2b953fb05221052022135836.pdf` (case C.Rev 55-2018, Ali Dad vs Muhammad Hussain etc, "Citation Awaited") — [GBCC Reported Judgments postback](https://gbcc.gov.pk/ReportedJudgments.aspx)

**Supreme Appellate Court Gilgit-Baltistan (SAC GB)**
- The main list is a single static page, `https://sacgb.gov.pk/Judgments.html`, with one column ("Case Title") and about 757 rows. PDFs sit in four folders:
  - `Judgments/`: about 612 + 73
  - `Judgments/judgements-2021/`: 54
  - `Judgments/judgements2022-2026/`: 17
  - Example: `Judgments/judgements2022-2026/Umer Farooq Vs The State.pdf` (Cr. Appeal No.03/2024)
  - Source: [SAC GB Judgments](https://sacgb.gov.pk/Judgments.html)
- The "Latest Judgements" page lists 2 items. Its columns are Case Subject, Case No., Case Title, Author Judge, Judgment Date, Upload Date and Download; both items were uploaded in November 2022. It says "For more judgements, CLICK HERE to use judgement search", but the link points back to Judgments.html — [SAC GB Latest Judgements](https://sacgb.gov.pk/Latest%20Judgements.html)

**High Court of Azad Jammu & Kashmir (AJK HC)**
- The judgment search is at `https://ajkhighcourt.gok.pk/important-judgments`; `/Userside/Judgement` returns the same page. `https://ajkhighcourt.gok.pk/judgements` returns 404 — [AJK HC Judgments](https://ajkhighcourt.gok.pk/important-judgments)
- The form posts the same URL with these fields:
  - `judgment_tab` = judgment | previous ("Showing active judges." / "Showing previous judges.")
  - `cmbYear` = ALL or 1950-2026
  - `cmbBench` = ALL or judge ids 16-19
  - `cmbCategory` = ALL, Civil, Constitutional, Corporate, Criminal, Family, Revenu, Service, Writ Petition
  - `btnSearchJudgment`
- Result columns: S.No., Case Title, Category, Decision Date, Judgment (a "View" link to `https://ajkhighcourt.gok.pk/judgment_files/<name>.pdf`). Source: [AJK HC Judgments POST](https://ajkhighcourt.gok.pk/important-judgments)

**Supreme Court of Azad Jammu & Kashmir (AJK SC)**
- The listing is `https://ajksupremecourt.gok.pk/judgements-orders/`, titled "Important Judgements Of AJK Supreme Court", with a keyword filter and pagination. Each entry links to a WordPress post, for example `https://ajksupremecourt.gok.pk/pakistan-telecommunication-authority-vs-m-s-telenor-pakistan-pvt-limited/` (Civil Appeal No. 273 of 2023, 28-10-2026).
- The page returned **HTTP 500**, with the WordPress message "There has been a critical error on this website." after the content — [AJK SC Judgements/Orders](https://ajksupremecourt.gok.pk/judgements-orders/)
- The public WordPress REST API reports category id 18 "Judgments" with count 704, and `X-WP-Total: 886` posts in all — [AJK SC WP REST categories](https://ajksupremecourt.gok.pk/wp-json/wp/v2/categories?per_page=50); [WP REST posts](https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts?per_page=1)

**Federal Service Tribunal (FST)**
- Live status:
  - `https://fst.gov.pk/` and `https://www.fst.gov.pk/` failed the TLS handshake from curl/schannel.
  - Over HTTP, `http://fst.gov.pk/` returns 301 to https, and `http://www.fst.gov.pk/judgments` returns 301 to `https://www.fst.gov.pk/judgments`.
  - WebFetch of `https://www.fst.gov.pk/robots.txt` returned: "Account Suspended. This Account has been suspended. Contact your hosting provider for more information." The https home page gave a similar page with only a mailto link to webmaster@fst.gov.pk.
  - Source: [FST](https://fst.gov.pk/)
- The archived home page from 16 Jul 2026 has no judgments link. Its menu has Home, About Us, Honourable Members, Administration, Tenders, Gallery, News, Contact Us, and "Case Management System: Cause List, Online Cause List, Online Case Status". Its footer reads "2023 © All Rights Reserved by COMSATS Internet Services" — [Wayback, fst.gov.pk 2026-07-16](http://web.archive.org/web/20260716134606/https://fst.gov.pk/)
- The Wayback availability API has no snapshot of `fst.gov.pk/judgments` — [archive.org availability API](http://archive.org/wayback/available?url=fst.gov.pk/judgments)
- (Snippet only; older) The FST Report 2017-2018 says the tribunal launched a website and that "important judgments and press releases are also placed on the website" — [FST Report 2017-2018](https://fst.gov.pk/fst-panel/uploads/forms/file_1543921561.pdf)

**Appellate Tribunal Inland Revenue (ATIR)**
- `https://atir.gov.pk/Judgements` shows a heading "Judgments" and then "No Record Found In Database". The page credits private donors (Naeem Law Associates, several FCAs, and the MTBA and RITBA bar presidents) for "the successful establishment of this website". It also reads "Built at Ujjan.com" and "© 2023 - Appellate Tribunal Inland Revenue" — [ATIR Judgements](https://atir.gov.pk/Judgements)
- The archived copy from 18 Jan 2026 shows the same "No Record Found In Database" — [Wayback ATIR Judgements 2026-01-18](http://web.archive.org/web/20260118080836/https://atir.gov.pk/Judgements/)

**Competition Commission of Pakistan (CCP) and Competition Appellate Tribunal (CAT)**
- The CCP orders page is `https://cc.gov.pk/home/orders`. Columns: Sr. No, Title, Order Date, Nature of Violation, View Detail (`https://cc.gov.pk/home/vieworders/<id>`), and Download Order (Pdf), which links to `http://appadminccp.cc.gov.pk/ccporders/<32-hex>.pdf`.
  - There are 177 unique order PDFs and 177 vieworders ids.
  - The newest is "Show Cause Notice issued to M/s All Pakistan Edible Oil Tankers Owners Association", 11 Sep 2026.
  - Source: [CCP Orders](https://cc.gov.pk/home/orders)
- CAT orders are hosted by CCP at `https://cc.gov.pk/home/decidedcatcases`, titled "Tribunal Orders - All Order By the Competition Appellate Tribunal".
  - Columns: CCP order Title, CCP order Date, Appeal No, CAT order Title, CAT order Date, CAT order (Pdf), linking to `http://appadminccp.cc.gov.pk/catorders/<human filename>.pdf`.
  - There are 87 unique PDFs. The newest is "British Lyceum Vs CCP", 06-07-2026.
  - Sub-pages by statute section: `_section3` (3 PDFs), `_section4` (15), `_section10` (36), `_section39` (0). All of these are included in the 87.
  - Source: [CCP – CAT orders](https://cc.gov.pk/home/decidedcatcases)
- No standalone official CAT website was found. The search surfaced only CCP pages and press — [web search, 12 Nov 2026](https://cc.gov.pk/home/decidedcatcases_section4)

**Federal Tax Ombudsman (FTO)**
- `https://www.fto.gov.pk/decisions.aspx` is labelled "Reported Decisions" in the menu and "Latest Decisions" on the page. It introduces "Some important cases, where after investigation and research studies recommendations were made to FBR".
  - It lists 245 rows (Complaint No, Download).
  - PDFs are at `https://www.fto.gov.pk/assets/decisions/<complaint>_<year>.pdf`, for example `assets/decisions/11887_2026.pdf` and `review_14817_2026.pdf`.
  - Source: [FTO decisions](https://www.fto.gov.pk/decisions.aspx)
- The FTO menu item "Latest Decisions" opens `http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions`, headed "Signed Decisions -:Findings Signed By Hon'ble FTO:-". The page says: "For the convenience of taxpayers and the general public, the Hon'ble Federal Tax Ombudsman has made all its decisions available online, which will remain accessible on the official FTO website for a period of 15 days."
  - It listed 647 rows dated 29/10/2026 to 12/11/2026.
  - PDFs are at `http://ftocmis.fto.gov.pk/DataRepository/SIGNEDFINDINGS_<yyyymmddhhmmssfff>.PDF`.
  - Source: [FTO Signed Decisions](http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions)

**Wafaqi Mohtasib (Federal Ombudsman Secretariat)**
- The "Findings" menu item opens `https://mohtasib.gov.pk/Publications`. It has 13 rows (Title, StartDate, Download) linking to `/SiteImage/Publication/<name>.pdf`.
  - Dates run from 23/11/2017 to 18/12/2020, for example "WMS-ONL/0009161/20 Christian Marriage Registration Certificate 18/12/2020" → `/SiteImage/Publication/finding_onl_9161_20.pdf`.
  - Source: [Wafaqi Mohtasib Findings](https://mohtasib.gov.pk/Publications)
- The rest of the site publishes annual reports, for example `SiteImage/Downloads/WMS Annual Report 2025_compressed.pdf`, plus special studies. Its complaint tracking runs on `complaints.mohtasib.gov.pk` — [Wafaqi Mohtasib home](https://mohtasib.gov.pk/)

**Banking courts, consumer courts, environmental tribunals**
- No official online judgment repository was found for these. The search surfaced only the LJCP's statistical "Administrative Tribunals and Special Courts" reports (ATSC 2023 and 2024) and Law Ministry descriptions — [LJCP ATSC 2024 (snippet)](https://ljcp.gov.pk/SiteImage/Misc/files/ATSC%202024%20(20-06-25).pdf); [MoLaw Annex I (snippet)](https://molaw.gov.pk/SiteImage/Misc/files/Annex-I.pdf)
- Decisions from these forums do appear on the unofficial aggregator pakcaselaw.duckdns.org (snippet only). It is not an official source — [pakcaselaw (snippet)](https://pakcaselaw.duckdns.org/browse)

### Inferences
- For PHC and the AJK HC, the database is the authoritative list. Each bench is a filter (or a case-number suffix), not a separate source.
- BHC has two official channels: static per-judge pages, which carry only reported or significant judgments, and the portal search app. Their coverage likely differs. The portal may include unreported judgments, but this was not verified.
- CAT has no website of its own. CCP's pages are the only official online copy of CAT orders found.
- The FTO's "all decisions" feed is a 15-day rolling window. A complete FTO corpus is therefore only possible by collecting continuously from now on. Back-years would have to come from the 245 curated decisions plus whatever annual reports contain.

### Gaps
- No standalone official website was found for the Competition Appellate Tribunal. Whether CAT itself keeps one is unresolved.
- The official status of `atir.gov.pk` is not confirmed by a government source. It credits private donors and an outside developer. The Law Ministry has an ATIR page (snippet only, not fetched).
- No provincial Environmental Protection Tribunal, consumer court or banking court site with published decisions was found. This search was shallow (one query plus LJCP snippets).
- I could not tell whether the FST's suspension is temporary, nor confirm any alternative FST domain.

---

## Q2. What is published, years covered, approximate counts, languages

### Takeaway
- **PHC** is by far the largest: 5,949 reported or referred judgments, 2009-2026, about 1,103 carrying a PHC neutral citation.
- **BHC**'s static pages hold about 2,001 reported or significant judgments (citation years 2010-2026), at PDF ids 1-2004.
- **SAC GB** has about 757 judgments, mostly from cases of 2009-2018.
- **AJK SC** has 704 judgment posts since January 2016.
- **FTO** has 245 curated decisions (2022-2026) plus about 650 signed findings in the rolling 15-day window.
- **AJK HC** has about 264 judgments, 2022-2026.
- **CCP** has 177 orders (2007-2026) and **CAT** 87 orders.
- **GBCC** is tiny: 17 decision dates, 2015-2020.
- **Wafaqi Mohtasib** has 13 findings, 2017-2020.
- **ATIR and FST**: none.

Nearly everything is English. The AJK HC bench names are in Urdu.

### Cited Findings
- **PHC**, "All Years" search (12 Nov 2026):
  - 5,949 records, of which 5,935 have a judgment PDF (5,885 unique URLs).
  - By decision year: 2009: 15; 2010: 97; 2011: 119; 2012: 246; 2013: 266; 2014: 298; 2015: 527; 2016: 322; 2017: 539; 2018: 350; 2019: 317; 2020: 314; 2021: 268; 2022: 485; 2023: 425; 2024: 258; 2025: 730; 2026: 373.
  - By category: Criminal 2,438; Civil 1,733; Constitutional 1,291; Service 309; Revenu 128; Corporate 50.
  - Columns: S.No, Case, Remarks (a headnote-like summary), Other Citation (for example "2025 CLC 1482 Pesh", or "awaited"), PHC Neutral Citation (for example "2025 PHC 14"; 1,103 records have one), Decision Date, S.C.Status (upheld / set aside / Pending), Category, Judgment (PDF), SC Judgment (PDF; 278 records link the Supreme Court judgment).
  - Source: [PHC Reported Judgment search](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search)
  - 2025 alone gave 727 neutral citations, numbered up to "2025 PHC 9015", with decision dates from 13-01-2025 to 24-12-2025. The numbers are clearly not consecutive within the published set, so only a selection of numbered judgments is listed — [PHC search, year=2025](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search)
- **BHC**: the static pages carry only "Reported Judgments" and "Significant Judgments" per judge, each with a law-report citation such as "PLD 2022 Balochistan 81" — [BHC reported judgments, Justice Abdul Hameed Baloch](https://bhc.gov.pk/resources/judgments/justice-abdul-hameed-baloch/reported-judgments). I fetched all 48 per-judge pages politely (1 s delay) on 12 Nov 2026:
  - 1,959 "Reported Judgments" entries and 42 "Significant Judgments" entries.
  - 2,001 unique PDF ids, spanning `/media/judgments/1.pdf` to `/media/judgments/2004.pdf`.
  - By citation year (reported list): 2010: 88; 2011: 114; 2012: 175; 2013: 70; 2014: 68; 2015: 100; 2016: 58; 2017: 136; 2018: 161; 2019: 99; 2020: 167; 2021: 133; 2022: 116; 2023: 164; 2024: 140; 2025: 151; 2026: 19.
  - Largest lists: Justice Rozi Khan Barach (253), Justice Abdullah Baloch (231), Justice Muhammad Hashim Kakar (177).
  - Source: [BHC Judgments index and per-judge pages](https://bhc.gov.pk/resources/judgments)
- **GBCC**: the decision-date dropdown has 17 values (2015-06-26 … 2020-10-01). A search on 2018-10-17 returned a single row (Sr # 12, C.Rev 55-2018, "Citation Awaited") — [GBCC Reported Judgments](https://gbcc.gov.pk/ReportedJudgments.aspx)
- **SAC GB**: about 757 rows and 753 unique PDF links.
  - By case-number year: 2007: 2; 2008: 3; 2009: 36; 2010: 42; 2011: 35; 2012: 14; 2013: 21; 2014: 43; 2015: 102; 2016: 127; 2017: 136; 2018: 55; 2019: 23; 2020: 16; 2023: 9; 2024: 5; 2025: 1.
  - The list carries no judgment dates.
  - Source: [SAC GB Judgments](https://sacgb.gov.pk/Judgments.html)
- **AJK HC**:
  - "Judgments" tab (active judges), all years: 220 PDF links / about 221 rows. By decision year: 2022: 19; 2023: 78; 2024: 81; 2025: 26; 2026: 17.
  - "Previous Judgments" tab: 43 PDFs. By year: 2022: 6; 2023: 20; 2024: 12; 2025: 5.
  - The year dropdown offers 1950-2026, but results only start in 2022.
  - Source: [AJK HC Judgments](https://ajkhighcourt.gok.pk/important-judgments)
- **AJK SC**: the category "Judgments" holds 704 posts. The oldest are dated 2016-01-14 ("Azad Govt. & others VS Sardar M. Mukhtar Khan"). The newest is 28-10-2026 (PTA vs Telenor, Civil Appeal 273/2023). Also listed: "Presidential Reference No. 01 of 2026" (23-09-2026) — [AJK SC WP REST, category 18](https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts?categories=18&per_page=3&order=asc); [AJK SC Judgements/Orders](https://ajksupremecourt.gok.pk/judgements-orders/)
- **CCP**: 177 orders. Years in the listing run from 2007 (CCP was set up under the 2007 Ordinance) to 2026. "Nature of Violation" tags include "Price Fixation / Cartelization" and "Deceptive Marketing Practices" — [CCP Orders](https://cc.gov.pk/home/orders)
- **CAT**: 87 order PDFs. Each is paired with the underlying CCP order and appeal number (for example "41/2025 British Lyceum Vs CCP 06-07-2026") — [CCP – CAT orders](https://cc.gov.pk/home/decidedcatcases)
- **FTO**:
  - Curated decisions: 245. By complaint year: 2022: 37; 2023: 117; 2024: 41; 2025: 30; 2026: 26. One "own motion" item, `0020_om_2022.pdf`, returned 404 when downloaded — [FTO decisions](https://www.fto.gov.pk/decisions.aspx)
  - Rolling feed: 647 signed findings dated 29/10/2026-12/11/2026 (Oct: 186; Nov: 461) — [FTO Signed Decisions](http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions)
- **Wafaqi Mohtasib**: 13 findings, 23/11/2017-18/12/2020. They include "Representations filed by SUI Northern gas pipelines limited against the findings of the Wafaqi Mohtasib" (22/10/2020) — [WMS Findings](https://mohtasib.gov.pk/Publications)
- **ATIR**: 0 ("No Record Found In Database") — [ATIR Judgements](https://atir.gov.pk/Judgements)
- **FST**: 0 found. The live site is suspended, and the July 2026 archived site has no judgments section — [Wayback FST](http://web.archive.org/web/20260716134606/https://fst.gov.pk/)
- **Languages**:
  - Sample judgments from PHC, AJK HC, AJK SC, SAC GB, GBCC, CCP, CAT and FTO are in English, judging from the extracted text and headings, for example "JUDGMENT SHEET / PESHAWAR HIGH COURT, PESHAWAR / JUDICIAL DEPARTMENT" and "HIGH COURT OF AZAD JAMMU AND KASHMIR".
  - AJK HC bench names in the dropdown are in Urdu, for example "جناب جسٹس سردار لیاقت حسین، چیف جسٹس عدالت العالیہ".
  - PHC offers an Urdu site toggle ("English || اُردو").
  - Sources: [PHC sample](https://peshawarhighcourt.gov.pk/PHCCMS/judgments/WP-No.6226-P-of-2026-Ayesha-Jameel-etc-vs.pdf); [AJK HC page](https://ajkhighcourt.gok.pk/important-judgments)

### Inferences
- None of these courts publishes all orders. Each publishes a curated subset:
  - PHC: reported or referred judgments
  - BHC static pages: reported or significant judgments
  - GBCC: reported judgments
  - AJK SC: "important judgements"
- The FTO's 15-day feed is the only "everything" feed in scope.
- PHC's neutral-citation numbers (up to about 9,015 in 2025) suggest PHC assigns neutral citations to far more judgments than it lists. The listed set is a selection.
- SAC GB's archive thins out after 2018. AJK HC's online coverage starts only in 2022.

### Gaps
- The BHC portal's coverage (whether it holds all judgments or reported ones only) and its count could not be checked: the API redirected to login for a direct call, and I did not drive the UI.
- I did not count the GBCC total exactly. That needs one postback per decision date (17 postbacks).
- No body states its total count anywhere on its site. All counts here are derived from the listings.
- The 704 AJK SC "Judgments" posts may include a few orders or interim orders. Their titles include "(Interim Order)".

---

## Q3. Format: text PDF vs scanned (sample tests)

### Takeaway
Formats are mixed, and OCR is needed for a large share:
- **Born-digital text PDFs**: AJK HC (Word-generated), AJK SC uploads, some PHC and SAC GB files.
- **Image-only scans**: older PHC files, SAC GB, GBCC, CCP orders and CAT orders.
- **Scans with a weak copier OCR layer**: FTO (for example "lSBIrr" for "ISB/IT").

### Cited Findings (samples downloaded 12 Nov 2026)

| Sample | Size | Pages | Image objects | pdftotext non-whitespace characters | Producer / Creator | Verdict |
|---|---|---|---|---|---|---|
| PHC `CR411-2020-----13-01-2025.pdf` | 372,864 B | ~15 | 15 | 0 | (none) | Scanned, no text |
| PHC `TR86--2024-----13-02-2025.pdf` | 389,427 B | ~13 | 13 | 0 | (none) | Scanned, no text |
| PHC `WP-No.6226-P-of-2026-Ayesha-Jameel-etc-vs.pdf` | 153,804 B | ~10 | 0 | 17,744 | n/a | Text PDF ("JUDGMENT SHEET … W.P. No. 6226-P/2026 … Date of hearing 02/11/2026") |
| SAC GB `judgements2022-2026/Umer Farooq Vs The State.pdf` | 2,020,645 B | ~4 | 4 | 0 | HP Scan | Scanned |
| SAC GB `Judgments/Qalandar___others_versus_Munawar.pdf` | 52,472 B | 1 | 0 | 616 | convertonlinefree.com | Text ("IN THE SUPREME APPELLATE COURT GILGIT-BALTISTAN … C. Misc. No. 47/2013 … CPLA No. 38/2013") |
| GBCC `attach/judgements/file-a2ecbae7-….pdf` | 1,862,528 B | ~5 | 5 | 0 | HP Scan | Scanned |
| AJK HC `judgment_files/Abdul_Ghafar_vs__State.pdf` | 703,653 B | ~11 | 0 | 12,976 | Microsoft Word 2016 | Text PDF |
| AJK HC `judgment_files/Sobidar_Manzoor_Hussain_Vs__The_State_death_Qisas.pdf` | 1,310,779 B | ~41 | 0 | 36,506 | Microsoft Word 2016 | Text PDF |
| AJK SC `wp-content/uploads/2020/03/Nazir-vs.-Raja-Arif.pdf` | 113,806 B | ~9 | 0 | 6,209 | n/a | Text PDF ("SUPREME COURT OF AZAD JAMMU AND KASHMIR [Appellate Jurisdiction] … Criminal Appeal No. 55 of 2019") |
| CCP order `ccporders/e8153b39….pdf` | 1,253,333 B | ~33 | 33 | 0 | HP Scan | Scanned |
| CAT order `catorders/08-British Lyceum (06-07-2026).pdf` | 7,213,784 B | ~16 | 32 | 160 (only the "CamScanner" watermark) | CamScanner | Phone-app scan |
| FTO `assets/decisions/11887_2026.pdf` | 1,094,366 B | ~5 | 5 | 5,650 | VersaLink B7025 (Xerox MFP) | Scan + OCR ("COMPLAINT NO.11887/lSBIrr/2026 … Oated:26.06.2026") |
| FTO `DataRepository/SIGNEDFINDINGS_20261112151120146.PDF` | 3,802,709 B | ~10 | 10 | 16,465 | VersaLink B7025 | Scan + OCR ("COMPLAINT NOS.16330 & 163321LHR11T12026") |
| WMS `SiteImage/Publication/finding_onl_9161_20.pdf` | 1,103,807 B | ~4 | 4 | 4 | iLovePDF | Scanned |

Sources (sample URLs):
- [PHC CR411](https://peshawarhighcourt.gov.pk/PHCCMS//judgments/CR411-2020-----13-01-2025.pdf); [PHC WP 6226](https://peshawarhighcourt.gov.pk/PHCCMS/judgments/WP-No.6226-P-of-2026-Ayesha-Jameel-etc-vs.pdf)
- [SAC GB Umer Farooq](https://sacgb.gov.pk/Judgments/judgements2022-2026/Umer%20Farooq%20Vs%20The%20State.pdf)
- [GBCC sample](https://gbcc.gov.pk/attach/judgements/file-a2ecbae7-848c-4c86-b758-6d2b953fb05221052022135836.pdf)
- [AJK HC Abdul Ghafar](https://ajkhighcourt.gok.pk/judgment_files/Abdul_Ghafar_vs__State.pdf)
- [AJK SC Nazir vs Raja Arif](https://ajksupremecourt.gok.pk/wp-content/uploads/2020/03/Nazir-vs.-Raja-Arif.pdf)
- [CCP order](http://appadminccp.cc.gov.pk/ccporders/e8153b39fa6e9eecce3064b63a3e6e8d.pdf); [CAT order](http://appadminccp.cc.gov.pk/catorders/08-British%20Lyceum%20(06-07-2026).pdf)
- [FTO 11887](https://www.fto.gov.pk/assets/decisions/11887_2026.pdf); [FTO signed finding](http://ftocmis.fto.gov.pk/DataRepository/SIGNEDFINDINGS_20261112151120146.PDF)
- [WMS finding](https://mohtasib.gov.pk/SiteImage/Publication/finding_onl_9161_20.pdf)

- Not tested: BHC judgment PDFs (`https://bhc.gov.pk/media/judgments/<id>.pdf`). robots.txt disallows `/media/`, so I did not download a sample — [BHC robots.txt](https://bhc.gov.pk/robots.txt)
- Not tested: AJK SC 2026 posts. They embed Google Drive viewers (`https://drive.google.com/file/d/<id>/view` and `/preview`) instead of site-hosted PDFs — [AJK SC WP REST post 15999](https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts?per_page=1)

### Inferences
- Plan for OCR: English, with Urdu fragments possible. Even the FTO text layers are noisy enough that re-OCR or a correction step is advisable for citations and complaint numbers.
- PHC is mixed: two of the three samples were image-only. The share of scanned files across the 5,935 PDFs is unknown, but probably large.

### Gaps
- Sample sizes are tiny (1-3 per body), so scan/text proportions are not established.
- The AJK SC Google Drive files were not tested (and see the access question below).

---

## Q4. Search/listing structure, URL stability and enumerability (technical feasibility)

### Takeaway
Most sources can be enumerated programmatically through their public listing pages, with no CAPTCHA and no login:
- **PHC**: one POST with all filters on "All" returns about 12.4 MB of HTML listing all 5,949 records.
- **AJK HC**: plain POST; a single "All" query returns everything.
- **AJK SC**: public WordPress REST API.
- **CCP, CAT, SAC GB, FTO, WMS**: static HTML lists.
- **GBCC**: ASP.NET postbacks, but they 302 to static PDF URLs.

The weak spots:
- **BHC**: PDFs sit under a robots-disallowed path, and the portal API redirected to login for a direct call.
- **FTO signed feed**: only a 15-day window.
- **AJK SC 2026 files**: on Google Drive.

### Cited Findings
- **PHC**:
  - The search is a classic HTML POST form (multipart) to `reportedJudgments.php?action=search`, with no CAPTCHA or token fields. Setting year=0, judge=0, category=0 returned 12,377,475 bytes in about 10 s, listing all 5,949 rows in one page (client-side DataTables, no server pagination). One earlier identical attempt failed to connect (curl code 000) and succeeded on retry — [PHC search](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search)
  - PDF URLs are static files under `https://peshawarhighcourt.gov.pk/PHCCMS//judgments/`, named by uploaders. Examples include `CR411-2020-----13-01-2025.pdf`, `C.R-No.204-P2022-Abdul-Qayum-Khattak-Vs.-Abu-ul-Hassan-&-others.pdf` and a generic `Eh.Cr.A-No.pdf`. Names can contain `&`, double slashes and truncations, and 5,935 links resolved to only 5,885 unique URLs — [PHC search](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search)
- **BHC**:
  - The static per-judge pages are plain HTML. PDFs have sequential numeric ids (`/media/judgments/1331.pdf`, `1333.pdf`) — [BHC reported judgments page](https://bhc.gov.pk/resources/judgments/justice-abdul-hameed-baloch/reported-judgments)
  - The ids run 1-2004 with 2,001 used, so the PDF URLs are almost fully enumerable. Robots disallows the folder, though (see Q5).
  - The site sets a "RESS" cookie through JS and reloads once (a responsive-design cookie, not an access control) — [BHC Judgments](https://bhc.gov.pk/resources/judgments)
  - The portal's API base is `https://api.bhc.gov.pk/` (Nuxt + @nuxtjs/auth). A direct POST to `https://api.bhc.gov.pk/v2/judgments` without the app's browser context returned 302 to `https://api.bhc.gov.pk/login`. I did not pursue it further, to avoid circumventing access controls — [api.bhc.gov.pk](https://api.bhc.gov.pk/robots.txt)
- **GBCC**:
  - The ASP.NET WebForms page needs `__VIEWSTATE`/`__EVENTVALIDATION`. A search with no filters returned no rows, so a search needs a decision date or a bench.
  - Pressing "View PDF" (a postback) returns a 302 Location to `/attach/judgements/file-<GUID><ddMMyyyyHHmmss>.pdf`. That static URL then downloads directly (200, application/pdf).
  - No CAPTCHA was found on the page (0 matches for "captcha").
  - Source: [GBCC Reported Judgments](https://gbcc.gov.pk/ReportedJudgments.aspx)
- **SAC GB**: a single static HTML page holds every link. URLs are relative paths built from party names with spaces (for example `Judgments/judgements2022-2026/Umer Farooq Vs The State.pdf`) — [SAC GB Judgments](https://sacgb.gov.pk/Judgments.html)
- **AJK HC**:
  - A plain POST (form-urlencoded) with `btnSearchJudgment` returns all rows for the chosen tab. Without the submit-button field, the plain page comes back.
  - No CAPTCHA. The only validation is a client-side JS check.
  - The home page's recent-judgment links use 24-hex names (`judgment_files/c96ece6e1f0393cc38827825.pdf`). Search results show both hex names and title-based names (`judgment_files/Abdul_Ghafar_vs__State.pdf`).
  - Source: [AJK HC Judgments](https://ajkhighcourt.gok.pk/important-judgments)
- **AJK SC**:
  - The WordPress REST endpoint `/wp-json/wp/v2/posts?categories=18&per_page=100` returns JSON (date, title, content), and `X-WP-TotalPages` supports paging.
  - In the 100 newest judgment posts (2024-2026), the file host is:
    - 2024: 33 posts, wp-content/uploads
    - 2025: 32 posts, wp-content/uploads
    - 2026: 18 posts wp-content/uploads and 17 Google Drive
  - Older posts (2020) link `http://ajksupremecourt.gok.pk/wp-content/uploads/YYYY/MM/<slug>.pdf`. The very oldest (2016) posts returned no link in the `content` field.
  - Source: [AJK SC WP REST](https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts?categories=18&per_page=100)
  - The HTML listing and the single-post pages returned HTTP 500 (WordPress fatal error) while still rendering partial content — [AJK SC listing](https://ajksupremecourt.gok.pk/judgements-orders/)
- **CCP/CAT**: static HTML tables.
  - CCP order PDFs have opaque 32-hex names on `appadminccp.cc.gov.pk` over **http** (not https).
  - CAT PDFs have human filenames with spaces and parentheses.
  - Source: [CCP Orders](https://cc.gov.pk/home/orders); [CAT orders](https://cc.gov.pk/home/decidedcatcases)
- **FTO**:
  - `decisions.aspx` is static HTML with predictable names (`assets/decisions/<complaint>_<year>.pdf`).
  - The signed-findings feed is a single HTML page with timestamp-named PDFs on `ftocmis.fto.gov.pk`, over http.
  - The feed's host `onlinecomplaints.cloudns.asia:4041` is a free dynamic-DNS name on a non-standard port, although the page footer says "Designed and Developed by FTO MIS Team".
  - Sources: [FTO decisions](https://www.fto.gov.pk/decisions.aspx); [FTO Signed Decisions](http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions)
- **Wafaqi Mohtasib**: a static table of 13 PDFs under `/SiteImage/Publication/` — [WMS Findings](https://mohtasib.gov.pk/Publications)
- **Site-integrity observation**: both the PHC and BHC home pages contain hidden third-party links (spam/SEO injection).
  - PHC, after `</body>`: `<a style="display:none" href="https://it.eng.uir.ac.id/lte_assets/slot-gacor/">` — [PHC home](https://peshawarhighcourt.gov.pk/app/site/)
  - BHC footer: `<div style="display:none"><a href="https://www.evrazgeoforum.com/">` — [BHC home](https://bhc.gov.pk/)

### Inferences
- Bulk collection looks technically feasible without bypassing anything for PHC, AJK HC, AJK SC (via REST), SAC GB, GBCC (17 postbacks plus row postbacks), CCP, CAT, FTO-curated and WMS.
- For BHC, the robots.txt `Disallow: /media/` covers every judgment PDF. A compliant crawler cannot fetch them, so written permission from BHC (or an alternative channel) is needed.
- The FTO signed feed needs a daily (or at least weekly) scheduled collector to build a complete corpus going forward. Back-files need a request to FTO.
- The AJK SC files on Google Drive are official-by-linkage. But Drive download endpoints have their own terms and rate limits, and they are not .gok.pk URLs. Provenance metadata should record the linking official post.
- Filenames are unstable or non-unique at PHC (duplicates, truncated names), SAC GB (party-name filenames) and CAT. Use the listing row as the identity (case number + date + neutral citation) and store a content hash.
- The hidden spam links on PHC and BHC show that the sites have been tampered with. Integrity checks are prudent: hash each PDF and keep the fetch date and URL. Prefer PDFs reached through the official listing over search-engine-discovered URLs.

### Gaps
- Whether the BHC portal API is meant to be public: the SPA presumably calls it from the browser without user login, but my direct call was redirected to login. This needs a browser-based check or a question to BHC IT.
- No server-side rate-limit policy is published by any of these sites. One PHC connection failure was seen.
- The 2016 AJK SC posts (no link in `content`) may store files in custom fields or attachments. This was not investigated.

---

## Q5. robots.txt and terms of use / copyright notices (permission to collect)

### Takeaway
- **Explicitly permissive robots**: AJK SC (and api.bhc.gov.pk).
- **Restrictive**: BHC, which disallows `/media/`, where all judgment PDFs live.
- **No robots.txt**: everything else, either a 404 or an HTML page returned instead.
- **No body publishes terms of use or a licence** for its judgments. Footers carry only generic "All Rights Reserved" notices.

Permission to collect is therefore unaddressed, not granted. The fair default is the courts' public-access purpose plus robots, and written permission is advisable, especially for BHC.

### Cited Findings
- **robots.txt, as fetched on 12 Nov 2026**:
  - BHC `https://bhc.gov.pk/robots.txt`: "User-agent: * / Disallow: /_scripts/ / Disallow: /assets/ / Disallow: /blocks/ / Disallow: /lib/ / Disallow: /media/ / Disallow: /pages/" — [BHC robots.txt](https://bhc.gov.pk/robots.txt)
  - api.bhc.gov.pk: "User-agent: * / Disallow:" — [api.bhc.gov.pk robots.txt](https://api.bhc.gov.pk/robots.txt)
  - portal.bhc.gov.pk/robots.txt returns the SPA's HTML shell (no robots) — [portal robots](https://portal.bhc.gov.pk/robots.txt)
  - AJK SC: "User-agent: * / Disallow: / Disallow: /?s= / Sitemap: https://ajksupremecourt.gok.pk/sitemap.xml". The first Disallow line is empty, so everything is allowed except `/?s=`. — [AJK SC robots.txt](https://ajksupremecourt.gok.pk/robots.txt)
  - PHC: the robots.txt URL returns HTTP 200 with `<script type="text/javascript"> window.location.href = 'app/site/'; </script>`, i.e. no robots rules — [PHC robots.txt](https://peshawarhighcourt.gov.pk/robots.txt)
  - ATIR: robots.txt returns the HTML home page — [ATIR robots.txt](https://atir.gov.pk/robots.txt)
  - These all returned 404:
    - GBCC: "The resource cannot be found." — [gbcc robots](https://gbcc.gov.pk/robots.txt)
    - SAC GB — [sacgb robots](https://sacgb.gov.pk/robots.txt)
    - AJK HC (CodeIgniter 404) — [ajkhc robots](https://ajkhighcourt.gok.pk/robots.txt)
    - CCP — [cc robots](https://www.cc.gov.pk/robots.txt)
    - appadminccp.cc.gov.pk — [appadminccp robots](http://appadminccp.cc.gov.pk/robots.txt)
    - Wafaqi Mohtasib (IIS 404) — [mohtasib robots](https://mohtasib.gov.pk/robots.txt)
    - FTO — [fto robots](https://fto.gov.pk/robots.txt)
    - ftocmis.fto.gov.pk — [ftocmis robots](http://ftocmis.fto.gov.pk/robots.txt)
    - onlinecomplaints.cloudns.asia:4041 — [FTO feed robots](http://onlinecomplaints.cloudns.asia:4041/robots.txt)
  - FST: not retrievable. The site is suspended ("Account Suspended") — [FST robots](https://www.fst.gov.pk/robots.txt)
- **Copyright and terms text, quoted from footers**:
  - PHC: "2010-2026 Peshawar High Court. All Rights Reserved." The reported-judgments page says "All Rights are reserved. © Peshawar High Court, Peshawar." — [PHC home](https://peshawarhighcourt.gov.pk/app/site/); [PHC Reported Judgment](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php)
  - BHC: "© 2026 High Court of Balochistan. All rights reserved." — [BHC Judgments](https://bhc.gov.pk/resources/judgments)
  - GBCC: "© Copyright GB Chief Court . All Rights Reserved Designed by IT Department". Its only policy link is "Mobile App Privacy Policy" (`App_Privacy_Policy.html`) — [GBCC](https://gbcc.gov.pk/ReportedJudgments.aspx)
  - SAC GB: "Copyright © 2025 Supreme Appellate Court Gilgit-Baltistan." — [SAC GB Judgments](https://sacgb.gov.pk/Judgments.html)
  - AJK HC: "Copy Right @ 2017-2025. High Court of AJ&K Muzaffarabad Design & Develop by IT Section High Court of AJ&K" — [AJK HC](https://ajkhighcourt.gok.pk/important-judgments)
  - AJK SC: "Copyright 2020. All Rights Reserved." — [AJK SC](https://ajksupremecourt.gok.pk/judgements-orders/)
  - CCP: "© CCP 2024, Competition Commission of Pakistan ©All rights reserved" — [CCP Orders](https://cc.gov.pk/home/orders)
  - FTO: "© Federal Tax Ombudsman - All right reserved Designed & Developed by Manager MIS, FTO" — [FTO decisions](https://www.fto.gov.pk/decisions.aspx). The signed-decisions page says "Designed and Developed by FTO MIS Team © 2016 All Rights" (truncated in the page text) — [FTO feed](http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions)
  - Wafaqi Mohtasib: "Copyright © 2026, National Information Technology Board-NITB" — [WMS home](https://mohtasib.gov.pk/)
  - ATIR: "© 2023 - Appellate Tribunal Inland Revenue" — [ATIR](https://atir.gov.pk/Judgements)
  - FST (archived July 2026): "2023 © All Rights Reserved by COMSATS Internet Services Privacy Terms Contact" — [Wayback FST](http://web.archive.org/web/20260716134606/https://fst.gov.pk/)
- **No dedicated terms-of-use, disclaimer or reuse-licence page** was linked from any of these sites' home pages or judgment pages. A search of the fetched HTML for links containing "disclaimer", "terms", "privacy", "policy" or "copyright" found only the GBCC mobile-app privacy policy and the CCP "Policy Notes" (an unrelated publication series) — [GBCC](https://gbcc.gov.pk/index.aspx); [CCP](https://www.cc.gov.pk/)

### Inferences
- The "All Rights Reserved" footers are generic website notices. They do not specifically license or forbid reuse of judgment texts. How Pakistani copyright law treats judgments is covered in a separate note (`copyright_open_data_landscape.md`).
- For a corpus built only from official copies:
  - PHC, GBCC, SAC GB, AJK HC, CCP, CAT, FTO and WMS have no robots restriction (no file at all).
  - AJK SC explicitly allows crawling.
  - BHC disallows its judgment-PDF folder. Collecting BHC PDFs at scale would breach that robots directive unless BHC gives permission.
- Courtesy and good practice: identify the crawler in its user agent, throttle (PHC's server dropped one connection), and write to each registrar for permission. Prioritise BHC (because of robots), PHC (the largest volume) and FTO (to get the archive beyond 15 days).

### Gaps
- No court or tribunal publishes a reuse policy, an open-data statement or an API terms document. Whether permission letters exist (for example for commercial reporters) is unknown.
- The "Privacy" and "Terms" links on FST's archived footer were not followed. The live site is down.

---

## Q6. Bodies that publish nothing (or effectively nothing) online

### Takeaway
- **Nothing published**:
  - FST: site suspended; even before that it had no judgments section.
  - ATIR: judgments page empty.
  - Banking courts, consumer courts and environmental tribunals: no official repository found.
- **Effectively stale**:
  - Wafaqi Mohtasib: last finding posted in 2020.
  - GBCC: last decision date in 2020.
  - SAC GB: few items after 2018, and the newest "Latest Judgements" uploads are from 2022.

### Cited Findings
- FST, live: "Account Suspended" — [FST](https://www.fst.gov.pk/robots.txt). FST, July 2026: no judgment menu, only cause lists and case status — [Wayback FST](http://web.archive.org/web/20260716134606/https://fst.gov.pk/)
- ATIR: "Judgments No Record Found In Database", on both 18 Jan 2026 and 12 Nov 2026 — [ATIR](https://atir.gov.pk/Judgements); [Wayback ATIR](http://web.archive.org/web/20260118080836/https://atir.gov.pk/Judgements/)
- Wafaqi Mohtasib: the newest "Findings" item is dated 18/12/2020 — [WMS Findings](https://mohtasib.gov.pk/Publications)
- GBCC: the newest decision-date option is 2020-10-01 — [GBCC](https://gbcc.gov.pk/ReportedJudgments.aspx)
- SAC GB: the newest uploads on "Latest Judgements" are dated 03-11-2022 and 18-11-2022. The main list holds 17 files in `judgements2022-2026/` — [SAC GB Latest](https://sacgb.gov.pk/Latest%20Judgements.html); [SAC GB Judgments](https://sacgb.gov.pk/Judgments.html)
- Banking, consumer and environmental forums: only statistical LJCP reports were found (snippet only) — [LJCP ATSC 2024](https://ljcp.gov.pk/SiteImage/Misc/files/ATSC%202024%20(20-06-25).pdf)

### Inferences
- For FST and ATIR decisions, the official copies available online are the appellate judgments of the Supreme Court and High Courts (where those courts publish them), plus whatever the tribunals provide on request. A product restricted to official copies will have a gap here unless it obtains them directly from the tribunals.

### Gaps
- Whether FST or ATIR publish decisions through another channel (for example FBR's site for ATIR, or a new FST domain) was not established. A search for FBR's "appellate-tribunal" category turned up FBR pages (snippet only, not fetched): https://fbr.gov.pk/categ/appellate-tribunal/665
- Provincial service tribunals (KP, Balochistan) and the AJK/GB service tribunals were not covered.
