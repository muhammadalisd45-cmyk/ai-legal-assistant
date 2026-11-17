# Official statute sources: Khyber Pakhtunkhwa (incl. ex-FATA/PATA), Balochistan, Gilgit-Baltistan, AJK, plus amendment history and point-in-time law

Research date: 2026-11-12. Unless marked otherwise, "fetched" means I retrieved the URL directly (curl, or WebFetch-equivalent) on 2026-11-12. "Snippet only" means the information came from a web-search result summary and the page itself was not fetched. All counts are from my own parsing of the fetched HTML on 2026-11-12 and may change. PDF checks used `pdftotext` on single files I downloaded; this was spot-checking only, not bulk downloading.

## Source inventory (all jurisdictions)

### Takeaway
Each jurisdiction has one primary official source. KP and Balochistan have searchable "Code" portals run by their Law departments. For AJK, the Law Department's WordPress site hosts per-Act and per-Ordinance PDFs plus compiled Law Code volumes. GB has no code portal, only short download lists on the Assembly and government portals. Legislature websites supplement the codes and are often more current (KP) or less current (Balochistan).

### Cited Findings: inventory table

| Title | URL | Organisation | Category | Date / last updated (as observed 2026-11-12) | Credibility | Access status |
|---|---|---|---|---|---|---|
| KP Code (KP Laws Site, "KPLS") | https://kpcode.kp.gov.pk/ (list: /homepage/list_all_law; detail: /homepage/lawDetails/{id}; PDFs: /uploads/) | Law, Parliamentary Affairs & Human Rights Dept, Govt of KP | Official consolidated statute portal (Acts, Ordinances, Regulations, Rules, 1 Notification) | Newest items: KP Acts VII–IX of 2026 (promulgated 07-05-2026); sitemap lastmod 2025-10-02; sample PDF ModDate 2026-10-14 | High (official) | Fetched |
| KP Code robots.txt | https://kpcode.kp.gov.pk/robots.txt | same | robots | — | — | Fetched: `User-agent: * / Allow: / / Sitemap: https://kpcode.kp.gov.pk/sitemap.xml` |
| Provincial Assembly KP: Acts | https://www.pakp.gov.pk/act/ ; https://www.pakp.gov.pk/all-acts/ | Provincial Assembly of KP | Legislature acts list + gazetted-copy PDFs | Lists up to KP Act No. XXI of 2026 (passed 24 Aug 2026, enforcement 2026-08-31) | High (official) | Fetched (200); robots.txt returned 404 |
| Balochistan Code (Balochistan Laws Site) | https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1 ; detail Document.aspx?wise=opendoc&docid=…&docc=… ; PDFs /lawdir/{guid}.pdf | Law & Parliamentary Affairs Dept Balochistan; "Maintained by Science & IT Department Balochistan" | Official statute portal (Acts, Ordinances, Rules, Regulations, Gazette Notifications, Policies) | Latest promulgation date in listing: Thu Nov 05, 2026 | High (official) | Fetched |
| Balochistan Code robots.txt | https://balochistancode.gob.pk/robots.txt | same | robots | — | — | Fetched: 24 comment lines only (content-signal preamble), no directives |
| Balochistan Code Urdu UI | http://balochistancode.gob.pk/urdu/ | same | Urdu interface | — | High | Fetched (301 to /urdu/, then 200) |
| Provincial Assembly of Balochistan: Acts | https://pabalochistan.gov.pk/acts | Provincial Assembly of Balochistan | Legislature acts list + PDFs | Latest listed: Act XV of 2026 (assented 19/05/2026) | High | Fetched (200). Old URL https://pabalochistan.gov.pk/new/acts/ returns 301 to /public/new/acts, which is a 404 |
| Balochistan Printing & Stationery Dept | https://printing.balochistan.gov.pk/ (/downloads/) | Govt of Balochistan | Gazette printer | — | High | Fetched home and downloads (no gazette PDFs found on /downloads/); robots fetched |
| blncode.pitb.gov.pk | http://blncode.pitb.gov.pk / https://… | Unknown (PITB subdomain) | Linked from Sindh Code per prior context | — | Unknown | Inaccessible: DNS resolves to 103.226.216.192, but TCP connect fails on ports 80 and 443 ("Failed to connect … after 21056 ms") |
| Gilgit-Baltistan Assembly: Acts | https://gbassembly.gbit.gov.pk/pages/acts | GB Assembly | Legislature acts list | Year groups 2020–2025; contains test rows | Medium (official but buggy) | Fetched page; 3 of 3 sampled PDFs return 404; robots: `User-agent: * Disallow:` |
| gba.gov.pk/acts/ | https://gba.gov.pk/acts/ | GB Assembly (older domain) | Acts list | — | — | Inaccessible: TLS error `SEC_E_CERT_EXPIRED` (certificate expired) |
| gba.gbit.gov.pk/acts/ | https://gba.gbit.gov.pk/acts/ | GB Assembly (older domain) | Acts list | — | — | Inaccessible: HTTP 404 |
| Government of GB portal: Laws, Acts, Downloads | https://gilgitbaltistan.gov.pk/pages/laws ; /pages/acts ; /pages/downloads | Government of Gilgit-Baltistan | Small download lists (GB Order 2018, rules, ~15 Acts) | GB Order 2018 PDF Last-Modified 12 Nov 2024 | High (official), low coverage | Fetched; robots.txt 404 |
| AJK Law Department (law.gok.pk) | https://law.gok.pk/acts/ ; /ordinance/ ; /adopted-laws-in-ajk/ ; /publications/ | Law, Justice, Parliamentary Affairs & Human Rights Dept, AJK | Official per-Act and per-Ordinance PDFs, Law Code volumes I–XIV, Interim Constitution | Latest Act: Act V of 2025 (Gazette dated 27 Aug 2025); latest Ordinance: Ordinance III of 2026 | High | Fetched; robots: WordPress default (`Disallow: /wp-admin/`) |
| AJK Legislative Assembly: Acts | https://ajkassembly.gok.pk/acts/ | AJK Legislative Assembly | Acts list (2019, 2022, 2023) + rules PDFs | One upload dated 2026/10 (Privileges Act 1974 PDF) | High, low coverage | Fetched; robots: `User-agent: * Disallow:` (Yoast) |
| law.ajk.gov.pk | https://law.ajk.gov.pk/assets/lawlibrary/… | AJK Law Dept (legacy host) | Linked PDF | — | — | Not fetched (seen only as a link on law.gok.pk) |
| Pakistan Code | https://pakistancode.gov.pk/english/ | Ministry of Law & Justice (federal) | Federal consolidated code (cross-cutting check) | — | High | Fetched home + 1 law page; robots: `User-agent: googlebot / Disallow: /pdffiles/` |
| Dawn: GB Assembly tenure | https://www.dawn.com/news/1957215 | Dawn (press) | News | — | Medium | Snippet only |
| Dawn: Action in Aid of Civil Power Ordinance | https://www.dawn.com/news/1505809 | Dawn | News | — | Medium | Snippet only |
| KP Assembly bill page: Continuation of Laws FATA Bill 2019 | https://pakp.gov.pk/bill/the-khyber-pakhtunkhwa-continuation-of-laws-in-the-erstwhile-federally-administered-tribal-areas-bill-2019 | PA KP | Bill record | — | High | Snippet only |
| visitgilgitbaltistan.gov.pk files; fwegb.gov.pk rules; sacgb.gov.pk | (see GB section) | GB Tourism / Forest Dept / Supreme Appellate Court GB | Departmental hosting of GB Acts/Rules | — | Medium-High | Snippet only |
| UNEP LEAP / FAOLEX GB entries | https://leap.unep.org/en/countries/pk/national-legislation/gilgit-baltistan-forest-act-2019 | UNEP/FAO | Secondary index | — | Medium (secondary) | Snippet only |

