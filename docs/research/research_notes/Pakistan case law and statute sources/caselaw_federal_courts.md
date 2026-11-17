# Official case-law sources: Pakistan's federal-level courts (Supreme Court, Federal Shariat Court, Islamabad High Court)

Research date: 2026-11-12 (all "fetched" items were retrieved on this date with curl (UA `Mozilla/5.0 (research)`, no TLS bypass, no cookies or CAPTCHA handling) or with the WebFetch tool).
Method note: Pages were fetched directly, robots.txt files were read before any data endpoint was called, and only endpoints that the courts' own public pages call without a login or CAPTCHA were queried (one call each). No CAPTCHA, login or WAF block was bypassed. Where a host blocked us, the error is recorded and nothing else was tried.

Scope note: The 27th Constitutional Amendment (November 2025) created a **Federal Constitutional Court (FCC)**, which is now also a federal-level court. It is outside this assignment's three courts, but it is flagged in Gaps because it now hears constitutional matters that used to go to the SC ([Wikipedia: Federal Constitutional Court of Pakistan](https://en.wikipedia.org/wiki/Federal_Constitutional_Court_of_Pakistan), snippet only). Its site https://www.fccp.gov.pk/judgments was fetched: HTTP 200, but it is an empty React shell (`<div id="root"></div>`), and `/robots.txt` returns the same SPA HTML, so no robots file exists.

## Source inventory

| Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| SCP robots.txt | https://scp.gov.pk/robots.txt | Supreme Court of Pakistan (SCP) | robots | live 2026-11-12 | Primary | Fetched (200, 2,676 B) |
| SCP Judgments Search | https://scp.gov.pk/JudgmentsSearch | SCP | Official search | live 2026-11-12 | Primary | Fetched (200, 77.6 KB) |
| SCP Latest Judgments | https://scp.gov.pk/LatestJudgments.aspx → redirects to /LatestJudgments | SCP | Official listing | items uploaded up to 11-11-2026 | Primary | Fetched (200, 101.9 KB) |
| SCP Sitemap | https://scp.gov.pk/Sitemap.aspx | SCP | Site map | live | Primary | Fetched (200) |
| SCP Default (home) | https://scp.gov.pk/Default.aspx | SCP | Home | live | Primary | Fetched (200) |
| SCP sitemap.xml | https://scp.gov.pk/sitemap.xml | SCP | Sitemap | — | Primary | Inaccessible: HTTP 404 |
| SCP case-search JS | https://scp.gov.pk/Scripts/case-search.js?v=20261017-1 | SCP | Site code | v=20261017-1 | Primary | Fetched (200) |
| SC legacy domain (home) | https://www.supremecourt.gov.pk/ | SCP | Legacy site / PDF host | — | Primary | Inaccessible: HTTP 403 "Access Denied" (Akamai edgesuite reference page) |
| SC legacy robots.txt | https://www.supremecourt.gov.pk/robots.txt | SCP | robots | — | Primary | Inaccessible: HTTP 403 Access Denied |
| SC legacy latest-judgements | https://www.supremecourt.gov.pk/latest-judgements/ | SCP | Legacy listing | — | Primary | Inaccessible: HTTP 403 |
| SC apex without www | https://supremecourt.gov.pk/ | SCP | — | — | — | Inaccessible: curl exit 35 (TLS handshake failure) |
| SC judgment PDF sample | https://www.supremecourt.gov.pk/downloads_judgements/c.p._2972_2022.pdf | SCP | Judgment PDF | uploaded per SCP listing | Primary | Inaccessible: HTTP 403 via curl (https and http) and via WebFetch |
| SC legacy WP endpoints | https://www.supremecourt.gov.pk/wp-content/plugins/insert-php/online_judgments.php ; .../my-plugin/latest_judgements.php | SCP | Legacy listing | snippet showed entries dated Nov 2025 to Mar 2026 | Primary (search index) | Snippet only (not fetched; host returns 403 to us) |
| FSC robots.txt | https://www.federalshariatcourt.gov.pk/robots.txt | Federal Shariat Court (FSC) | robots | live | Primary | Fetched (200, 196 B) |
| FSC home | https://federalshariatcourt.gov.pk/ (same content at www.) | FSC | Home | Last-Modified: Thu, 12 Nov 2026 08:03:41 GMT | Primary | Fetched (200, 43 KB) |
| FSC Shariat Petitions judgments | https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php | FSC | Official listing | latest item 19 Mar 2025 | Primary | Fetched (200, 225 KB) |
| FSC Criminal judgments | https://www.federalshariatcourt.gov.pk/criminaljudgments.html | FSC | Listing | — | Primary | Fetched: "Under Construction" |
| FSC Suo Moto | https://www.federalshariatcourt.gov.pk/suomoto.html | FSC | Listing | — | Primary | Fetched: "Under Construction" |
| FSC Landmark judgments | https://www.federalshariatcourt.gov.pk/landmarkjudgemnts.html | FSC | Listing | — | Primary | Fetched (empty table shell; no data rendered server-side) |
| FSC Orders / Cause list | https://www.federalshariatcourt.gov.pk/orders.html ; /causelist.html | FSC | Listing | — | Primary | Fetched (200); contents not analysed in detail |
| FSC sitemap.xml | https://www.federalshariatcourt.gov.pk/sitemap.xml | FSC | Sitemap (WordPress AIOSEO) | lastmod 2026-10-01 | Primary | Fetched (200) |
| FSC PDF sample 1 | https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=128 | FSC | Judgment PDF (PLD 2025 FSC 1) | decided 19 Mar 2025 | Primary | Fetched (200, application/pdf, 14 pp, 532 KB) |
| FSC PDF sample 2 | https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=109 | FSC | Judgment PDF (Sh.P. 24/I of 1990) | 1990s | Primary | Fetched (200, application/pdf, 133 KB) |
| IHC www | https://www.ihc.gov.pk/ | Islamabad High Court (IHC) | Home (iframe wrapper) | live | Primary | Fetched (200, 1.4 KB) |
| IHC robots.txt | https://ihc.gov.pk/robots.txt ; https://mis.ihc.gov.pk/robots.txt | IHC | robots | — | Primary | Both HTTP 404 (no robots file) |
| IHC MIS index | https://mis.ihc.gov.pk/index.aspx → /index | IHC | Portal home | live | Primary | Fetched (200, 72.7 KB) |
| IHC Judgments page | https://mis.ihc.gov.pk/frmJgmnt (also frmJgmnt.aspx?jgs=0 / ?jgs=1) | IHC | Official listing | live | Primary | Fetched (200, 41 KB) |
| IHC Search Judgements/Orders | https://mis.ihc.gov.pk/frmSrchOrdr.aspx → /frmSrchOrdr | IHC | Official search | live | Primary | Fetched (200, 100 KB) |
| IHC latest-judgments JSON | POST https://mis.ihc.gov.pk/ihc.asmx/GetLatestJgmntsNew | IHC | JSON web service used by page | live | Primary | Fetched once (200, 3.4 KB, 8 records) |
| IHC search JSON | POST https://mis.ihc.gov.pk/ihc.asmx/srchDecisionClms | IHC | JSON web service used by page | live | Primary | Fetched once (200, 120.6 KB, 97 records) |
| IHC PDF sample | https://mis.ihc.gov.pk/attachments/judgements/209540/1/Muhammad_Usman_v_FoP_WP_No_1553_of_2026__J_Arbab_Muhammad_Tahir__Approved_for_Reporting_639280833781874862.pdf | IHC | Judgment PDF | Last-Modified 20 Oct 2026 | Primary | Fetched (200, application/pdf, 6 pp) |
| FCC judgments | https://www.fccp.gov.pk/judgments | Federal Constitutional Court | SPA | — | Primary | Fetched (200 but JS shell only) |
| Third-party "SCP" citation index | https://pakcaselaw.duckdns.org/browse/journal/SCP?p=20 | Unknown private site | Aggregator | — | Low (unofficial, garbled entries reported) | Snippet only |
| IEEE DataPort SC judgments dataset | https://ieee-dataport.org/documents/supreme-court-pakistan-judgments-dataset | IEEE DataPort (third party) | Dataset | about 1,200 judgments up to May 2025 (per snippet) | Medium (secondary) | Snippet only |
| SC 2015 Urdu directive coverage | https://www.scconline.com/blog/post/2015/09/11/directions-given-for-the-implementation-of-urdu-as-the-official-language-of-pakistan/ | SCC Online blog | Secondary news | 11 Sep 2015 | Medium | Snippet only |
| 2013 Urdu translation section plan | https://tribune.com.pk/story/604505/entertainment | Express Tribune | Secondary news | 2013 | Medium | Snippet only |
| NJPMC AI guidelines | https://www.thenews.pk/print/1412952-njpmc-issues-guidelines-for-ai-use-at-judicial-institutions ; https://www.app.com.pk/?p=1160741 | The News; APP | Secondary news | Feb 2026 (per snippet) | Medium | Snippet only |
| SC AI judgment coverage | https://propakistani.pk/2025/04/11/supreme-court-backs-use-of-ai-in-judiciary/ ; https://www.dawn.com/news/1907299/judiciary-embracing-ai | ProPakistani; Dawn | Secondary news | Apr 2025 | Medium | Snippet only |
| IHC digital court | https://arynews.tv/ihc-launches-smart-paperless-digital-court | ARY News | Secondary news | undated in snippet | Low/Medium | Snippet only |