### Inferences
- For complete current coverage, a product needs a code portal and the legislature's acts list for each of KP and Balochistan, because the two sources lag each other in opposite directions (see below). For AJK, law.gok.pk is the primary source. GB needs a patchwork of sources and still has gaps.

### Gaps
- No official online gazette archive was found for KP, Balochistan, GB or AJK (details below).

## Khyber Pakhtunkhwa: KP Code (kpcode.kp.gov.pk) and KP Assembly

### Takeaway
KP Code says it holds law in "revised" (consolidated) form, with Acts, Ordinances, Regulations and Rules. On 2026-11-12 it reported 969 records across five categories, but its "All Laws" list shows only 575. That explains the earlier figure of about 575 from the letter pages; the id range up to about 1,623 also includes Rules, deleted ids and gaps. The portal lags the Assembly by roughly six months: the Assembly lists KP Acts up to No. XXI of 2026 (Aug 2026), but KP Code's newest Acts are Nos. VII–IX of 2026 (May 2026).

### Cited Findings
- **Stated total on the "All Laws" list.** https://kpcode.kp.gov.pk/homepage/list_all_law shows "Total Records Found : 575". It pages 15 per page, and the last page offset is /list_all_law/0/15/570, which holds 5 items. The ordering is newest id first: the top item is lawDetails/1623, "The KP Province Speaker and Deputy Speaker's (Immunities, Privileges, Salaries and Allowances) Act, 2026 … ACT NO. VIII OF 2026 | Promulgation Date: 07-05-2026". [list_all_law](https://kpcode.kp.gov.pk/homepage/list_all_law) (fetched)
- **Per-category totals from Advanced Search.** The form POSTs to /homepage/advance_search_process and redirects (302) to /homepage/advance_search_process_law_rule_urdu/{base64 of query}, for example `bWFpbl9jYXRlZ29yeV9pZD01` = "main_category_id=5".
  - Acts = 422
  - Ordinance = 125
  - Notifications = 1
  - Regulation = 44
  - Rules = 377
  - Sum = 969 [advance_search](https://kpcode.kp.gov.pk/homepage/advance_search) (fetched)
- **Department filter.** The Advanced Search department dropdown has about 57 department options, including "Peshawar High Court" and "Khyber Pakhtunkhwa Public Service Commission". [advance_search](https://kpcode.kp.gov.pk/homepage/advance_search) (fetched)
- **What the id gaps are.** Spot checks of detail ids:
  - id 1608 = "Forest Development Fund (Management & Utilization) Rules, 2006", Main Category: Rules
  - id 1620 = "THE KHYBER PAKHTUNKHWA ADVOCATE-GENERAL (TERMS AND CONDITIONS OF SERVICE) RULES, 2005", Rules
  - ids 5 and 1616 return a page shell with no law (no title, no PDF)

  [lawDetails/1608](https://kpcode.kp.gov.pk/homepage/lawDetails/1608), [lawDetails/1620](https://kpcode.kp.gov.pk/homepage/lawDetails/1620), [lawDetails/1616](https://kpcode.kp.gov.pk/homepage/lawDetails/1616) (fetched)
- **Consolidation claim (FAQ).**
  - "The KPLS is an online official version of the primary legislation in force in the KP (Pakistan)."
  - "KPLS is managed by the Government of the KP, Law and Parliamentary Affairs Department."
  - "KPLS shall carry most (but not all) types of legislation, both primary and secondary. Legislation is held in 'revised' form. This means that amendments made by subsequent legislations are incorporated into the main text."

  [FAQ](https://kpcode.kp.gov.pk/homepage/faq) (fetched)
- **Overview page.** It says the site "aims at providing free access to the KP laws (principal/substantive as well as delegated/subordinate). Arrangements are on ground to keep the PLS updated on regular basis." It also names "Pervaiz Khattak, Chief Minister", so the text is stale. [Overview](https://kpcode.kp.gov.pk/homepage/overview) (fetched)
- **Footer and disclaimer.** "This site is developed only for informational purposes and is subject to the Disclaimer. © 2026 Law & Parliamentary Affairs Department, Government of KP". [lawDetails/1623](https://kpcode.kp.gov.pk/homepage/lawDetails/1623) (fetched)
- **Views.** The portal offers Alphabetical, Department wise, Chronological, Category wise (/homepage/search_by_category/{id}), Advanced Search and "Laws in Urdu". [list_all_law](https://kpcode.kp.gov.pk/homepage/list_all_law) (fetched)
- **Urdu.** The "Laws in Urdu" page is headed "گزٹ نوٹیفیکیشن کی تاریخ وار فہرست سازی" (chronological listing of gazette notifications). It has 96 year links (/homepage/search_by_year_urdu/{id}), one of them labelled "2047", which looks like a data-entry error. Three sampled year pages (ids 47, 78, 80) returned empty responses. [Urdu](https://kpcode.kp.gov.pk/homepage/urdu) (fetched)
- **Repealed marking.** Detail pages include CSS for a `.repealed` badge (red, animated), but no `.repealed` element appeared on any sampled detail page. That includes the two Continuation of Laws Acts (ids 1426, 1438), which press reports say were withdrawn (see FATA section). [lawDetails/1438](https://kpcode.kp.gov.pk/homepage/lawDetails/1438) (fetched)
- **PDF spot checks.** Both sampled PDFs are born-digital with a text layer and an iTextSharp watermark:
  - The KP Act VIII of 2026 PDF has Producer "Microsoft Word 2013; modified using iTextSharp 5.5.10" and ModDate 2026-10-14; the first 3 pages give 7,279 characters of text.
  - The Forest Development Fund Rules 2006 PDF (ModDate 2025-07-25) shows consolidation footnote markers: "GOVERNMENT OF 1[Khyber Pakhtunkhwa] ENVIRONMENT DEPARTMENT … THE 5[Khyber Pakhtunkhwa] FOREST DEVELOPMENT FUND …".

  [PDF](https://kpcode.kp.gov.pk/uploads/The_KP_Province_Speaker_and_Deputy_Speakers_Immunities_Privileges_Salaries_and_Allowances_Act_2026.pdf), [PDF](https://kpcode.kp.gov.pk/uploads/Khyber_Pakhtunkhwa_Forest_Development_Fund_Management_and_Utilization_Rules_2006Watermarked.pdf) (fetched)
- **Sitemap.** https://kpcode.kp.gov.pk/sitemap.xml contains a single `<loc>` (homepage), lastmod 2025-10-02T11:26:00+00:00. [sitemap](https://kpcode.kp.gov.pk/sitemap.xml) (fetched)
- **KP Assembly acts list.** It gives columns "Sr. # | Act # | Title | Passage Date | Enforcement Date". Entries include:
  - "Khyber Pakhtunkhwa Act No. XX of 2026 The Khyber Pakhtunkhwa Promotion of Digital Payments Act, 2026 21 Aug 2026 2026-08-31"
  - "Act No. XXI of 2026 … Fiscal Resposibility and Debt Managment (Amenment) ACT,2026 24 Aug 2026"
  - "Act No. XVI of 2026 The Hindu Marriage (Khyber Pakhtunkhwa) (Amendment) Act, 2026"
  - "Act No. XI of 2026 The Khyber Pakhtunkhwa Educational Testing and Evaluation Agency Act, 2026"

  The page links PDFs under /wp-content/uploads/, including files suffixed "-GC.pdf" (gazetted copy). The menu has "Constitution (Upto 27th Amendment)" and "Previous Acts". The footer reads "All Rights Reserved, Provincial Assembly of Khyber Pakhtunkhwa". [PAKP Acts](https://www.pakp.gov.pk/act/) (fetched)
- **KP Code is missing these 2026 Acts.** Title searches on KP Code:
  - "Digital": no records
  - "Hindu Marriage": no records
  - "Educational Testing": 1 record, the "[KHYBER PAKHTUNKHWA] EDUCATIONAL TESTING AND EVALUATION AGENCY ORDINANCE, 2001" (no 2026 Act)
  - "Finance Act": 41 records, newest "THE KHYBER PAKHTUNKHWA FINANCE ACT, 2025 … ACT NO. XVIII OF 2025" (no Finance Act 2026, which is Act XIII of 2026 on the Assembly list)

  [KP Code advanced search](https://kpcode.kp.gov.pk/homepage/advance_search) (fetched)

### Inferences
- **The ~575 vs ~1,623 discrepancy.**
  - 575 is the stated size of the "All Laws" list, which appears to cover primary legislation only. 575 ≠ Acts 422 + Ordinances 125 = 547, so about 28 other records (possibly some Regulations or the Notification) are included. I could not determine which.
  - The id space up to 1,623 also covers the 377 Rules and 44 Regulations. Those are reachable only through category or advanced search, not the All-Laws list.
  - The remaining ~650 ids appear to be deleted or unpublished records, which render as empty shells.
  - A crawler should therefore enumerate the category searches (Rules = 377, Regulation = 44) as well as the All-Laws list, or walk ids 1–1623 and discard empty pages.
- **Consolidation.** KP Code is the only source in scope that publishes consolidated (as-amended) texts, using bracketed footnote markers. It does not show versions or history, and amendment Acts are not reliably listed separately.
- **Currency.** KP Code lags the Assembly by about six months (Acts X–XXI of 2026 missing). The KP Assembly site is needed for as-enacted recent Acts and gazetted copies.
- **Repeal status.** Status is unreliable on KP Code: a repealed-badge feature exists in the CSS, but it was not observed in use.

### Gaps
- KP Code: the disclaimer page itself was not located or fetched. There is no explicit "last updated" date per law. The Urdu year pages returned empty responses, so Urdu coverage is unverified. The definition of the 575-record "All Laws" set is unexplained.
- I did not count the KP Assembly "All Acts" archive: the /all-acts/ page returned no PDF links in static HTML (likely loaded by script or through tenure selection).

## Balochistan: Balochistan Code (balochistancode.gob.pk) and Balochistan Assembly

### Takeaway
Balochistan Code lists 1,790 published entries on 2026-11-12, embedded in one alphabetical page: 410 Acts, 172 Ordinances, 637 Rules, 34 Regulations, 497 Gazette Notifications and 40 Policies. About 111 are duplicate titles. Texts are as-enacted: amendment instruments are separate entries, with no consolidation and no repeal flags. Recent PDFs can be image-only scans. The code is more current than the Assembly's acts list.

### Cited Findings
- **Listing data.** The alphabetical page (https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1, 659 KB) embeds all entries in a hidden field `datafield`. I parsed 1,790 entries with 1,790 unique docids (min 2, max 2,221). Section counts:
  - RULES 637
  - GAZETTE NOTIFICATION 497
  - ACTS 410
  - ORDINANCE 172
  - POLICIES 40
  - REGULATIONS 34

  Every entry shows "Status: Published". [Alphabetical](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1) (fetched)
- **Duplicates and data quality.**
  - Normalising titles gives 1,679 unique titles for 1,790 entries.
  - 29 titles contain ".doc", for example "Al- Hamd University Act 2005.doc", which appears alongside "Al- Hamd University Act 2005".
  - "Baln Safe Cities Authority Act, 2026" appears twice (docids 2166, 2167).
  - "Balochistan Establishment of Special Court(s) (Overseas Pakistanis Property) Act, 2025" appears four times (docids 2143–2146).
  - Some entries carry the department label "Bank" (for example docid 2206).

  [Alphabetical](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1) (fetched)
- **Amendment handling.** 673 of 1,790 titles contain "amend". Amendments are listed as separate entries under an "(Amendment-YYYY)" naming pattern, for example "The Balochistan Civil Servents Act, 1974 (Amendment-2025) … Act No. IX of 2025" and "The Balochistan Government Rules of Business, 2012 (Amendment-2026)". Only 14 titles contain "repeal". [Alphabetical](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1) (fetched)
- **Currency.** Recent entries include:
  - "The Balochistan Citizen Facilitation and Good Governance Act, 2026 … Act No. XXIV of 2026 | Promulgation Date: Fri Oct 16, 2026"
  - "The Balochistan Employment of Children … (Amendment-202[6]) … Act No. XIX of 2026 | Tue Sep 08, 2026"
  - A Rules entry with "Promulgation Date: Thu Nov 05, 2026"

  Entries by promulgation year: 2025 = 92, 2026 = 74. [Alphabetical](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1) (fetched)
- **Navigation.** Views are Alphabetical, Departmental, Chronological, Thematic and Categorical. Chronological filters use dst codes: 3 = Acts, 5 = Ordinances, 1 = Service Rules, 2 = General Rule, 7 = Gazette Notifications, 8 = Bye Laws, 9 = Regulations, 10 = Policies. Free-text search is at laws_rules.aspx?wise=Search&sphrase=…. [Home](https://balochistancode.gob.pk/) (fetched)
- **Detail pages.** A detail page needs both docid and docc. Using docid alone with docc=0 returned an ASP.NET "Runtime Error". With the correct pair, for example Document.aspx?wise=opendoc&docid=2206&docc=2047, the page shows the title, a "Download" link to /lawdir/{guid}.pdf, and no metadata about status or amendments. [docid 2206](https://balochistancode.gob.pk/Document.aspx?wise=opendoc&docid=2206&docc=2047) (fetched)
- **PDF spot checks.**
  - The Citizen Facilitation and Good Governance Act 2026 (/lawdir/32451bb8-….pdf, 3.39 MB) has no extractable text (3 characters), so it is a scanned or image PDF.
  - "The Caste Disabilities Removal (West Pakistan Amendment) Act, 1963" (/lawdir/2a5fbc7b-….pdf, 17 KB) is text-based: "(W.P. Act X of 1963) CONTENTS SECTIONS … 2. Amendment of section 1 of Act XXI of 1850."

  [PDF 2026](http://balochistancode.gob.pk/lawdir/32451bb8-f114-4d06-a95e-fc3f533393a6.pdf), [PDF 1963](http://balochistancode.gob.pk/lawdir/2a5fbc7b-8186-41e1-b3d7-7d2213fb85a4.pdf) (fetched)
- **About page.** "The Balochistan Laws Site (BLS) has been developed and is managed by Government of Balochistan, Law and Parliamentary Affairs Department… Presently, the Site contains more than three hundred substantive laws. The process of dove-tailing delegated legislation with these laws is currently in hand." The page also names "Jam Mir Kamal Khan Chief Minister", so the text is stale. Footer: "All rights reserved by Law & parliamentary affairs department Balochistan , Maintained by Science & IT Department Balochistan." [About](https://balochistancode.gob.pk/Aboutus.aspx) (fetched)
- **Urdu interface.** http://balochistancode.gob.pk/urdu/ serves a fully Urdu UI (حروف تہجی کے لحاظ سے, محکمانہ لحاظ سے, …). [Urdu](http://balochistancode.gob.pk/urdu/) (fetched)
- **robots.txt (Balochistan Code).** The file contains only a commented content-signal preamble and no directives:
  - "(c) If the website operator does not include a content signal for a corresponding use, the website operator neither grants nor restricts permission via content signal with respect to the corresponding use."
  - "ai-input: inputting content into one or more AI models (e.g., retrieval augmented generation, grounding…)"
  - "ai-train: training or fine-tuning AI models."
  - "ANY RESTRICTIONS EXPRESSED VIA CONTENT SIGNALS ARE EXPRESS RESERVATIONS OF RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION DIRECTIVE 2019/790…"

  [robots](https://balochistancode.gob.pk/robots.txt) (fetched)
- **Balochistan Assembly acts.**
  - https://pabalochistan.gov.pk/acts returns 200 (617 KB) with 428 PDF links under /storage/{n}/….pdf.
  - Columns are "Act No | Act Title | Passed on | Assented on | Type". Acts are grouped by year from 1972 to 2026 (14 Acts parsed for 2026, highest No. XV: "THE BALOCHISTAN PRISONS AND PRISONER'S CORRECTIONAL SERVICE ACT, 2026, ACT NO. XV OF 2026. 14/05/2026 19/05/2026").
  - The same site posts "2009 Recruitment Rules with all amendments up to 24th August, 2026" and "Rules of Procedure (Amended up to 22nd Dec 2025 )".
  - The legacy URL /new/acts/ redirects (301) to /public/new/acts, which returns 404.

  [PAB Acts](https://pabalochistan.gov.pk/acts) (fetched)
- **pabalochistan.gov.pk robots.txt.** "User-agent: * / Disallow:" (allows all). [robots](https://pabalochistan.gov.pk/robots.txt) (fetched)
- **Printing & Stationery Dept robots.txt.** It declares "Content-Signal: search=yes,ai-train=no,use=reference". It lists many AI crawlers with Disallow, including ClaudeBot, anthropic-ai, Claude-Web, GPTBot, CCBot, Google-Extended and meta-externalagent. Its /downloads/ page had no PDF links. [robots](https://printing.balochistan.gov.pk/robots.txt), [Downloads](https://printing.balochistan.gov.pk/downloads/) (fetched)
- **What the Printing Dept prints.** According to its About page, it prints Gazettes, Ordinances, Acts, Rules and Assembly proceedings. [About](https://printing.balochistan.gov.pk/?p=20) (snippet only)

### Inferences
- **The ~1,790 count.** About 1,680 distinct titles span six instrument types. The code holds 410 + 172 = 582 Acts and Ordinances, of which roughly 40% of all entries are amendment instruments. Distinct principal laws are therefore far fewer.
- **Consolidation.** Balochistan Code is an as-enacted repository, so a product would have to build its own consolidations.
- **Rights posture.** The Balochistan government's printing-department host explicitly opts out of AI training and blocks Anthropic crawlers. The Code host is silent. Treat Balochistan as a jurisdiction where AI use needs a careful rights review.
- **Currency.** The Code (Act XXIV of 2026, Oct 2026) is ahead of the Assembly's list (Act XV of 2026, May 2026).

### Gaps
- What blncode.pitb.gov.pk is could not be resolved: the host was unreachable. PITB is presumably the Punjab Information Technology Board, which suggests a PITB-built Balochistan code (possibly a staging or alternate site). This is an inference, not verified, and I did not re-fetch the Sindh Code page that links to it.
- No online archive of the Balochistan Gazette was found. The Code's "Gazette Notification" category (497 entries) is the closest substitute.
- The proportion of scanned PDFs is unknown (only 2 sampled).

## KP merged districts (ex-FATA/PATA): where extension and adaptation laws are published

### Takeaway
Instruments extending or continuing laws in the erstwhile FATA/PATA are published on KP Code, alongside legacy PATA Regulations. KP Code does not flag their later status, and I found no dedicated official compilation for the merged districts.

### Cited Findings
- **KP Code title searches.**
  - "Tribal" returns 27 records, including:
    - THE KHYBER PAKHTUNKHWA CONTINUATION OF LAWS IN THE ERSTWHILE FEDERALLY ADMINISTERED TRIBAL AREAS ACT, 2019 (lawDetails/1438)
    - …ERSTWHILE PROVINCIALLY ADMINISTERED TRIBAL AREAS ACT, 2018 (lawDetails/1426)
    - THE FEDERALLY ADMINISTERED TRIBAL AREAS DEVELOPMENT AUTHORITY REGULATION (REPEAL) ACT, 2020
    - three 2022 regularisation Acts for erstwhile FATA employees
    - Provincially Administered Tribal Areas (Application Of Laws) Regulation, 1994
    - THE PROVINCIALLY ADMINISTERED TRIBAL AREAS (APPLICATION OF ELECTIONS LAW) REGULATION, 2001
    - The West Pakistan General Clauses (Extension to Tribal Areas) Regulation, 1961
    - Provincially Administered Tribal Areas Criminal Law (Special Provisions) Rules 1977
  - "Erstwhile" returns 5 records; "Continuation" returns 2.

  [KP Code](https://kpcode.kp.gov.pk/homepage/lawDetails/1438) (fetched)
- **PDFs.** Both Continuation Acts have PDFs on KP Code, for example /uploads/THE_KHYBER_PAKHTUNKHWA_CONTINUATION_OF_LAWS_IN_THE_ERSTWHILE_FEDERALLY_ADMINISTERED_TRIBAL_AREAS_ACT_2019.pdf. Neither detail page shows a repealed badge. [lawDetails/1426](https://kpcode.kp.gov.pk/homepage/lawDetails/1426) (fetched)
- **Assembly record.** The KP Assembly bill page records the Continuation of Laws (FATA) Bill 2019 as introduced and passed on 29 Apr 2019. [PAKP bill](https://pakp.gov.pk/bill/the-khyber-pakhtunkhwa-continuation-of-laws-in-the-erstwhile-federally-administered-tribal-areas-bill-2019) (snippet only)
- **Press report of withdrawal.** According to press coverage, the Advocate General told the Peshawar High Court that the challenge had become infructuous because the Action (in Aid of Civil Power) Ordinance, 2019 had been promulgated and the two continuation laws "withdrawn". [Dawn](https://www.dawn.com/news/1505809); [The News](https://thenews.com.pk/print/528142-ag-tells-phc-actions-in-aid-of-civil-powers-extended-to-entire-kp) (snippet only)

### Inferences
- Only KP Code is a structured source for merged-district instruments. Because it lacks repeal and status metadata, a product could present the 2018/2019 Continuation Acts as in force when their status is disputed or changed. Status must be curated manually.
- Federal-era FATA Regulations (for example under former Art. 247) would sit on Pakistan Code or in historic federal gazettes. I did not verify this in this session.

### Gaps
- The current legal status of the 2018/2019 Continuation Acts is not verified from an official repeal instrument.
- I found no official list of which federal and provincial laws were extended to the merged districts, or when.
- The KP Gazette notifications extending specific laws to the tribal districts were not found online.

## Gilgit-Baltistan: official sources, the GB Order, and federal laws extended to GB

### Takeaway
GB has no official statute code or portal. Official texts are scattered across three sites:
- the GB Assembly Acts page: buggy, with test rows, placeholder assent dates and broken PDFs
- the Government of GB portal: about 15 Acts and a handful of rules
- departmental sites

Two older Assembly domains are down (expired TLS certificate, or 404). The Government of GB Order 2018 is hosted officially as a text PDF. The federal-law extension mechanism lies in s.60(3) of the Order and in adaptation instruments, but I found no consolidated list of federal laws extended to GB.

### Cited Findings
- **GB Assembly Acts page (gbassembly.gbit.gov.pk/pages/acts).**
  - The page groups Acts under "Year: 2025, 2023, 2022, 2021, 2020", with 23 "Act No." rows and 28 PDF links.
  - The 2025 rows are test data: "1 Act No.III of 2025 test-3 Friday, 12th December, 2025 … 2 Act No.III of 2025 test-2".
  - Several 2021 Acts show "Thursday, 12th November, 2026" (the date of my fetch) in a date column, for example "Act No. X of 2021 THE MEMBERS GILGIT BALTISTAN ASSEMBLY(Salaries, Allowances, and Privileges) ACT-2021.pdf Wednesday, 29th June, 2022 Thursday, 12th November, 2026 Private".
  - One entry is titled "THE GILGIT-BALTISTAN REVENUE AUTHORITY BILL 2022" under "Act No.I of 2023".

  [GB Assembly Acts](https://gbassembly.gbit.gov.pk/pages/acts) (fetched)
- **GB Assembly PDFs.** All three sampled PDF links returned HTTP 404 (Laravel "Not Found"):
  - …/acts/2023-02-08 05:12:18the-gb-public-procurement-act-2021.pdf
  - …/acts/2025-04-17%2008:20:27service-tribunal-amendment-act-2022.pdf
  - …/acts/servicetribunalamendmentact.pdf

  Filenames contain spaces and colons. [GB Assembly](https://gbassembly.gbit.gov.pk/pages/acts) (fetched)
- **Older domains.** https://gba.gov.pk/acts/ fails with "SEC_E_CERT_EXPIRED … The received certificate has expired". https://gba.gbit.gov.pk/acts/ returns 404. (fetched; errors recorded)
- **Government of GB portal, Laws page.** "Law Downloads": GB Order 2018 (listed twice), GB Staff Vehicles (use & maintenance) Rules 2021, GB Medical Attendant Rules, GB Procurement Rules 2022. [Laws](https://gilgitbaltistan.gov.pk/pages/laws) (fetched)
- **Government of GB portal, Acts page.** "Act Downloads" (15):
  - GB Council Adaptation of Laws Act 2012; GB Council Adaptation of Laws (Amendment) Act 2014
  - GB Finance Act 2024; GB IT Board Act 2024
  - Civil Servants Act 2011; GB Civil Servants Act (Amendment) 2019
  - PEC-Act-1976
  - The Ministers Gilgit Baltistan Salaries Allowances…
  - Forest Amendment Act 2020; Compulsory Education Act 2020; Induction Regularization of PPHI…
  - Travel Agencies Tour Operators Ac[t]…; Tourist Guide Act 2020; Tobacco Control Act-2020
  - GB PPRA Act 2021

  The Downloads page also lists "Northern Areas Council Telecom Adaptation Order 2006". [Acts](https://gilgitbaltistan.gov.pk/pages/acts) (fetched)
- **GB Order 2018 PDF.** https://gilgitbaltistan.gov.pk/storage/downloads/GB%20Order%202018.pdf: Last-Modified Tue, 12 Nov 2024, 417,605 bytes, text-based (about 128k characters extracted).
  - Short title: "This Order may be called the Government of Gilgit-Baltistan Order, 2018."
  - s.60 "Legislative Powers": "(3) The Prime Minister shall have the powers to adopt any amendment in the existing laws or any new law in force in Pakistan subject to the legislative competence under sub-section (2)." Also "(4) If any provision of an Act of Assembly is repugnant to any provision of any law which the Prime Minister is competent to enact, then the law made by the Prime Minister … shall prevail…"
  - s.99 "Continuance of existing laws": "(1) … all laws which immediately before the commencement of this Order, were in force in Gilgit-Baltistan shall continue to be in force until altered, repealed or amended by an Act of the appropriate authority."

  [GB Order 2018](https://gilgitbaltistan.gov.pk/storage/downloads/GB%20Order%202018.pdf) (fetched)
- **GB Council Adaptation of Laws Act 2012 PDF.** 117 KB, no extractable text (4 characters), so it is scanned. [PDF](https://gilgitbaltistan.gov.pk/storage/downloads/GB%20Council%20Adaptation%20of%20Laws%20Act%202012.pdf) (fetched)
- **robots.txt.** gbassembly.gbit.gov.pk: "User-agent: * / Disallow:". gilgitbaltistan.gov.pk/robots.txt: 404. (fetched)
- **GB Assembly output (Dawn).** Dawn reported that the GB Assembly "adopted 63 Acts during its five-year tenure", including six federal ones. [Dawn](https://www.dawn.com/news/1957215) (snippet only)
- **Departmental hosting.** GB Acts and Rules also appear on departmental sites: Tourism (https://visitgilgitbaltistan.gov.pk/files/GB%20Tourist%20Guid%20Act.pdf), Forest/Wildlife/Environment (https://fwegb.gov.pk/rules/) and the Supreme Appellate Court GB (law digest, https://sacgb.gov.pk/publications/law%20digest.pdf). FAOLEX/LEAP indexes GB Acts as a secondary source. [visitgilgitbaltistan](https://visitgilgitbaltistan.gov.pk/files/GB%20Tourist%20Guid%20Act.pdf), [fwegb](https://fwegb.gov.pk/rules/), [LEAP](https://leap.unep.org/en/countries/pk/national-legislation/gilgit-baltistan-forest-act-2019) (snippet only)

### Inferences
- **Coverage.** Official online coverage of GB statutes is a small fraction of the corpus. The Assembly alone passed about 63 Acts in one tenure (Dawn), and the official pages list about 23 + 15 items, with dead PDFs. Building a complete GB corpus would need offline or gazette acquisition, FOI or RTI requests, or partnership with the GB Law and Prosecution Department.
- **Federal law in GB.** Federal laws apply in GB through adaptation or adoption (GB Order 2018 s.60(3), Council Adaptation of Laws Acts 2012/2014, sector Adaptation Orders such as Telecom 2006). Pakistan Code texts therefore cannot be assumed to apply in GB without an adaptation instrument.

### Gaps
- I did not locate a website for the GB Law and Prosecution Department or any GB statute code.
- No GB Gazette archive was found online (only a third-party Scribd copy of an extraordinary gazette was surfaced, snippet only).
- I did not verify the current constitutional status of the GB Order 2018: subsequent Supreme Court proceedings, any later "Governance Order" amendments, or the 2009 Empowerment and Self-Governance Order text, which I did not find on an official host.
- I found no official list of federal laws adapted or extended to GB, and the scanned Adaptation of Laws Act 2012 could not be read without OCR.

## Azad Jammu & Kashmir: official sources and the Interim Constitution 1974

### Takeaway
The AJK Law Department (law.gok.pk) is the best-covered official source in scope:
- about 1,015 Act PDFs and about 1,143 Ordinance PDF links, most bulk-uploaded in 2023 and current to Act V of 2025 and Ordinance III of 2026
- an "Adopted Laws" table (618 rows) and 14 compiled Law Code volumes
- the Interim Constitution 1974

Texts are as-enacted or gazette copies. Older items are scans; recent gazette copies have a text layer.

### Cited Findings
- **Acts page.** law.gok.pk/acts/ has columns "Title | ACT No. | Year". First rows:
  - "Azad Jammu and Kashmir University of Haveli Act, 2025 (Act V of 2025)"
  - "Azad Jammu and Kashmir Finance Act, 2025 (Act IV of 2025)"
  - "The Azad Jammu and Kashmir Mangla DAM Housing Authority Act 2025 (Act I of 2025)"
  - "Azad Penal Code(First Amendment)Act,2024 (Act VII of 2024)"

  I counted 1,015 PDF links. By upload folder: 2023 = 976, 2021 = 24, 2024 = 11, 2025 = 3, 2022 = 1. [AJK Acts](https://law.gok.pk/acts/) (fetched)
- **Ordinances page.** law.gok.pk/ordinance/ has 1,143 PDF links (2023 uploads = 1,124). The newest is "The Azad Jammu and Kashmir Finance (Amendment) Ordinance, 2026 (Ordinance III of 2026)". [AJK Ordinances](https://law.gok.pk/ordinance/) (fetched)
- **Adopted Laws page.** law.gok.pk/adopted-laws-in-ajk/ has HTML tables with 618 `<tr>` rows, headed "S.No. | Title | Act/Order/Resolution No. | Year". The list starts "1 The AK Courts and Laws Code, 1948. Reported from AJK Laws Code 1948". The final table ends "136. The AJ&K Income Tax (Adaptation and Validation) Act, 2017 (I of 2017) Adaptation". A row 134 note reads "(to adapt amendments made in Income Tax Ordinance, 2001 of Pakistan)". The word "repeal" appears 17 times. [Adopted laws](https://law.gok.pk/adopted-laws-in-ajk/) (fetched)
- **Publications page.** It lists "Volume I (1948-1962) … Volume XIII(20015-2017) Volume XIV(2018-2023)", the Law Department Manual 2016, the AJK State Judicial Policy 2018, the AJK Supreme Court Rules 2016 and the "AJ&K Interim Constitution,1974". It also links Pakistani laws hosted on punjabpolice.gov.pk (for example the Qanun-e-Shahadat Order 1984). [Publications](https://law.gok.pk/publications/) (fetched)
- **Volume PDFs.**
  - Volume XIII (https://law.gok.pk/wp-content/uploads/2021/06/Volume-XIII.pdf): 16,720,911 bytes, Last-Modified 19 Jun 2021.
  - Volume I (/2020/07/vol-1.pdf): 5,607,249 bytes, Last-Modified 16 Jul 2020.
  - Volume XIV links to "/2024/08/index-XIV-final.pdf" (filename suggests an index only).
  - Interim Constitution PDF (/2023/10/AJK-interim-constitution.pdf): 3,288,991 bytes, Last-Modified 26 Oct 2023.

  (HEAD requests, fetched)
- **PDF spot checks.**
  - The Haveli Act 2025 PDF is a text-layer gazette extract: "THE GAZETTE OF AZAD JAMMU & KASHMIR EXTRA ORDINARY GAZETTE PUBLISHED BY AUTHORITY V0L.LXXI Muzaffarabad Dated 27th August , 2025 No.269 … Law, Justice, Parliamentary Affairs and Human Rights Department".
  - A 2023 bulk upload ("The-Azad-Jammu-and-Kashmir-Shariat-Court-Amendment-Act-1995-ACT-XVI-OF-1995.pdf") has no text layer, so it is scanned.

  [Haveli PDF](https://law.gok.pk/wp-content/uploads/2025/09/G.-No.269-Univerisity-of-Haveli-Act-2025-PDF-FILE.pdf), [1995 PDF](https://law.gok.pk/wp-content/uploads/2023/05/The-Azad-Jammu-and-Kashmir-Shariat-Court-Amendment-Act-1995-ACT-XVI-OF-1995.pdf) (fetched)
- **Footer.** law.gok.pk: "Powered by LAW Department AJK | Designed by IT Team © Copyright 2026, All Ri[ghts Reserved]". robots.txt: "User-agent: * / Disallow: /wp-admin/ / Allow: /wp-admin/admin-ajax.php / Sitemap: https://law.gok.pk/wp-sitemap.xml". [Publications](https://law.gok.pk/publications/), [robots](https://law.gok.pk/robots.txt) (fetched)
- **AJK Legislative Assembly Acts page.** 15 Act rows (years 2019, 2022, 2023) and 24 PDF links. Examples:
  - "Act IV of 2023 The Azad Jammu and Kashmir Interim Constitution, 1974 2023-06-03 2023-06-04 Government"
  - "Act III of 2023 The Azad Jammu and Kashmir Legislative Assembly Privileges (Amendment)Act, 2023"
  - "THEAZADJAMMUANDKASHMIRLEGISLATIVEASSEMBLYPRIVILEGESACT1974.pdf", uploaded under /wp-content/uploads/2026/10/

  The page also offers rules in English and Urdu (/ruleseng.pdf, /rulesurdu.pdf). [AJK Assembly Acts](https://ajkassembly.gok.pk/acts/) (fetched)
- **ajk.gov.pk robots.txt.** WordPress default with sitemap (fetched content; the first request returned no status code).

### Inferences
- AJK is the most complete of the four jurisdictions online in as-enacted form, through law.gok.pk. There is no consolidation: Acts, amendment Acts and Ordinances are separate PDFs, and the Law Code volumes are chronological compilations. A large share of the 2023 bulk uploads appear to be scans that need OCR.
- The AJK Assembly site is not a comprehensive catalogue; it covers only 2019–2023.
- The Interim Constitution PDF (Oct 2023) post-dates the Act IV of 2023 entry. Its exact amendment currency was not verified.

### Gaps
- I did not determine whether the Interim Constitution PDF incorporates all amendments to date.
- The full contents of Volume XIV were not checked (the link may be an index only).
- I did not search for an AJK Gazette archive beyond the gazette extracts hosted on law.gok.pk.
- Urdu texts of AJK Acts were not checked.

## Cross-cutting: amendment history, point-in-time versions, and how amendments are signalled

### Takeaway
None of the official sources checked offers point-in-time ("as on date") versions or a structured amendment history. KP Code alone publishes consolidated texts, marked with bracketed footnotes. Balochistan Code, AJK law.gok.pk and the legislature sites publish as-enacted instruments, with amendments listed as separate items. A few documents carry "amended up to [date]" labels. Pakistan Code's page template has a commented-out "Repealed Laws" tab and CSS for a "Doc History" button, but the history feature did not render on the page sampled.

### Cited Findings
- **KP (consolidated).** The FAQ says legislation is held in "revised" form with amendments "incorporated into the main text". The PDFs use footnote markers such as "1[Khyber Pakhtunkhwa]". There is no per-law version list or as-on date. [KP FAQ](https://kpcode.kp.gov.pk/homepage/faq) (fetched)
- **Balochistan (as-enacted).** Amendment instruments are separate entries with "(Amendment-YYYY)" titles (673 of 1,790 titles contain "amend"). [Balochistan Code](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1) (fetched)
- **"Amended up to" labels.** The Balochistan Assembly posts "Recruitment Rules with all amendments up to 24th August, 2026" and "Rules of Procedure (Amended up to 22nd Dec 2025 )". The KP Assembly posts "Constitution (Upto 27th Amendment)". [PAB](https://pabalochistan.gov.pk/acts), [PAKP](https://www.pakp.gov.pk/act/) (fetched)
- **Pakistan Code (federal).**
  - The law page for the Muslim Family Laws Ordinance 1961 shows tabs "Complete Law", "Subordinate Legislation" and "Print/Download PDF".
  - A "Repealed Laws" tab is present in the HTML but commented out.
  - CSS for ".nav-doc-history" ("Push Doc History to right") exists, but no Doc History link rendered on that page.
  - The homepage "Latest Uploads" ticker lists items dated 2023 (for example "21 FEB: The Islamabad Capital Territory Local Government (Amendment) Act, 2023").
  - robots.txt: "User-agent: googlebot / Disallow: /pdffiles/".

  [Pakistan Code law page](https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Npa5po-sg-jjjjjjjjjjjjj), [home](https://pakistancode.gov.pk/english/index.php) (fetched)
- **Gazettes online.**
  - KP: no gazette portal found. The KP Assembly hosts "Gazetted copy" PDFs, for example https://www.pakp.gov.pk/wp-content/uploads/2025/10/The-Khyber-Pakhtunkhwa-Press-Newspaper-News-Agencies-and-Books-Registration-Amendment-Act-2025-Gazetted-copy.pdf (snippet only) and "-GC.pdf" files under /2026/07/ (fetched).
  - Balochistan: the Printing Dept site has no gazette downloads (fetched); the Code's "Gazette Notification" category has 497 entries (fetched).
  - AJK: gazette extracts are embedded in law.gok.pk PDFs (fetched).
  - GB: none found (search).

  [PAKP](https://www.pakp.gov.pk/act/), [Printing Bal.](https://printing.balochistan.gov.pk/downloads/)

### Inferences
- **Building point-in-time law.** Point-in-time law for these jurisdictions has to be built by the product, from as-enacted principal Acts plus dated amendment instruments. Dates are available in Balochistan Code metadata ("Promulgation Date"), the Assembly lists (passage, assent and enforcement dates) and AJK gazette headers. KP Code's consolidated texts can serve as a check on the latest state, but they are undated and lag about six months.
- **Gazettes.** Because no official gazette archive is online for any of the four jurisdictions, gazette-verified authenticity and commencement dates cannot be fully established from online official sources.

### Gaps
- I did not test whether Pakistan Code shows a working "Doc History" on other laws; that sits in another researcher's federal scope.
- I found no "updated on" date per law on any provincial or regional portal.
- I did not establish the official terms of use or disclaimer texts for KP Code (the footer references a "Disclaimer" page I did not locate), the Balochistan Code ("All rights reserved"), GB or AJK. No site had explicit reuse or licensing terms.