---

## 1. Supreme Court of Pakistan (SCP)

### Takeaway
The SC's current official site is **scp.gov.pk** (ASP.NET WebForms on Cloudflare). Its full judgment search (`/JudgmentsSearch`) is gated by **Google reCAPTCHA v3**, so programmatic search is not permissible without bypassing an access control. The **Latest Judgments** page (`/LatestJudgments`) is plain server-rendered HTML with no CAPTCHA, showing 25 entries with metadata and direct PDF links. Those PDFs live on the legacy host **www.supremecourt.gov.pk/downloads_judgements/**, which returned **HTTP 403 (Akamai "Access Denied")** to every automated fetch we tried. SCP's robots.txt **disallows ClaudeBot, anthropic-ai, GPTBot, CCBot and others** and sets `Content-Signal: search=yes,ai-train=no,use=reference` for all agents, an explicit reservation against AI training.

### Cited Findings (raw facts)

**Official sites and URLs**
- scp.gov.pk is live. Response headers: `Server: cloudflare`, `x-aspnet-version: 4.0.30319`, `x-powered-by: ASP.NET`, `x-powered-by-plesk: PleskWin`. The site sets an `ASP.NET_SessionId` cookie. [scp.gov.pk](https://scp.gov.pk/) (fetched, HEAD)
- Judgment URLs: `https://scp.gov.pk/JudgmentsSearch` (search) and `https://scp.gov.pk/LatestJudgments` (latest list). The site map also links CauseList.aspx, CauseListSearch.aspx, OnlineCaseInformation.aspx, AnnualReports.aspx, PressRelease.aspx, ResearchCentrePublications.aspx, NationalJudicialPolicy.aspx, LawJusticeCommission.aspx and FortnightlyDisposalReport.aspx. [Sitemap](https://scp.gov.pk/Sitemap.aspx) (fetched)
- The header of the search page carries a "Beta" label, plus links to a Google Play app (`pk.gov.supremecourt`) "for case updates, judgments & more". [JudgmentsSearch](https://scp.gov.pk/JudgmentsSearch); [LatestJudgments](https://scp.gov.pk/LatestJudgments.aspx) (fetched)
- `www.supremecourt.gov.pk/` returned HTTP 403 with body "Access Denied … You don't have permission to access … on this server. Reference #18.2fef2117…" and a link to `errors.edgesuite.net`, which indicates an Akamai edge block. `supremecourt.gov.pk/` (no www) failed the TLS handshake (curl exit 35). [www.supremecourt.gov.pk](https://www.supremecourt.gov.pk/) (inaccessible)
- Search snippets show that the legacy WordPress endpoints `https://www.supremecourt.gov.pk/wp-content/plugins/insert-php/online_judgments.php` and `.../my-plugin/latest_judgements.php` still exist in search indexes, with listings that carry an "SCPCitation" value (e.g. "2025 SCP 449") and entries dated Nov 2025 to Mar 2026. (Snippet only; host 403 to us.)

**Search form structure (JudgmentsSearch)**
- The page is a `<form method="post" action="./JudgmentsSearch">` with `__VIEWSTATE`, `__EVENTVALIDATION` and `__EVENTTARGET`, i.e. ASP.NET WebForms postbacks. [JudgmentsSearch](https://scp.gov.pk/JudgmentsSearch) (fetched)
- Filters (field names verbatim): `ddlSittingJudges` (19 judges + blank), `ddlFormerJudges` (49 + blank, mutually exclusive with sitting judge), `ddlReported` (values `Y`/`N`, labelled "Reported Yes/No"), `txtPartiesName`, `txtTagline`, `txtKeywords`, `ddlCaseType` (35 types, e.g. C.A., C.P.L.A., Crl.P.L.A., J.P., S.M.C., H.R.C., Reference., T.A.(C)), `txtCaseNumber` (placeholder "e.g., C.P.L.A.4677/2025"), `ddlCaseYear` (2026 back to **1980**), `txtDateOfAnnouncement` (date), `txtCitation`, `txtSCCitation` ("Enter SC citation..."). [JudgmentsSearch](https://scp.gov.pk/JudgmentsSearch) (fetched)
- The search button is `onclick="return submitProtectedSearch();__doPostBack('ctl00$MainContent$btnSearch','')"`. The page loads `https://www.google.com/recaptcha/api.js?render=6Lfya_MtAAAAAKhOQ_aIQG3EbOT8WuMT3ind3tGL`. `case-search.js` calls `grecaptcha.execute(siteKey, { action: action })` and writes the token into a hidden field `recaptchaV3Token`. The page text includes the error string "Unable to verify this search. Please try again." [JudgmentsSearch](https://scp.gov.pk/JudgmentsSearch); [case-search.js](https://scp.gov.pk/Scripts/case-search.js?v=20261017-1) (fetched)

**Latest Judgments listing**
- The page is server-rendered HTML with no reCAPTCHA script tag (one textual "recaptcha" mention only). Table headers are verbatim: "Sr. No. | Case Subject | Case No | Case Title | Author Judge | Judgment Date | Upload Date | Citation | SC Citation | Download". [LatestJudgments](https://scp.gov.pk/LatestJudgments.aspx) (fetched)
- It holds 25 rows, each with a direct PDF link. Examples:
  - `https://www.supremecourt.gov.pk/downloads_judgements/c.p._2972_2022.pdf`
  - `.../c.p._10_l_2025.pdf`
  - `.../crl.a._281_2023.pdf`
  - `.../c.a._431_2026.pdf`
  - `.../c.p._677_p_2026.pdf`
  - `.../crl.p._207_k_2025.pdf`
  - `.../c.a._1285_2021_dn.pdf` and `.../c.a._1285_2021_wdn.pdf`. The listing describes the second judgment on C.A.1285/2021, by Mr. Justice Muhammad Shafi Siddiqui, as "Dissenting Note."
  - [LatestJudgments](https://scp.gov.pk/LatestJudgments.aspx) (fetched)
- Example row text: "Restoration / Before High Court C.P.L.A.903/2026 Safdar Ali Butt v. Faisalabad Development Authority… Mr. Justice Muhammad Ali Mazhar 23-07-2026 07-11-2026 PDF 33.14 KB (1) If advocate lacks a sense of his professional duty…". Some rows carry a short holding summary. Upload dates in the list ran from 31-10-2026 to 11-11-2026. The Citation and SC Citation cells were empty for the rows shown. File sizes are mostly 18–137 KB, with some 1.2–2.65 MB. [LatestJudgments](https://scp.gov.pk/LatestJudgments.aspx) (fetched)
- No pagination controls were seen on LatestJudgments (25 rows only).

**PDF access**
- `GET https://www.supremecourt.gov.pk/downloads_judgements/c.p._2972_2022.pdf` returned HTTP 403 (Akamai, 446-byte HTML), over both https and http. WebFetch on the same URL also returned 403. `https://scp.gov.pk/downloads_judgements/c.p._2972_2022.pdf` returned 404, so scp.gov.pk does not mirror the PDFs. **No SC PDF could be downloaded, so text extractability was not verified.**

**robots.txt and terms (verbatim)**
- [scp.gov.pk/robots.txt](https://scp.gov.pk/robots.txt) (fetched), relevant lines:
  ```
  # ai-input: inputting content into one or more AI models (e.g., retrieval
  #           augmented generation, grounding, or other real-time taking of content for
  #           generative AI search answers).
  # ai-train: training or fine-tuning AI models.
  # ANY RESTRICTIONS EXPRESSED VIA CONTENT SIGNALS ARE EXPRESS RESERVATIONS OF
  # RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION DIRECTIVE 2019/790 ...
  # BEGIN Cloudflare Managed content
  User-agent: *
  Content-Signal: search=yes,ai-train=no,use=reference
  Allow: /
  User-agent: ClaudeBot
  Disallow: /
  User-agent: anthropic-ai
  Disallow: /
  User-agent: Claude-Web
  Disallow: /
  User-agent: GPTBot
  Disallow: /
  User-agent: CCBot
  Disallow: /
  User-agent: Google-Extended
  Disallow: /
  ```
  Other disallowed agents: Amazonbot, Applebot-Extended, Bytespider, Diffbot, omgili, cohere-ai, MistralAI-Training, meta-externalagent, GoogleOther, Baiduspider, PetalBot, Awario bots, Google-CloudVertexBot, QualifiedBot, Cotoyogi, ICC-Crawler, atlassian-bot, FishBot, BorderxBot, NavuBot, SemrushBot-SWA, WARDBot, magpie-crawler, KimiBot, CitibotSiteCrawler.
  The file's preamble also says: "If the website operator does not include a Content-Signal for a corresponding use, the website operator neither grants nor restricts permission via Content-Signal". **ai-input is not specified.**
- The footer says: "Copyright © 2026 Supreme Court of Pakistan. All Rights Reserved". Its "Privacy Policy" and "Terms of Use" links are `href="#"`, i.e. placeholders with no actual terms page. [JudgmentsSearch](https://scp.gov.pk/JudgmentsSearch) (fetched)
- The robots.txt for the PDF host (www.supremecourt.gov.pk) could not be retrieved (403).

**Neutral citation, Urdu and AI initiatives**
- The SC listings carry a separate "SC Citation" column and search field alongside "Citation" (law-report citation). [LatestJudgments](https://scp.gov.pk/LatestJudgments.aspx) (fetched). Search snippets of the legacy WP listing show values in the form "2025 SCP 449". (Snippet only)
- A third-party index lists Supreme Court decisions as "2025 SCP 112" / "2024 SCP 416" with parallel PLD/SCMR/PLJ citations, about 2,116 entries. [pakcaselaw.duckdns.org](https://pakcaselaw.duckdns.org/browse/journal/SCP?p=20) (snippet only, unofficial, reported duplicates and garbling)
- No Urdu-language judgment section or Urdu link was found on the fetched pages: a grep for "urdu" on Sitemap, Default and LatestJudgments returned nothing.
- In September 2015 the SC directed that judgments in public-interest cases and judgments "enunciating a principle of law" under Art. 189 be translated into Urdu and published in line with Art. 251. [SCC Online blog, 11 Sep 2015](https://www.scconline.com/blog/post/2015/09/11/directions-given-for-the-implementation-of-urdu-as-the-official-language-of-pakistan/) (snippet only). A 2013 report said the registrar planned a section for Urdu translations of rulings. [Express Tribune, 2013](https://tribune.com.pk/story/604505/entertainment) (snippet only)
- AI developments:
  - April 2025: in *Ishfaq Ahmed v. Mushtaq Ahmed*, a two-member SC bench headed by Justice Syed Mansoor Ali Shah recommended that the NJPMC, with the LJCP, develop guidelines on AI use in the judiciary. [ProPakistani, 11 Apr 2025](https://propakistani.pk/2025/04/11/supreme-court-backs-use-of-ai-in-judiciary/); [Dawn](https://www.dawn.com/news/1907299/judiciary-embracing-ai) (snippets only)
  - 11 Feb 2026: the NJPMC, at its 57th meeting, adopted "national guidelines for the use of artificial intelligence in judicial institutions", drafted by the LJCP and reported as published on the SC, LJCP and high court websites. [The News](https://www.thenews.pk/print/1412952-njpmc-issues-guidelines-for-ai-use-at-judicial-institutions); [APP](https://www.app.com.pk/?p=1160741) (snippets only; guideline text not fetched)
  - The SCP home page links to an LJCP slider item: https://www.ljcp.gov.pk/SliderDetail/NmJhZmVhY2MtMTkxYS00ODM5LTg4NjItNzQ1YTcxNTAyN2Vm (link seen; content not fetched).

### Inferences (analysis)
- **Coverage.** The case-year dropdown starts at 1980, which suggests the search database goes back to case years around 1980. This was not verified because the search is CAPTCHA-gated. The "Reported Y/N" filter shows that the database holds both reported and unreported judgments, not just approved-for-reporting ones. The 35 case types include leave petitions (C.P.L.A., Crl.P.L.A., J.P.), so short leave-refusing orders and judgments are likely present.
- **Case-number format.** SC numbers take the form `<type>.<no>[-<registry>]/<year>`, e.g. C.P.L.A.224-P/2025, where the suffix is a branch registry (P = Peshawar, K = Karachi, L = Lahore; Q presumably Quetta). PDF filenames are lowercase normalisations: `c.p._224_p_2025.pdf`, `crl.p._207_k_2025.pdf`, `c.a._1285_2021_dn.pdf` (dissent). The filename drops "L.A." (C.P.L.A. becomes `c.p.`), so filenames are semi-predictable but not unique keys. Guess-based enumeration would be unreliable and would amount to probing.
- **Neutral citation.** "SC Citation" / "YYYY SCP N" looks like a court-assigned neutral citation, since it is distinct from reporter citations (PLD/SCMR) and has its own column. No official notice defining it or its start date was found. Treat it as probable, not confirmed.
- **Feasibility.**
  - (a) The search endpoint must not be automated: reCAPTCHA v3 is an access control.
  - (b) LatestJudgments (25 rows, no CAPTCHA) could be polled at low frequency to capture new uploads with rich metadata: subject tagline, author judge, judgment and upload dates, summary.
  - (c) The PDF host blocked every automated request from our environment with 403. Whether this is geo-based, reputation-based or UA-based is unknown, and working around it (UA spoofing, proxies) would be bypassing an access control.
  - (d) robots.txt explicitly disallows Anthropic/OpenAI/CC crawlers and states `ai-train=no`. Any training use of SCP-hosted content conflicts with an express reservation. RAG/"ai-input" use is unstated, and `use=reference` suggests reference use (citation/linking) is tolerated.
  - **Net:** compliant bulk collection from SC official sources is currently **not feasible** without written permission or a data-sharing arrangement with the SC (Registrar / SC Research Centre / IT). The project should pursue that route.
- **Format (inference only).** Small file sizes (18–137 KB for multi-page judgments) are consistent with born-digital text PDFs. The 1–2.6 MB files may contain scans or annexures. Unverified.

### Gaps
- No SC PDF could be retrieved, so text extractability, paragraph numbering and the presence of an SC citation on the face of the judgment are **unverified**. Needs a manual browser download by a team member.
- Total SC judgment count and earliest judgment year actually available are unknown (search gated). Not found in fetched pages. Annual reports (AnnualReports.aspx) were not fetched.
- No official definition or start date of "SC Citation" / "SCP" neutral citation was found.
- No current SC Urdu-translations section was found. Whether the 2015 Urdu directive led to an online Urdu judgment collection is unknown.
- No SC Terms of Use exists (the link is a placeholder). It is unknown whether the SC has any policy on reuse of judgments, or whether the www.supremecourt.gov.pk 403 is geo-fencing.
- No RSS/feeds were found on scp.gov.pk.
- The full text of the NJPMC AI guidelines (Feb 2026) was not fetched. Whether they address third-party AI use of judgments is unknown.

---

## 2. Federal Shariat Court (FSC)

### Takeaway
The FSC site (**www.federalshariatcourt.gov.pk**, Apache; static HTML/PHP pages plus WordPress remnants) publishes **one working judgment list: Shariat Petitions, 169 entries (1980–2025)**. It is a single server-rendered HTML table with integer-ID PDF links (`shariatjudgment2.2.php?download=N`, IDs 3–210). There is no CAPTCHA or login, and robots.txt only disallows `/wp-admin/`. The "Criminal" and "Suo Moto" judgment pages are "Under Construction", and the Landmark page rendered no rows. PDFs are mixed: a 2025 file is a text PDF of the **PLD-reported version, with PLD headnotes**; a 1990 file is a scan with an OCR text layer of mediocre quality.

### Cited Findings (raw facts)
- **Home navigation.** The menu lists "Judgments: Shariat (Shariat Petitions, Suo Moto), Criminal, Landmark Judgments", plus Roster, Cause List, Orders, Annual Report, Judicial Statistics, "E-Library", and "Case Flow Management System". The footer reads "© 2026 Federal Shariat Court — IT Wing". [FSC home](https://federalshariatcourt.gov.pk/) (fetched)
- **Shariat Petitions list.** Heading: "Shariat Judgments, Shariat Petitions · Federal Shariat Court of Pakistan, Show 25 50 100 All, **169 judgments**". Columns: "# | Sh.P. / Ref. No | Party Names | FSC Citation | Decision Date | Author Judge | Law Challenged | Remarks | Judgment". [shariatjudgment2.2.php](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php) (fetched)
- **Sample rows:**
  - "Sh.P.NO.10/I of 2023 | Syeda Fouzia Jalaal Shah Vs. Federation of Pakistan … | PLD 2025 FSC 1 | 19 Mar 2025 | Justice Dr. Syed Muhammad Anwer … | Chaddar or Parchi custom in the area of District Bannu … | Partially Allowed."
  - "Sh.P.NO.1/I of 2024 … PLD 2024 FSC 33 | 23 Apr 2024".
  - [same](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php) (fetched)
- **Links and IDs.** Each row links `?view=N` (View) and `?download=N` (Download). There are 159 rows with download links (IDs 3 to 210, non-contiguous) and 10 rows without a link. (Own parse of fetched HTML.)
- **Decision-year distribution** (parsed from the table): 1980 (10), 1981 (12), 1982 (8), 1983 (3), 1984 (9), 1985 (3), 1986 (1), 1987 (2), 1988 (1), 1989 (8), 1990 (1), 1991 (13), 1992 (18), 1993 (1), 1998 (1), 2003 (1), 2004 (2), 2005 (2), 2007 (3), 2008 (5), 2009 (6), 2010 (6), 2012 (4), 2013 (7), 2014 (2), 2015 (4), 2016 (8), 2017 (2), 2018 (1), 2020 (2), 2021 (5), 2022 (6), 2023 (7), 2024 (3), 2025 (1). The latest decision is dated 19 Mar 2025. (Own parse.)
- **Download response.** `?download=128` returned `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="ShariatPetitionNo.10-Iof2023.pdf"` (14 pages, PDF 1.7). `pdftotext` extracted 37,484 characters starting:
  ```
  P L D 2025 Federal Shariat Court 1
  Present: Iqbal Hameedur Rahman, C.J., ...
  Shariat Petition No. 10/I of 2023, decided on 19th March, 2025.
  Enforcement of Shari'ah Act (X of 1991)---
  ----S.13---Penal Code (XLV of 1860), S. 498-A---...
  ```
  The judgment body has numbered paragraphs ("2. The petitioner in support…", "3. After admission…"). Some Urdu/Arabic terms were dropped by extraction, leaving blanks: "commonly known as  (Haq Bakhshwai)". [download=128](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=128) (fetched)
- `?download=109` returned filename "S.P.NO.24-I-1990L-W.pdf" (133 KB). It has a text layer (9,817 chars), but with OCR errors, e.g. "Mr.Justice Dr.Tanzil-ur-P.ahman CHIEF JUSTICE", "Justice, Lav? & Parliamentarv Affairs", "2ia.rud^pin_Ahmad". [download=109](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=109) (fetched)
- **Other judgment pages.** [criminaljudgments.html](https://www.federalshariatcourt.gov.pk/criminaljudgments.html) and [suomoto.html](https://www.federalshariatcourt.gov.pk/suomoto.html) say verbatim: "🚧 This Page is Under Construction We are working on this section and it will be available soon." [landmarkjudgemnts.html](https://www.federalshariatcourt.gov.pk/landmarkjudgemnts.html) shows "Landmark Judgments, Leading decisions of the Federal Shariat Court of Pakistan, newest first. Search by title or citation and download the full judgment as PDF." and "Source: Federal Shariat Court of Pakistan, federalshariatcourt.gov.pk. PDFs open on the court's website." No rows were in the server HTML, and no data endpoint was identified (fetched).
- **robots.txt** (verbatim, complete). [robots.txt](https://www.federalshariatcourt.gov.pk/robots.txt) (fetched)
  ```
  User-agent: *
  Allow: /wp-admin/admin-ajax.php
  Disallow: /wp-admin/
  Sitemap: https://www.federalshariatcourt.gov.pk/sitemap.xml
  Sitemap: https://www.federalshariatcourt.gov.pk/sitemap.rss
  ```
- **sitemap.xml** comment: "This sitemap was dynamically generated on November 12, 2026 at 6:23 pm by All in One SEO - the original SEO plugin for WordPress". It points to `/en/home/page-sitemap.xml` (lastmod 2026-10-01), a WordPress remnant that does not list the judgment pages. [sitemap.xml](https://www.federalshariatcourt.gov.pk/sitemap.xml) (fetched)
- **No disclaimer or terms.** No terms-of-use, disclaimer or copyright notice was found beyond the footer "© 2026 Federal Shariat Court — IT Wing". [FSC home](https://federalshariatcourt.gov.pk/) (fetched)
- **Urdu.** Pages load the Google fonts "Noto Nastaliq Urdu" and "Amiri", but no Urdu judgment list was observed. (Fetched HTML)

### Inferences (analysis)
- **Feasibility: high.** The FSC Shariat Petitions corpus (about 159 PDFs) is fully listed in one HTML page with integer download IDs, and robots.txt permits it. A one-off polite crawl (rate-limited) of the listing plus `?download=N` for the IDs *in the listing* is compliant. Guessing IDs not in the listing is unnecessary.
- **Coverage is narrow.** Only Shariat-jurisdiction petitions (Art. 203-D) are listed. The FSC's criminal appellate (Hudood) judgments, which are the bulk of its output, and its suo motu judgments are **not published online** ("Under Construction"). The list is clearly selective: 169 items across 45 years, with gaps in years.
- **Copyright and "official copy" risk.** At least the recent file is the *PLD-reported* version, carrying the law-report publisher's headnotes ("P L D 2025 Federal Shariat Court 1"). It is hosted by the court, but the headnotes are editorial content of a private reporter (PLD Publishers). For an "official copies only" corpus, the product may need to strip headnotes and keep the judgment text. Legal review recommended.
- **Format.** The format is mixed: born-digital text for recent files, scan plus OCR for older ones. Older files need re-OCR, and Urdu/Arabic glyphs drop out in extraction even from text PDFs. The FSC citation field gives reporter citations (PLD … FSC …), not a neutral citation.

### Gaps
- How many listed PDFs are scans vs born-digital is unknown (only 2 sampled).
- The 10 listed judgments without download links were not identified.
- The Landmark Judgments page probably loads its data client-side, but the data source was not identified.
- orders.html and causelist.html were fetched but not analysed. Whether "Orders" means judicial orders or administrative office orders is unclear.
- No FSC statement on reuse or copyright was found. Whether the court licenses the PLD text is unknown.
- No FSC neutral citation scheme, RSS feed or digitisation announcement was found.

---

## 3. Islamabad High Court (IHC)

### Takeaway
**www.ihc.gov.pk** is just an iframe wrapper for **mis.ihc.gov.pk** (an ASP.NET site on IIS 10). The judgments pages (`/frmJgmnt`, `/frmSrchOrdr`) are populated by **public, unauthenticated JSON ASMX web services** (`/ihc.asmx/GetLatestJgmntsNew`, `/ihc.asmx/srchDecisionClms`, `srchDecision*`), with **no CAPTCHA**. There is **no robots.txt** (404 on both hosts). Records carry rich metadata:
- approved-for-reporting flag (`O_AFR`) and landmark flag (`ISLANDMARK`)
- citation (`O_CITATION`, e.g. "2026 CLC 381" or "Citation Awaited")
- IHC headnote and subject
- even SC-appeal outcome fields

The sample PDF was a **born-digital text PDF with numbered paragraphs and an "Approved for reporting." endorsement**. PDF filenames include a .NET-ticks-like suffix, so they are discoverable via the JSON listing, not by guessing. A site disclaimer says content is "for information only" and not for "official purposes".

### Cited Findings (raw facts)
- **iframe wrapper.** www.ihc.gov.pk returns a small page containing `<iframe src="https://mis.ihc.gov.pk/index.aspx" …>` with meta description "Official Website of Islamabad High Court, Islamabad." [www.ihc.gov.pk](https://www.ihc.gov.pk/) (fetched)
- **Judgments page text** (verbatim): "Judgements / Orders. View Reported and important judgments of Honourable judges of Islamabad High Court. Note: Please contact the concerned Case Branch to get the missing / wrong data (if any ) updated on the System." Its links are "Judgements of Sitting Justices" (`frmJgmnt.aspx?jgs=1`), "Judgements of Former Justices" (`?jgs=0`), "Case Law Management System", "Search Judgements / Orders" (`frmSrchOrdr.aspx`) and "IHC Latest Judgments". [frmJgmnt](https://mis.ihc.gov.pk/frmJgmnt) (fetched)
- **Disclaimer** (verbatim, on frmJgmnt): "Disclaimer: The content available on this site is for information only. Users are advised not to rely on this information for official purposes. Islamabad High Court, Islamabad, is not responsible for any damages arising from use of the content of this site." [frmJgmnt](https://mis.ihc.gov.pk/frmJgmnt) (fetched)
- **robots.txt.** https://ihc.gov.pk/robots.txt returned 404 (Apache) and https://mis.ihc.gov.pk/robots.txt returned 404 (IIS). No robots rules exist.
- **Page scripts.**
  - The judgments page calls `$.ajax({type:"POST", contentType:"application/json; charset=utf-8", url:"ihc.asmx/GetLatestJgmntsNew"})`.
  - Its judge list comes from `Go("ihc","Juges_GA", …, {PISRETIRED:0, CUR_REC:null})`.
  - Per-judge "Reported" and "Important" buttons call `srchJugmnts('0', judgeId, '0','0','', '01/01/1900', LANDMARK, AFR)`, which POSTs `{'PCASENO','PJUG','PADV','PYEAR','pPrty','PDDATE','PLANDMARK','PAFR'}` to `ihc.asmx/srchDecisionClms`.
  - Results go into a jQuery DataTable with columns "Sr | CASE_NO | Bench | Hon'ble_Author_Judge | PARTY_NAMES | CITATIONS".
  - View links have the form `/frmRdJgmnt.aspx?cseNo=<CASENO> | <O_CITATION>&cseTle=<PARTIES>&jgs=<BENCH>&jgmnt=<ATTACHMENTS>`.
  - [frmJgmnt](https://mis.ihc.gov.pk/frmJgmnt) (fetched); the generic caller is `/js/CallSer.js`, which POSTs to `<page>.asmx/<fun>`.
- **Search page.** frmSrchOrdr contains no CAPTCHA. Its web methods are `ihc.asmx/srchDecision`, `srchDecision1`, `srchDecision5`, `FillYear`, `Advct_GA`, `Juges_GA`, `/ihc.asmx/getHrngDtl` and `/ihc.asmx/getRltdCse`. Input placeholders: "Enter Keyword", "Case No", "Case Title / Party Name / Appellant / Opponent", "Decision Date (date/month/year)", "Page #". [frmSrchOrdr](https://mis.ihc.gov.pk/frmSrchOrdr.aspx) (fetched)
- **GetLatestJgmntsNew** (one POST) returned 8 records.
  - Record fields: PARTIES, DDATE, ATTACHMENTS, ISLANDMARK, O_AFR, O_CITATION, CASENO, BENCHNAME, T_SITTING, T_CL, T_ORDR, T_DSP.
  - Examples:
    - CASENO "Writ Petition-2494-2025", DDATE "16-JUL-2025", O_CITATION "2026 CLC 381"
    - "Writ Petition-5459-2025", "2026 YLR 1121"
    - "Writ Petition-1553-2026", "Citation Awaited"
  - ATTACHMENTS example: `/attachments/judgements/209540/1/Muhammad_Usman_v_FoP_WP_No_1553_of_2026__J_Arbab_Muhammad_Tahir__Approved_for_Reporting_639280833781874862.pdf`.
  - [GetLatestJgmntsNew](https://mis.ihc.gov.pk/ihc.asmx/GetLatestJgmntsNew) (fetched once)
- **srchDecisionClms** (one POST, PYEAR=2025, PAFR=1, PLANDMARK=0, all judges) returned 97 records.
  - Record fields: APPL_IN, ATTACHMENTS, AUTHOR_JUDGES, BENCHNAME, CASECODE, CASENO, CREATEDDATE, CSNO, DDATE, ISLANDMARK, JUDGENAME, O_AFR, O_CITATION, O_CITATION_IMP, O_DDATE, O_ID, O_IHC_HEADNOTE, O_REMARKS, O_SC_AFR, O_SC_ATTACHMENTS, O_SC_CITATION, O_SC_CITED, O_SC_DDATE, O_SC_HEADNOTE, O_SC_RESULT, O_SC_STATUS, O_SUBJECT, O_UNDERSECTION, PARTIES, PRNTCASECODE, RPTTYPE, TITLE, USERNAME, VAFR.
  - Decision years in the result: 2025 (63), 2026 (34). PYEAR therefore appears to filter by case-registration year.
  - 24 of 97 had a real citation; the rest were "Citation Awaited".
  - [srchDecisionClms](https://mis.ihc.gov.pk/ihc.asmx/srchDecisionClms) (fetched once)
- **PDF headers.** `GET` on the attachment returned 200 with `Content-Type: application/pdf`, `Last-Modified: Tue, 20 Oct 2026 03:56:18 GMT`, `Server: Microsoft-IIS/10.0` and `Access-Control-Allow-Origin: *`. The file is PDF 1.5, 6 pages. [sample PDF](https://mis.ihc.gov.pk/attachments/judgements/209540/1/Muhammad_Usman_v_FoP_WP_No_1553_of_2026__J_Arbab_Muhammad_Tahir__Approved_for_Reporting_639280833781874862.pdf) (fetched)
- **PDF text.** `pdftotext` extracted 12,776 characters, beginning "Form No: HCJD/C-121 ORDER SHEET IN THE ISLAMABAD HIGH COURT, ISLAMABAD (JUDICIAL DEPARTMENT) W.P. No.1553-2026 Muhammad Usman Versus Federation of Pakistan and others … Arbab Muhammad Tahir, J.- The petitioner…". Paragraphs are numbered 2–9, and there are page headers "Page - 2 / W.P. No.1553-2026". The text ends with "Approved for reporting." The text includes a litigant's full **IBAN**. (Own extraction of fetched PDF)
- **Filename pattern.** Filenames include a long numeric suffix such as `_639280833781874862`, consistent with .NET DateTime ticks, under `/attachments/judgements/<record id>/<n>/`. (Fetched JSON)
- **Third-party copy.** A private site (Legalise) hosts IHC judgments with keyword/bench/year search. [legalise-codex](https://legalise-codex.pages.dev/digest/islamabad-high-court-judgments-search-legalise) (snippet only, secondary)

### Inferences (analysis)
- **What is published.** The listing covers reported (AFR) and "important"/landmark judgments, per the page's own words, plus a broader "Search Judgements / Orders" over decisions. Whether *all* orders are exposed via `srchDecision*` was not tested. The data model also tracks SC appeal results (`O_SC_RESULT`, `O_SC_CITATION`), useful for "subsequent history" features.
- **Neutral citation.** None is visible. Citations are commercial reporter citations (CLC, YLR, etc.) filled in after reporting. Case number format: `<Case Type>-<No>-<Year>` in the JSON (e.g. "Intra Court Appeal-362-2025") vs `W.P. No.1553-2026` on the PDF face.
- **Feasibility: technically high.** There is no robots.txt, no CAPTCHA and no login, and JSON endpoints are called by the public pages. PDFs are directly downloadable from URLs given in JSON, but not guessable. A per-judge × reported/important sweep (Juges_GA, then srchDecisionClms) or a year sweep could enumerate the published set.
- **Risks.**
  - The endpoints are undocumented internal services, not a published API.
  - The disclaimer says content is "for information only" and not to be relied on "for official purposes". The product should present these as court-published copies, not certified copies.
  - The IIS server is single-instance and fragile (CallSer.js error messages ask users to contact the IT in-charge). Strict rate limiting (≤1 req/2–5 s, off-peak) is advisable.
  - Personal data (bank account numbers, names) appears in judgments, so a privacy/redaction policy is needed.
  - Seeking written permission from the IHC Registrar/IT is still advisable.
- **Format.** Born-digital text PDFs (verified in 1 sample). Older or former-judge PDFs may be scans; untested.

### Gaps
- Earliest year and total count of IHC judgments online are unknown. Only one year (2025, AFR) was queried, to avoid load. The court was established in 2010 (background knowledge, not verified this session).
- The "Case Law Management System" target URL and the frmRdJgmnt viewer were not inspected.
- No Urdu judgments, RSS feed, neutral citation or terms-of-use page was found. ihc.gov.pk root robots.txt is absent, so legal permission rests on the disclaimer only.
- IHC digitisation news (paperless/e-court) was seen only in snippets; no dated primary announcement was verified ([ARY](https://arynews.tv/ihc-launches-smart-paperless-digital-court), snippet only).

---

## 4. Cross-court legal/permission questions and remaining gaps

### Takeaway
None of the three courts publishes a licence or terms of reuse for judgments. The SC is the only one with an explicit machine-readable restriction: an AI-crawler block plus `ai-train=no`. The FSC permits crawling. The IHC is silent (no robots.txt) but disclaims official reliance.

### Cited Findings
- SC robots: `Content-Signal: search=yes,ai-train=no,use=reference`; ClaudeBot, anthropic-ai and GPTBot disallowed. [scp.gov.pk/robots.txt](https://scp.gov.pk/robots.txt) (fetched)
- SC "Terms of Use" link is `href="#"`. [JudgmentsSearch](https://scp.gov.pk/JudgmentsSearch) (fetched)
- FSC robots allow all except /wp-admin/. [robots.txt](https://www.federalshariatcourt.gov.pk/robots.txt) (fetched)
- IHC has no robots.txt (404) and shows a disclaimer. [frmJgmnt](https://mis.ihc.gov.pk/frmJgmnt) (fetched)

### Inferences
- **Recommended collection posture:**
  - **FSC:** crawl the listing, polite and rate-limited.
  - **IHC:** use the JSON listing with strict rate limits and seek written permission.
  - **SC:** do not automate. Request permission or a data feed from the SC. Meanwhile, at most poll LatestJudgments metadata manually or at low frequency, and do not use SC content for model training given `ai-train=no`.
- Whether Pakistani copyright law exempts reproduction of court judgments was **not researched this session**. It needs a separate statute check (Copyright Ordinance 1962) before relying on it.

### Gaps
- Statutory copyright status of judgments in Pakistan (Copyright Ordinance 1962 exceptions) is unverified.
- The Federal Constitutional Court (fccp.gov.pk, created Nov 2025) is now a federal-level court issuing constitutional judgments. Its site is a JS SPA whose data API was not examined. It needs its own profile.
- SC Annual Reports and LJCP reports with judgment-count statistics were not fetched.
- The NJPMC AI guidelines text (adopted 11 Feb 2026 per secondary reports) was not fetched.
