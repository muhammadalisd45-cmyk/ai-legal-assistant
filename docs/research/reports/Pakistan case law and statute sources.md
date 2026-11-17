# Permission, not technology, gates Pakistan's legal corpus

Every Pakistani superior court, the main tribunals and every statute jurisdiction except Gilgit-Baltistan has an official online source. Almost all of them can be collected without CAPTCHAs, logins or paid access. What limits the Pakistan Justice Navigator (PJN) corpus is permission, coverage and document quality, not technology. On 12 November 2026 roughly **8,300 judgment and decision PDFs** could be collected right away under robots rules and site notices. They come from the Peshawar High Court, the Federal Shariat Court, both AJK apex courts, the Gilgit-Baltistan courts, the Competition Commission and Competition Appellate Tribunal, and the two federal ombudsmen. The two largest troves need written consent first: the **Sindh High Court's roughly 77,000 uploaded judgments and orders** and the **Lahore High Court's reported-judgment archive from 2010**. The **Supreme Court is the most closed source**. Its robots.txt blocks AI crawlers and declares `ai-train=no`, its search sits behind reCAPTCHA, and its PDF host returned HTTP 403 to every automated request. Pakistani copyright law is favourable: s.57(1)(q) of the Copyright Ordinance 1962 makes it non-infringing to reproduce court judgments and Gazette-published matter. But website terms, publisher headnotes and criminal bars on identifying juveniles and rape victims still shape what PJN may do. On the statute side, KP, Balochistan and AJK have usable official portals. GB has no code, and no jurisdiction offers point-in-time versions. Federal, ICT, Punjab and Sindh were verified by a follow-up pass on 13 November 2026 (Part E1): their listings expose enough metadata to detect new and amended laws automatically. PJN currently holds 56 official statute PDFs and no judgments. The fastest way to close that gap is to ingest the open tier now, send permission letters to the Supreme, Lahore, Sindh and Balochistan High Courts, and switch statute collection to the automated source-sync pipeline (Part F).

**How this report is organised.** Part A is the executive research report (analysis). Part B is the master source directory. Part C holds the raw extracted facts with source attribution, kept separate from the analysis. Part D maps key findings to evidence. Part E is the gap report. Part F gives the final summary and next actions. Unless stated otherwise, all observations date from live fetches on 12–13 November 2026. None of this is legal advice.

---

# Part A — Executive research report

## Three access tiers cover every court and tribunal

The useful way to sort Pakistan's official case-law sources is not by court rank. It is by whether PJN can lawfully and technically collect a source today. Three tiers emerge, and the volume is spread across them very unevenly.

**Tier 1, open now (about 8,300 documents).** The **Peshawar High Court** is the largest openly collectable source. It has **5,949 reported or referred judgments from 2009 to 2026** (5,885 unique PDF URLs). One POST to its search form returns all of them, with no CAPTCHA and no robots file. Every bench (Mingora, Abbottabad, Bannu, D.I. Khan) is covered through case-number suffixes in a single database ([PHC](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search)). The **Federal Shariat Court** lists **169 Shariat-petition judgments (1980–2025)** in one HTML table, with 159 downloadable PDFs. Its robots file blocks only `/wp-admin/`. Its criminal and suo motu judgment pages read "Under Construction", so most of its Hudood appellate output is not online ([FSC](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php)).

The **AJK Supreme Court** exposes **704 judgment posts since January 2016** through a public WordPress REST API, and its robots file allows crawling ([AJK SC REST](https://ajksupremecourt.gok.pk/wp-json/wp/v2/categories?per_page=50)). The **AJK High Court** has about **263 judgments, all from 2022 onward** ([AJK HC](https://ajkhighcourt.gok.pk/important-judgments)). The **Supreme Appellate Court GB** has about **753 PDFs, mostly from cases of 2009–2018** ([SAC GB](https://sacgb.gov.pk/Judgments.html)). The **GB Chief Court** offers only 17 decision dates between 2015 and 2020 ([GBCC](https://gbcc.gov.pk/ReportedJudgments.aspx)). Among regulators and ombudsmen, the **CCP has 177 orders and the Competition Appellate Tribunal 87**, both on cc.gov.pk ([CCP](https://cc.gov.pk/home/orders); [CAT](https://cc.gov.pk/home/decidedcatcases)). The **Federal Tax Ombudsman** posts 245 curated decisions and a rolling 15-day feed of every signed finding, with 647 findings in the window observed ([FTO](https://www.fto.gov.pk/decisions.aspx); [FTO feed](http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions)).

The **Islamabad High Court** also belongs in this tier on technical grounds. Its judgment pages are fed by unauthenticated JSON web services, and neither of its hosts has a robots.txt. It carries a disclaimer that content is "for information only", and the researchers still advise a permission letter ([IHC](https://mis.ihc.gov.pk/frmJgmnt)).

**Tier 2, technically open but legally reserved (roughly 90,000 documents).** The **Sindh High Court** has the richest corpus in the country. It publishes **judgments and orders, both AFR (approved for reporting) and non-AFR**, with advocates, topics, apex-court status and seat-coded neutral citations. Its sitting judges alone account for **77,258 uploads, of which 13,274 are AFR** ([SHC Report-002](https://caselaw.shc.gov.pk/caselaw/public/rpt-afr)). Its Disclaimer, however, forbids copying or re-publishing "in whole or in part" without "written consent from the Registrar" ([SHC Disclaimer](https://sindhhighcourt.gov.pk/disclaimer.php)).

The **Lahore High Court** publishes only AFR judgments, from 2010 onward. One plain GET per year returns a year's list: 704 sitting-judge and 59 former-judge items for 2025. Every page footer says material "should not be downloaded without prior agreement" ([LHC AFR](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting); [LHC footer](https://lhc.gov.pk/reported_judgments)). The researchers' extrapolation of 10,000–15,000 LHC PDFs in total is an estimate, not a published figure. LHC's own annual report shows the scale of what goes unpublished: **173,229 cases disposed of in 2025** against about 763 AFR uploads that year ([LHC Annual Report 2025](https://lhc.gov.pk/system/files/Annual%20Report%202025.pdf)).

**Tier 3, blocked or empty.** The **Supreme Court** blocks ClaudeBot, GPTBot, CCBot and about 30 other agents. For all agents it sets `Content-Signal: search=yes,ai-train=no,use=reference` ([SCP robots](https://scp.gov.pk/robots.txt)). Its search uses Google reCAPTCHA v3 ([SCP search](https://scp.gov.pk/JudgmentsSearch)). Only the 25-row Latest Judgments page is CAPTCHA-free, and the PDFs it links to on www.supremecourt.gov.pk returned Akamai 403s ([SCP Latest](https://scp.gov.pk/LatestJudgments.aspx)). The **Balochistan High Court** lists about 2,001 reported or significant judgments, but robots.txt disallows `/media/`, the folder where every PDF sits ([BHC robots](https://bhc.gov.pk/robots.txt)). The **Federal Service Tribunal**'s site is "Account Suspended" ([FST](https://www.fst.gov.pk/robots.txt)). The **Appellate Tribunal Inland Revenue** shows "No Record Found In Database" ([ATIR](https://atir.gov.pk/Judgements)). No official repository was found for banking courts, consumer courts or environmental tribunals. The new **Federal Constitutional Court**, created by the 27th Amendment, runs a JavaScript-only site whose data source was not examined ([FCC](https://www.fccp.gov.pk/judgments)).

The lopsidedness is the main strategic fact. About 90% of the identifiable official judgment volume (SHC plus LHC) is one consent letter per court away. The apex court, whose precedents bind every other court, is the hardest of all to obtain lawfully. No court publishes all of its orders, so every official corpus is a curated subset. The only exceptions are SHC's mix of AFR and non-AFR material and the FTO's 15-day feed.

## Copyright allows reuse; site terms, headnotes and anonymity laws limit it

Pakistan's Copyright Ordinance 1962 treats judgments as "Government work" owned by the State. Section 57(1)(q) then provides that reproducing or publishing "(i) any matter which has been published in any official Gazette" and "(ii) any judgment or order of a court, tribunal or other judicial authority" is not infringement, "unless the reproduction or publication … is prohibited" by the Government or the court ([Copyright Ordinance, Pakistan Code PDF](https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf); [WIPO Lex](https://www.wipo.int/wipolex/en/text/129350)). That covers both halves of PJN's corpus: court-issued judgment text and Gazette-published statutes.

Four constraints remain.

First, **site terms and robots signals are separate from copyright**. LHC's "prior agreement" footer, SHC's Registrar-consent Disclaimer, the Supreme Court's `ai-train=no` and the BHC `/media/` disallow are contractual or conventional reservations. A statutory exception may override them in copyright terms, but no Pakistani authority settles this. A product whose credibility rests on "official, citable sources" should not test it.

Second, **publisher editorial matter falls outside s.57(1)(q)(ii)**. The FSC's own 2025 PDF is the PLD-reported version, carrying "P L D 2025 Federal Shariat Court 1" headnotes ([FSC PDF](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=128)). PakistanLawsite's terms bar copying, scraping and storing ([Pakistanlawsite](https://www.pakistanlawsite.com/)). The free pakistancaselaw.com forbids bulk access and AI-training crawlers ([Pakistan Case Law terms](https://pakistancaselaw.com/terms)). PJN must strip reporter headnotes and must not source from either aggregator. The leading authority on headnote copyright, *Eastern Book Co. v. D.B. Modak*, is Indian and was confirmed only from a search snippet.

Third, **anonymity duties carry criminal penalties**. Juvenile Justice System Act 2018 s.13 punishes publishing a juvenile's identity with up to three years' imprisonment. Its Explanation exempts "the judgment of any High Court or the Supreme Court", but trial-court and Juvenile Court material is not exempt ([JJSA 2018](https://lpr.adb.org/sites/default/files/2024-07/pakistan-juvenile-justice-system-act-2018.pdf)). Section 376A PPC creates a similar offence for rape victims. Whether it has the same superior-court exemption could not be read from the OCR-damaged Gazette scan ([Gazette scan](https://sld.com.pk/wp-content/uploads/2021/04/1485428121_999.pdf)). In 2024 the LHC directed trial judges to identify victims by acronyms ([Dawn](https://dawn.com/news/1828670/lhc-asks-judges-to-protect-rape-victims-identity-in-verdicts)). Pakistan still has no enacted personal data protection law ([Dawn](https://www.dawn.com/news/2021159)). Yet court PDFs do expose personal data: the sampled IHC judgment printed a litigant's full IBAN ([IHC PDF](https://mis.ihc.gov.pk/attachments/judgements/209540/1/Muhammad_Usman_v_FoP_WP_No_1553_of_2026__J_Arbab_Muhammad_Tahir__Approved_for_Reporting_639280833781874862.pdf)).

Fourth, **official status carries disclaimers**. Pakistan Code says its laws "should not be taken as authentic or error-free" and that the Gazette prevails ([Pakistan Code](https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Fvbpw%3D-sg-jjjjjjjjjjjjj)). The IHC tells users "not to rely on this information for official purposes" ([IHC](https://mis.ihc.gov.pk/frmJgmnt)). PJN should present these as court- or ministry-published copies, not certified texts.

## Statute portals cover most jurisdictions, but none gives point-in-time law

**Federal and ICT law** sits on Pakistan Code, run by the Ministry of Law and Justice. Its robots.txt disallows only `googlebot` from `/pdffiles/` ([Pakistan Code](https://pakistancode.gov.pk/english/index.php)). Its texts are consolidated with amendment footnotes, and the Constitution PDF reflects the 27th Amendment 2025 ([Constitution PDF](https://pakistancode.gov.pk/pdffiles/administrator9d8e2ecc414c6d3371ac41114b61a2c4.pdf)). It has no working version history: a "Repealed Laws" tab is commented out of the page HTML, and its "Latest Uploads" ticker showed 2023 items. ICT statutes such as the Islamabad Capital Territory Local Government (Amendment) Act 2023 appear on the same portal ([Pakistan Code home](https://pakistancode.gov.pk/english/index.php)).

The session's earlier verified crawl recorded the following:

| Portal | Holdings (earlier crawl) |
|---|---|
| Pakistan Code | About **1,037 federal laws**, with direct PDFs |
| Punjab Code | About **746** laws |
| Sindh Code | About **1,383** Acts and Ordinances |

That crawl also found that the principal **Sindh Civil Courts Ordinance 1962** and **Sindh Land Revenue Act 1967** are **absent from Sindh Code**. The dedicated federal/ICT/Punjab/Sindh track was stopped early and later completed by a direct follow-up pass (Part E1, notes `statutes_federal_ict_punjab_sindh.md`), which also found an official consolidated copy of the Sindh Civil Courts Ordinance 1962 at the Sindh Judicial Academy.

**Khyber Pakhtunkhwa.** KP Code is the only provincial portal that publishes consolidated ("revised") texts. It holds 969 records: 422 Acts, 125 Ordinances, 44 Regulations, 377 Rules and 1 Notification ([KP Code FAQ](https://kpcode.kp.gov.pk/homepage/faq); [KP Code search](https://kpcode.kp.gov.pk/homepage/advance_search)). Its robots.txt allows everything. It **lags the Assembly by about six months**: the Assembly lists Acts up to No. XXI of 2026, while the Code's newest are Nos. VII–IX of 2026 ([KP Assembly](https://www.pakp.gov.pk/act/)).

**Balochistan.** Balochistan Code is an as-enacted repository with 1,790 entries. They comprise 410 Acts, 172 Ordinances, 637 Rules and 497 Gazette Notifications, plus Policies and Regulations, and about 1,679 unique titles. 673 titles contain "amend", and recent PDFs can be image-only ([Balochistan Code](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1)). The Code's robots file has no directives. The province's Printing Department host, however, declares `ai-train=no` and blocks Anthropic crawlers ([Printing Dept robots](https://printing.balochistan.gov.pk/robots.txt)).

**AJK.** The AJK Law Department hosts about **1,015 Act PDFs and 1,143 Ordinance PDFs**, current to Act V of 2025 and Ordinance III of 2026. It also hosts a 618-row Adopted Laws table, Law Code volumes I–XIV and the Interim Constitution. Many of the 2023 bulk uploads are scans ([AJK Acts](https://law.gok.pk/acts/); [AJK Ordinances](https://law.gok.pk/ordinance/)).

**Gilgit-Baltistan.** GB is the weakest jurisdiction. It has **no statute code**. The Assembly Acts page contains test rows, and 3 of 3 sampled PDFs returned 404 ([GB Assembly](https://gbassembly.gbit.gov.pk/pages/acts)). The government portal offers about 15 Acts plus the GB Order 2018 ([GB Acts](https://gilgitbaltistan.gov.pk/pages/acts)). Dawn reported 63 Acts in one Assembly tenure (snippet only) ([Dawn](https://www.dawn.com/news/1957215)). Federal law reaches GB only through adaptation under s.60(3) of the GB Order 2018, so Pakistan Code texts cannot be assumed to apply there ([GB Order 2018](https://gilgitbaltistan.gov.pk/storage/downloads/GB%20Order%202018.pdf)).

**Cross-cutting.** No official gazette archive was found online for KP, Balochistan, GB or AJK. None of the sources examined offers point-in-time ("as on date") law. PJN will have to build historical versions itself, from principal Acts plus dated amendment instruments. On KP Code, the merged-district Continuation of Laws Acts 2018/2019 show no repeal badge, although press reports say they were withdrawn. This shows why repeal status needs manual curation ([KP Code 1438](https://kpcode.kp.gov.pk/homepage/lawDetails/1438); [Dawn](https://www.dawn.com/news/1505809)).

## Formats and citations differ by court, so ingestion needs per-court handling

Born-digital, text-extractable PDFs dominate at LHC, SHC, IHC, AJK HC, AJK SC and recent FSC files ([LHC sample](https://sys.lhc.gov.pk/appjudgments/2026LHC8763.pdf); [SHC sample](https://caselaw.shc.gov.pk/caselaw/view-file/MzI4NzczY2Ztcy1kYzgz)). Image-only scans dominate elsewhere: 2 of 3 PHC samples, plus SAC GB, GBCC, CCP and CAT (CamScanner) files and Wafaqi Mohtasib findings. FTO files are scans with a weak copier OCR layer, for example "lSBIrr" for "ISB/IT" ([PHC scan](https://peshawarhighcourt.gov.pk/PHCCMS//judgments/CR411-2020-----13-01-2025.pdf); [FTO](https://www.fto.gov.pk/assets/decisions/11887_2026.pdf)). Urdu and Arabic glyphs drop out even from text PDFs ([FSC PDF](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=128)). An OCR stage for English with Urdu fragments is therefore mandatory, not optional.

Court-assigned citations exist but have never been formally announced, and no court prints them inside its PDFs:

| Court | Citation format | Where it appears |
|---|---|---|
| LHC | `YYYY LHC N` | Filename only |
| SHC | Seat-coded, e.g. `2026 SHC KHI 2016`; one judgment can carry two | Listing metadata |
| PHC | `2025 PHC 14`, on 1,103 records | Listing metadata |
| SC | "SC Citation" column, apparently `2025 SCP 449` | Listing column (format from a snippet) |
| IHC | Commercial reporter citations only | — |
| FSC | PLD citations only | — |

Sources: [LHC endpoint](https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2025&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1=); [SHC search](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search); [PHC](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search).

The citation model therefore has to take the citation from listing metadata, allow several citations per document, and keep reporter citations as cross-references. PHC and BHC home pages contain hidden spam links ([PHC home](https://peshawarhighcourt.gov.pk/app/site/); [BHC home](https://bhc.gov.pk/)), so every fetched PDF should be hashed and tied to the listing row that pointed to it.

## No third-party dataset is citable; one is a useful index

None of the five datasets the user named can serve as citable evidence. One of them earns a supporting role.

**endomorphosis/ipfs_pakistan_provincial_laws** has **1,122 KP and Balochistan Acts, Ordinances and Regulations, split into 21,857 section rows**. Every row records its official PDF URL, the PDF's SHA-256 and the detail page. The builder documented that it honoured robots.txt with delays of 3 seconds or more ([README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md)). That makes it a good gap-finder and fetch index for those two provinces. It contains nothing for Punjab, Sindh, ICT, GB, AJK or federal law. Repeal status is unverified, and some dates conflict with the document text.

**AyeshaJadoon/Pakistan_Laws_Dataset** is a 46.9 MB JSON dump that the Hugging Face viewer cannot read. It has hashed Pakistan Code filenames instead of titles, contains letter-spaced extraction garbage, and its claimed 969 laws are unverified ([HF API](https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset)). Its sibling **endomorphosis/ipfs_pakistan_laws** (970 federal instruments with per-row Pakistan Code URLs) is the better federal cross-check, though it is unvetted and partly sourced from Common Crawl ([README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_laws/raw/main/README.md)).

**abdullah693/adaption-pakistan-law-qa-pairs** has 11,195 rows, but **31% are unrelated general chat**. The CPC accounts for only 208 rows. The base answers matched Pakistan Code in 9 of 9 spot checks, but the LLM-"enhanced" fields imported US and Indian law. The dataset has no licence ([HF statistics](https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train)).

The **Zenodo Pakistani Law Dataset** (record 20509007, CC-BY-4.0) is an undergraduate project. It covers 7 statutes, not the 8 it claims, and has no CPC. It lacks PPC 295-A/B/C and 489-F and the Limitation Schedule, and shows no amendments after 2006 ([Zenodo](https://zenodo.org/api/records/20509007)). Only its lawyer-written questions are worth keeping, and only as evaluation prompts.

**SyedAhtsham/Pakistani-Law-Cases-Search-Engine** is an unlicensed 2021 student project. It holds 1,000 Supreme Court PDFs scraped from supremecourt.gov.pk, with no metadata and only stemmed token lists in place of full text ([GitHub API](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine); [project report](https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf)). Using it would sidestep the Court's `ai-train=no` signal. Its only use is as a list of cases to re-obtain officially.

## Conclusion

The research changes the problem PJN faces. The hard part is no longer finding official sources, because they exist almost everywhere and are mostly machine-readable. The hard part is turning a handful of formal relationships into data rights. Four letters, to the Registrars of the Supreme Court, Lahore High Court, Sindh High Court and Balochistan High Court, would unlock roughly 90% of identifiable official judgment volume and the apex precedent the product most needs. No amount of crawler engineering can substitute for them. Until those letters are answered, a PJN built only from Tier 1 would be thin and skewed. Its case law would lean heavily towards KP, AJK and GB, and its Supreme Court coverage would be close to nil. That skew is a product risk worth stating openly to users.

The second shift concerns what "official" means. Even official copies are curated subsets carrying disclaimers. Their citations appear only in listing metadata, and many arrive as scans or carry publisher headnotes. Statute portals are as-enacted (Balochistan, AJK), consolidated but six months behind (KP), or "under review" (federal). None is point-in-time. PJN's moat will therefore come from provenance discipline: hashing, listing-row identity, multi-citation keys, headnote stripping, anonymisation and its own version histories built on official inputs. It will not come from the volume of documents collected.

---

# Part B — Master source directory

Credibility: **Primary** means an official government, court or tribunal host. **Secondary** means press, an archive or a third party. Access status reflects 12–13 Nov 2026.

## B1. Case law: courts

| Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| SCP Judgments Search | https://scp.gov.pk/JudgmentsSearch | Supreme Court of Pakistan | Official search | Case years 1980–2026 in dropdown | Primary | Fetched; search gated by reCAPTCHA v3 |
| SCP Latest Judgments | https://scp.gov.pk/LatestJudgments.aspx | Supreme Court | Official listing (25 rows) | Uploads to 11-11-2026 | Primary | Fetched; no CAPTCHA |
| SCP robots.txt | https://scp.gov.pk/robots.txt | Supreme Court | Robots | Live | Primary | Fetched; blocks AI crawlers; `ai-train=no` |
| SC legacy PDF host | https://www.supremecourt.gov.pk/downloads_judgements/ | Supreme Court | Judgment PDFs | — | Primary | Inaccessible (Akamai HTTP 403) |
| Federal Constitutional Court judgments | https://www.fccp.gov.pk/judgments | Federal Constitutional Court | SPA | Created Nov 2025 | Primary | JS shell only; not profiled |
| FSC Shariat Petitions list | https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php | Federal Shariat Court | Official listing + PDFs | Latest 19 Mar 2025 | Primary | Fetched; open |
| FSC Criminal / Suo Moto pages | https://www.federalshariatcourt.gov.pk/criminaljudgments.html | FSC | Listing | — | Primary | "Under Construction" |
| IHC Judgments | https://mis.ihc.gov.pk/frmJgmnt | Islamabad High Court | Official listing (JSON-backed) | Live | Primary | Fetched; no robots, no CAPTCHA |
| IHC search JSON | https://mis.ihc.gov.pk/ihc.asmx/srchDecisionClms | IHC | Web service | Live | Primary | Fetched once (97 records) |
| LHC AFR (sitting judges) | https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting | Lahore High Court | Official listing | Latest 12-11-2026 | Primary | Fetched; copyright footer reserves download |
| LHC AFR (former judges) | https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting_by_former_judges | LHC | Official listing | Live | Primary | Fetched |
| LHC PDF host | https://sys.lhc.gov.pk/appjudgments/ | LHC | Judgment PDFs | Live | Primary | Fetched samples; robots 404 |
| LHC Annual Report 2025 | https://lhc.gov.pk/system/files/Annual%20Report%202025.pdf | LHC | Statistics | 2025 | Primary | Fetched |
| SHC Caselaw Advance Search | https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search | Sindh High Court | Official search | Live | Primary | Fetched; Cloudflare; no CAPTCHA |
| SHC Report-002 AFR | https://caselaw.shc.gov.pk/caselaw/public/rpt-afr | SHC | Statistics | Live | Primary | Fetched |
| SHC Disclaimer | https://sindhhighcourt.gov.pk/disclaimer.php | SHC | Terms | "© 2001-2002" | Primary | Fetched |
| SHC digital / Search Citation | https://digital.shc.gov.pk/search-citation | SHC | eCTC portal | © 2026 | Primary | Fetched; reCAPTCHA (do not automate) |
| PHC Reported Judgments | https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php | Peshawar High Court | Official database | Records to 2026 | Primary | Fetched; open |
| PHC Case Law digest | https://peshawarhighcourt.gov.pk/app/site/108/c/Case_Law.html | PHC | Digest PDFs | Latest Jan–Mar 2023 | Primary | Fetched |
| BHC Judgments index | https://bhc.gov.pk/resources/judgments | Balochistan High Court | Per-judge listings | 2026 | Primary | Fetched; PDFs under robots-disallowed `/media/` |
| BHC portal | https://portal.bhc.gov.pk/judgments | BHC | Search SPA | — | Primary | API redirected to login; not pursued |
| GBCC Reported Judgments | https://gbcc.gov.pk/ReportedJudgments.aspx | Chief Court GB | ASP.NET search | Decisions 2015–2020 | Primary | Fetched; open |
| SAC GB Judgments | https://sacgb.gov.pk/Judgments.html | Supreme Appellate Court GB | Static list | © 2025 | Primary | Fetched; open |
| AJK HC Judgments | https://ajkhighcourt.gok.pk/important-judgments | High Court of AJ&K | Search | 2022–2026 | Primary | Fetched; open |
| AJK SC Judgements/Orders | https://ajksupremecourt.gok.pk/judgements-orders/ | Supreme Court of AJ&K | WordPress listing | Latest 28-10-2026 | Primary | HTTP 500 but renders; REST API open |
| AJK SC REST API | https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts?categories=18&per_page=100 | AJK SC | JSON | Live | Primary | Fetched |

## B2. Case law: tribunals and quasi-judicial bodies

| Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| CCP Orders | https://cc.gov.pk/home/orders | Competition Commission | Orders | Latest 11 Sep 2026 | Primary | Fetched; open |
| CAT orders (CCP-hosted) | https://cc.gov.pk/home/decidedcatcases | Competition Appellate Tribunal via CCP | Orders | Latest 06-07-2026 | Primary | Fetched; open |
| FTO Reported Decisions | https://www.fto.gov.pk/decisions.aspx | Federal Tax Ombudsman | Selected decisions | 2022–2026 | Primary | Fetched; open |
| FTO Signed Decisions (15-day) | http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions | FTO (third-party DNS host) | Rolling feed | 29/10–12/11/2026 | Primary (by linkage) | Fetched |
| Wafaqi Mohtasib Findings | https://mohtasib.gov.pk/Publications | Federal Ombudsman | Findings | Newest 18/12/2020 | Primary | Fetched; stale |
| FST site | https://www.fst.gov.pk/ | Federal Service Tribunal | Official site | Suspended | Primary | Inaccessible ("Account Suspended") |
| FST archived home | http://web.archive.org/web/20260716134606/https://fst.gov.pk/ | Internet Archive | Archive | 16 Jul 2026 | Secondary | Fetched; no judgments section |
| ATIR Judgements | https://atir.gov.pk/Judgements | Appellate Tribunal Inland Revenue | Listing | © 2023 | Primary (official status unconfirmed) | Fetched; "No Record Found" |
| LJCP ATSC 2024 report | https://ljcp.gov.pk/SiteImage/Misc/files/ATSC%202024%20(20-06-25).pdf | LJCP | Statistics | 20-06-2025 | Primary | Snippet only |

## B3. Statutes

| Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| Pakistan Code | https://pakistancode.gov.pk/english/index.php | Ministry of Law & Justice | Federal + ICT consolidated code | © 2022; ticker items from 2023 | Primary | Fetched (home + sample laws); ~1,037 laws per session crawl |
| Punjab Code | https://punjabcode.punjab.gov.pk/en/alphabetical | Govt of Punjab | Provincial code | Crawled 2026-11-12 | Primary | Fetched; 746 laws with PDFs; robots.txt HTTP 403 |
| Punjab Code – recently updated | https://punjabcode.punjab.gov.pk/en/recently_updated | Govt of Punjab | Amendment/new-law feed | Fetched 2026-11-13 | Primary | Fetched |
| Sindh Code | https://sindhlaws.gov.pk/Alpha.aspx?pg=ACT | Govt of Sindh | Provincial code | Crawled 2026-11-12 | Primary | Fetched; 1,383 Acts/Ordinances (letter filter + paging); robots `Allow: /` |
| Sindh Judicial Academy – Updated Laws | https://sja.gos.pk/updated-laws/ | Sindh Judicial Academy | Consolidated texts (tier 2) | Fetched 2026-11-13 | Primary (secondary compilation) | Fetched; 41 laws incl. Sindh Civil Courts Ordinance 1962 |
| Pakistan Code – chronological / latest ordinances | https://pakistancode.gov.pk/english/KmTY5e.php | Ministry of Law and Justice | New-law feed | Fetched 2026-11-13 | Primary | Fetched |
| KP Code | https://kpcode.kp.gov.pk/homepage/list_all_law | KP Law Dept | Consolidated provincial code | Newest Act VIII/IX of 2026 | Primary | Fetched; robots Allow all |
| KP Assembly Acts | https://www.pakp.gov.pk/act/ | Provincial Assembly KP | Acts + gazetted copies | To Act XXI of 2026 | Primary | Fetched |
| Balochistan Code | https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1 | Balochistan Law Dept | As-enacted repository | To 05 Nov 2026 | Primary | Fetched; robots no directives |
| Balochistan Assembly Acts | https://pabalochistan.gov.pk/acts | Provincial Assembly Balochistan | Acts list | To Act XV of 2026 | Primary | Fetched; robots allow all |
| Balochistan Printing Dept | https://printing.balochistan.gov.pk/ | Govt of Balochistan | Gazette printer | — | Primary | Fetched; no gazette PDFs; `ai-train=no` |
| blncode.pitb.gov.pk | http://blncode.pitb.gov.pk | Unknown (PITB subdomain) | Unknown | — | Unknown | Inaccessible (TCP connect fails) |
| GB Assembly Acts | https://gbassembly.gbit.gov.pk/pages/acts | GB Assembly | Acts list | 2020–2025 | Primary (buggy) | Fetched; 3/3 PDFs 404 |
| GB Govt Acts / Laws | https://gilgitbaltistan.gov.pk/pages/acts | Govt of GB | Download list (~15 Acts) | GB Order PDF Nov 2024 | Primary | Fetched |
| gba.gov.pk / gba.gbit.gov.pk | https://gba.gov.pk/acts/ | GB Assembly (legacy) | Acts list | — | Primary | Inaccessible (expired cert / 404) |
| AJK Law Dept | https://law.gok.pk/acts/ | AJK Law Dept | Acts, Ordinances, Law Code vols | To Act V 2025 / Ord III 2026 | Primary | Fetched; WP robots |
| AJK Assembly Acts | https://ajkassembly.gok.pk/acts/ | AJK Legislative Assembly | Acts list | 2019–2023 | Primary | Fetched |

## B4. Legal framework and landscape

| Title | URL | Organisation | Category | Date | Credibility | Access status |
|---|---|---|---|---|---|---|
| Copyright Ordinance 1962 (Pakistan Code PDF) | https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf | Ministry of Law & Justice | Statute | Current portal copy | Primary | Fetched |
| Copyright Ordinance 1962 (WIPO Lex) | https://www.wipo.int/wipolex/en/text/129350 | WIPO | Statute (secondary host) | As amended to 2000 | Secondary | Fetched |
| Juvenile Justice System Act 2018 | https://lpr.adb.org/sites/default/files/2024-07/pakistan-juvenile-justice-system-act-2018.pdf | ADB LPR | Statute (secondary host) | Jul 2024 upload | Secondary | Fetched |
| s.376A PPC Gazette scan | https://sld.com.pk/wp-content/uploads/2021/04/1485428121_999.pdf | Supreme Law Digest | Gazette scan | 2016 | Secondary | Snippet only (OCR damaged) |
| LHC victim-anonymity ruling | https://dawn.com/news/1828670/lhc-asks-judges-to-protect-rape-victims-identity-in-verdicts | Dawn | News | 21 Apr 2024 | Secondary | Fetched |
| PakistanLawsite | https://www.pakistanlawsite.com/ | Oratier Technologies / PLD | Commercial publisher | © 2026 | Secondary | Fetched |
| Pakistan Case Law terms | https://pakistancaselaw.com/terms | Hamadullah Shah, Advocate | Free aggregator | 10 Jul 2026 | Secondary | Fetched |
| LJCP home (NJPMC AI guidelines link) | https://ljcp.gov.pk/ | Law & Justice Commission | Official | © 2026 | Primary | Fetched (guideline text not read) |
| PHC footnote-omission petition | https://www.dawn.com/news/1949786 | Dawn | News | 19 Oct 2025 | Secondary | Fetched |

## B5. Third-party datasets

| Title | URL | Owner | Category | Date | Credibility | Access status |
|---|---|---|---|---|---|---|
| Pakistan_Laws_Dataset (D1) | https://huggingface.co/datasets/AyeshaJadoon/Pakistan_Laws_Dataset | AyeshaJadoon | HF dataset (federal statutes) | 2025-01-30 | Low | Metadata + 3 byte ranges |
| ipfs_pakistan_provincial_laws (D2) | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws | endomorphosis | HF dataset (KP + Balochistan) | 2026-11-06 | Medium-high (provenance logged) | Metadata, viewer API, manifests |
| ipfs_pakistan_laws (federal sibling) | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_laws | endomorphosis | HF dataset (federal) | 2026-11-06 | Medium (unvetted) | README + first rows |
| adaption-pakistan-law-qa-pairs (D3) | https://huggingface.co/datasets/abdullah693/adaption-pakistan-law-qa-pairs | abdullah693 | Synthetic QA | 2026-06-20 | Low-medium | Viewer API (600 rows sampled) |
| Zenodo Pakistani Law Dataset | https://zenodo.org/records/20509007 | Umair Ahmed | Statute CSVs + QA | 2026-06-02 | Low-medium | API + 1 file in full |
| PakLegalAid QA (companion) | https://zenodo.org/records/20509273 | Umair Ahmed | QA CSV | 2026-06-02 | Low-medium | API |
| SC NER dataset (alternative) | https://zenodo.org/records/21671415 | Ul-Hasan, Shafait | 214 annotated SC judgments | 2026-07-29 | Medium | Metadata only |
| Pakistani-Law-Cases-Search-Engine | https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine | SyedAhtsham | Student repo, 1,000 SC PDFs | Last push 2023-05-08 | Low | API + 3 PDFs |

---

# Part C — Extracted data with source attribution (raw facts, no analysis)

## C1. Courts: what each publishes and how

| Court | What is published | Coverage / count (as observed) | Format (samples) | Collection mechanism | robots.txt | Terms / notice | Source |
|---|---|---|---|---|---|---|---|
| Supreme Court | Reported + unreported judgments (Reported Y/N filter); 35 case types | Case-year filter 1980–2026; Latest list 25 rows | Not verified (PDFs 403); listing sizes 18 KB–2.65 MB | reCAPTCHA v3 search; plain HTML Latest list | Blocks ClaudeBot, anthropic-ai, GPTBot, CCBot, etc.; all agents `ai-train=no`, `use=reference` | "© 2026 … All Rights Reserved"; Terms link is `href="#"` | [scp.gov.pk](https://scp.gov.pk/LatestJudgments.aspx) |
| Federal Shariat Court | Shariat petitions only | 169 listed, 159 PDFs, 1980–2025 | 2025: text PDF of PLD-reported version; 1990: scan + poor OCR | One HTML table; `?download=N` | Disallow `/wp-admin/` only | Footer "© 2026 … IT Wing" | [FSC](https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php) |
| Islamabad HC | Reported (AFR) + important; search over decisions | 2025 AFR query: 97 records (24 with citation) | Born-digital text, numbered paras | POST JSON `ihc.asmx/*` | None (404) | "for information only … not … for official purposes" | [IHC](https://mis.ihc.gov.pk/frmJgmnt) |
| Lahore HC | AFR only, sitting + former judges | 2010–2026; 2025: 704 + 59; 2015: 205; former 2010: 164 | Born-digital Word PDFs; no headnotes; citation not in text | GET `approved_judgments_result_new.php?year=` | lhc.gov.pk: no rule on judgments; data host 403; PDF host 404 | "should not be downloaded without prior agreement" | [LHC](https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting) |
| Sindh HC | Judgments + orders, AFR flag; all seats | Sitting judges: 77,258 uploads / 13,274 AFR | Born-digital tagged PDF | POST `AJAX_PUBLIC.php` (opt=search_judgement); `view-file/{base64}` | caselaw host: preamble only, no directives; main site disallows `/causelist/` | Registrar's written consent required to copy/re-publish | [SHC](https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search); [Disclaimer](https://sindhhighcourt.gov.pk/disclaimer.php) |
| Peshawar HC | Reported / referred judgments, all benches | 5,949 records, 2009–2026; 1,103 with PHC neutral citation; 278 link SC judgment | Mixed: 2/3 samples image-only | One POST "All Years" (12.4 MB HTML) | None (JS redirect) | "All Rights Reserved" | [PHC](https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search) |
| Balochistan HC | Reported + significant per judge | 1,959 + 42 entries; 2,001 PDF ids (1–2004); citation years 2010–2026 | Not tested (robots) | Static per-judge pages; portal API → login | Disallow `/media/` (all PDFs) | "© 2026 … All rights reserved" | [BHC](https://bhc.gov.pk/resources/judgments); [robots](https://bhc.gov.pk/robots.txt) |
| GB Chief Court | Reported judgments | 17 decision dates, 2015–2020 | Scan (HP Scan) | ASP.NET postback → static PDF | None (404) | "© … All Rights Reserved" | [GBCC](https://gbcc.gov.pk/ReportedJudgments.aspx) |
| SAC GB | Judgments | ~757 rows / 753 PDFs; case years 2007–2025, peak 2015–2017 | Mostly scans; some text | Single static HTML page | None (404) | "Copyright © 2025" | [SAC GB](https://sacgb.gov.pk/Judgments.html) |
| AJK HC | Judgments (active + previous judges) | 220 + 43 PDFs; 2022–2026 | Born-digital (Word 2016) | Form POST, "All" returns everything | None (404) | "Copy Right @ 2017-2025" | [AJK HC](https://ajkhighcourt.gok.pk/important-judgments) |
| AJK SC | "Important judgements" | 704 posts, 2016-01-14 to 2026-10-28 | Text PDFs; 2026 posts partly on Google Drive | WordPress REST API | Allows all except `/?s=` | "Copyright 2020" | [AJK SC REST](https://ajksupremecourt.gok.pk/wp-json/wp/v2/posts?categories=18&per_page=100) |

## C2. Tribunals and ombudsmen

| Body | Published | Count | Format | robots | Source |
|---|---|---|---|---|---|
| CCP | Orders, 2007–2026 | 177 | Scan (HP Scan), http host | None (404) | [CCP](https://cc.gov.pk/home/orders) |
| CAT (via CCP) | Appellate orders | 87 | Phone-app scan (CamScanner) | None (404) | [CAT](https://cc.gov.pk/home/decidedcatcases) |
| FTO | Curated decisions 2022–2026; all signed findings for 15 days | 245; 647 in window | Scan + copier OCR | None (404) | [FTO](https://www.fto.gov.pk/decisions.aspx); [feed](http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions) |
| Wafaqi Mohtasib | Selected findings 2017–2020 | 13 | Scan | None (404) | [WMS](https://mohtasib.gov.pk/Publications) |
| ATIR | Nothing | 0 | — | Returns HTML | [ATIR](https://atir.gov.pk/Judgements) |
| FST | Nothing; site suspended | 0 | — | Unretrievable | [FST](https://www.fst.gov.pk/robots.txt) |

## C3. Statute portals

| Jurisdiction / portal | Holdings | Consolidated? | Currency | Format | robots / terms | Source |
|---|---|---|---|---|---|---|
| Federal + ICT: Pakistan Code | ~1,037 laws (session crawl context) | Yes (footnotes) | Constitution to 27th Amdt; CPC "(Under Review)" | Text PDFs at `/pdffiles/administrator<hex>.pdf` | `User-agent: googlebot / Disallow: /pdffiles/`; "© 2022"; "under review … refer to … Gazette" | [Pakistan Code](https://pakistancode.gov.pk/english/index.php) |
| Punjab: Punjab Code | ~746 laws (session crawl context) | Not researched | Not researched | Not researched | Not researched | Session context |
| Sindh: Sindh Code | ~1,383 Acts/Ordinances (session crawl context); Sindh Civil Courts Ordinance 1962 and Sindh Land Revenue Act 1967 absent | Not researched | Not researched | Not researched | Not researched | Session context |
| KP: KP Code | 969 records (Acts 422, Ord 125, Reg 44, Rules 377, Notif 1); "All Laws" list 575 | Yes ("revised" form) | Newest Acts VII–IX of 2026 (May 2026) | Born-digital, iTextSharp watermark | `Allow: /`; "informational purposes … subject to the Disclaimer" | [KP Code](https://kpcode.kp.gov.pk/homepage/list_all_law) |
| KP: Assembly | Acts list with gazetted copies | No | To Act XXI of 2026 (Aug 2026) | PDF ("-GC.pdf") | robots 404 | [PAKP](https://www.pakp.gov.pk/act/) |
| Balochistan: Code | 1,790 entries (Rules 637, Gazette Notif 497, Acts 410, Ord 172, Policies 40, Reg 34); ~1,679 unique titles | No (as-enacted) | To Act XXIV of 2026 (Oct 2026) | Mixed; 2026 Act image-only | Preamble only; "All rights reserved" | [Balochistan Code](https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1) |
| Balochistan: Assembly | 428 PDFs, 1972–2026 | No | To Act XV of 2026 | PDF | Allow all | [PAB](https://pabalochistan.gov.pk/acts) |
| GB | ~23 Assembly rows (test data, dead PDFs); ~15 Acts + GB Order 2018 on govt portal | No | — | GB Order: text; Adaptation Act 2012: scan | Assembly allow all; portal 404 | [GB Assembly](https://gbassembly.gbit.gov.pk/pages/acts); [GB Govt](https://gilgitbaltistan.gov.pk/pages/acts) |
| AJK: law.gok.pk | 1,015 Act PDFs; 1,143 Ordinance PDFs; 618-row Adopted Laws; Law Code vols I–XIV; Interim Constitution | No | Act V 2025; Ord III 2026 | 2025 gazette: text; 2023 bulk: scans | WP default; "© 2026, All Rights Reserved" | [AJK Law](https://law.gok.pk/acts/) |
| PJN current holdings | 56 official statute PDFs; 0 judgments | — | — | — | — | Session context |

## C4. Third-party datasets

| Dataset | Size / scope (verified) | Provenance | Licence | Quality defects observed | Source |
|---|---|---|---|---|---|
| AyeshaJadoon/Pakistan_Laws_Dataset | One 46,924,676-byte JSON; card claims 969 laws (unverified) | `file_name` = Pakistan Code hashed PDF name; no URL/title/date | ODC-BY tag | Page headers, split words, letter-spaced garbage; viewer cannot read it | [HF](https://huggingface.co/api/datasets/AyeshaJadoon/Pakistan_Laws_Dataset) |
| endomorphosis/ipfs_pakistan_provincial_laws | 1,122 laws (KP 568, Bal 554) + 21,857 section rows; snapshot 2026-10-23 | Per-row official `pdf_url`, `pdf_sha256`, detail page | "other" / no licence stated | OCR on 816 pages in 144 docs; date/title mismatches; repeal unverified | [README](https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md) |
| abdullah693/adaption-pakistan-law-qa-pairs | 11,195 rows; 7,717 legal (criminal 3,349, constitutional 2,951, evidence 1,117, CPC 208, family 92) + 3,478 null-domain chat | Citations as shorthand; no URLs | None | Enhanced fields hallucinate (UCMJ, wrong clause); base 9/9 correct | [HF stats](https://datasets-server.huggingface.co/statistics?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train) |
| Zenodo 20509007 | 7 statutes (PPC, CrPC, QSO, MFLO, TPA, Police Order 2002, Limitation Act) + lawyer QA; ~5.4 MB | "parsed from official PDF versions" (no URL/edition) | CC-BY-4.0 | Missing PPC 295-A/B/C, 489-F; CrPC 164, 498, 561-A; Limitation Schedule; no post-2006 amendments | [Zenodo](https://zenodo.org/api/records/20509007) |
| SyedAhtsham repo | 1,000 SC PDFs (stored twice); 8 informal categories | Scraped from supremecourt.gov.pk by Dec 2021 | None | No metadata; tokens only; 29 empty token files; MAP 0.003 | [GitHub](https://api.github.com/repos/SyedAhtsham/Pakistani-Law-Cases-Search-Engine) |

## C5. Legal provisions (verbatim or near-verbatim)

| Provision | Text / effect | Source |
|---|---|---|
| Copyright Ord. s.57(1)(q)(i) | Reproduction of "any matter which has been published in any official Gazette" not infringement unless prohibited by Government | [Pakistan Code PDF](https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf) |
| Copyright Ord. s.57(1)(q)(ii) | "any judgment or order of a court, tribunal or other judicial authority, unless … prohibited by the court" | Same |
| Copyright Ord. s.2 "Government work" | Includes work made or published under control of "any court, tribunal or other judicial or legislative authority in Pakistan" | Same |
| JJSA 2018 s.13(1), (3), Explanation | Up to 3 years for publishing juvenile identity; up to 2 years for Juvenile Court proceedings without permission; HC/SC judgments exempt | [JJSA PDF](https://lpr.adb.org/sites/default/files/2024-07/pakistan-juvenile-justice-system-act-2018.pdf) |
| s.376A PPC (2016) | Offence of publishing rape-victim identity, up to 3 years; Explanation illegible | [Gazette scan](https://sld.com.pk/wp-content/uploads/2021/04/1485428121_999.pdf) |
| LHC 2024 direction | "Henceforth, they shall identify the victims using acronyms rather than full names." | [Dawn](https://dawn.com/news/1828670/lhc-asks-judges-to-protect-rape-victims-identity-in-verdicts) |
| GB Order 2018 s.60(3) | PM may adopt "any amendment in the existing laws or any new law in force in Pakistan" | [GB Order PDF](https://gilgitbaltistan.gov.pk/storage/downloads/GB%20Order%202018.pdf) |

---

# Part D — Evidence and citation table

| # | Key finding | Evidence | Source URL(s) |
|---|---|---|---|
| D1 | SC robots blocks AI crawlers and reserves AI training | `User-agent: ClaudeBot Disallow: /`; `Content-Signal: search=yes,ai-train=no,use=reference` | https://scp.gov.pk/robots.txt |
| D2 | SC search is CAPTCHA-gated | Loads reCAPTCHA v3; token in `recaptchaV3Token` | https://scp.gov.pk/JudgmentsSearch |
| D3 | SC PDFs not retrievable by automation | HTTP 403 Akamai on downloads_judgements | https://www.supremecourt.gov.pk/downloads_judgements/c.p._2972_2022.pdf |
| D4 | FSC publishes only Shariat petitions online | 169 judgments; criminal and suo motu "Under Construction" | https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php ; https://www.federalshariatcourt.gov.pk/criminaljudgments.html |
| D5 | FSC PDF carries PLD headnotes | Text begins "P L D 2025 Federal Shariat Court 1" | https://www.federalshariatcourt.gov.pk/shariatjudgment2.2.php?download=128 |
| D6 | IHC open via JSON, no robots, disclaimer only | 404 robots; `srchDecisionClms` returned 97 records | https://mis.ihc.gov.pk/frmJgmnt ; https://mis.ihc.gov.pk/ihc.asmx/srchDecisionClms |
| D7 | LHC reserves downloading | "should not be downloaded without prior agreement" | https://lhc.gov.pk/reported_judgments |
| D8 | LHC publishes a tiny fraction of disposals | 173,229 disposed in 2025 vs 704 + 59 AFR items | https://lhc.gov.pk/system/files/Annual%20Report%202025.pdf ; https://data.lhc.gov.pk/reported_judgments/judgments_approved_for_reporting |
| D9 | SHC is the largest official corpus | 77,258 uploads / 13,274 AFR (sitting judges) | https://caselaw.shc.gov.pk/caselaw/public/rpt-afr |
| D10 | SHC requires Registrar's consent | "without first obtaining written consent from the Registrar" | https://sindhhighcourt.gov.pk/disclaimer.php |
| D11 | PHC is the largest open corpus | 5,949 records 2009–2026, one POST | https://peshawarhighcourt.gov.pk/PHCCMS/reportedJudgments.php?action=search |
| D12 | BHC PDFs are robots-disallowed | `Disallow: /media/` | https://bhc.gov.pk/robots.txt |
| D13 | AJK SC open via REST | 704 posts in category 18; robots allow | https://ajksupremecourt.gok.pk/wp-json/wp/v2/categories?per_page=50 ; https://ajksupremecourt.gok.pk/robots.txt |
| D14 | FST and ATIR publish nothing | "Account Suspended"; "No Record Found In Database" | https://www.fst.gov.pk/robots.txt ; https://atir.gov.pk/Judgements |
| D15 | FTO full feed is only 15 days long | "will remain accessible … for a period of 15 days" | http://onlinecomplaints.cloudns.asia:4041/presentation/showalldecisions |
| D16 | Judgments and Gazette matter reproducible under copyright law | s.57(1)(q)(i)–(ii) | https://pakistancode.gov.pk/pdffiles/administratorc8dc84cf91fcedf0a4a00fc2710945a1.pdf |
| D17 | Commercial and free aggregators forbid scraping | PakistanLawsite "must not copy, download, scrape"; Pakistan Case Law "AI model-training crawlers are not permitted" | https://www.pakistanlawsite.com/ ; https://pakistancaselaw.com/terms |
| D18 | Juvenile identity bar exempts only HC/SC judgments | JJSA s.13 Explanation | https://lpr.adb.org/sites/default/files/2024-07/pakistan-juvenile-justice-system-act-2018.pdf |
| D19 | Court PDFs contain personal financial data | IHC sample includes litigant's IBAN | https://mis.ihc.gov.pk/attachments/judgements/209540/1/Muhammad_Usman_v_FoP_WP_No_1553_of_2026__J_Arbab_Muhammad_Tahir__Approved_for_Reporting_639280833781874862.pdf |
| D20 | Pakistan Code disclaims authenticity | "should not be taken as authentic or error-free" | https://pakistancode.gov.pk/english/UY2FqaJw1-apaUY2Fqa-apaUY2Fvbpw%3D-sg-jjjjjjjjjjjjj |
| D21 | KP Code consolidates but lags ~6 months | FAQ "revised form"; Assembly to Act XXI/2026 vs Code VII–IX/2026 | https://kpcode.kp.gov.pk/homepage/faq ; https://www.pakp.gov.pk/act/ |
| D22 | Balochistan Code is as-enacted with separate amendments | 1,790 entries; 673 titles contain "amend" | https://balochistancode.gob.pk/laws_rules.aspx?wise=alphabetical&opento=1 |
| D23 | Balochistan printing host opts out of AI training | `Content-Signal: … ai-train=no`; ClaudeBot disallowed | https://printing.balochistan.gov.pk/robots.txt |
| D24 | GB has no working statute code | Test rows; 3/3 PDFs 404; legacy domains down | https://gbassembly.gbit.gov.pk/pages/acts ; https://gba.gov.pk/acts/ |
| D25 | AJK has the broadest as-enacted regional collection | 1,015 Act PDFs; 1,143 Ordinance PDFs | https://law.gok.pk/acts/ ; https://law.gok.pk/ordinance/ |
| D26 | D2 is traceable to official URLs | Per-row `pdf_url` + `pdf_sha256`; robots honoured | https://huggingface.co/datasets/endomorphosis/ipfs_pakistan_provincial_laws/raw/main/README.md |
| D27 | D3 is one-third off-topic | 3,478 null-domain rows ("How do you cook ribs?") | https://datasets-server.huggingface.co/filter?dataset=abdullah693/adaption-pakistan-law-qa-pairs&config=default&split=train&where=%22domain%22%20IS%20NULL&length=5 |
| D28 | Zenodo dataset incomplete and stale | No CPC; missing lettered PPC sections; no amendment after 2006 | https://zenodo.org/api/records/20509007 |
| D29 | GitHub repo is a 1,000-PDF student snapshot | Report: "scraped website https://www.supremecourt.gov.pk/"; 1,000 cases | https://github.com/SyedAhtsham/Pakistani-Law-Cases-Search-Engine/blob/main/CaSearch%20Report.pdf |
| D30 | Neutral citations are court-specific and only in metadata | LHC `2025 LHC 8083`; SHC `2026 SHC KHI 2016`; PHC `2025 PHC 14` | https://data.lhc.gov.pk/dynamic/approved_judgments_result_new.php?year=2025&debug=0&courtName=All%20Courts&caseNumber=&citationTag=&partyName=&decisionDate0=&decisionDate1=&uploadDate=&uploadDate1= ; https://caselaw.shc.gov.pk/caselaw/pview.php?rpt=search |

---

# Part E — Research gap report

## E1. Federal, ICT, Punjab and Sindh statutes (gap filled 13 Nov 2026)

The dedicated research track for these four jurisdictions stopped early. A follow-up pass on 12–13 November 2026 fetched the sources directly; full notes are in `research_notes/Pakistan case law and statute sources/statutes_federal_ict_punjab_sindh.md`.

| Question | Finding (fetched) |
|---|---|
| Pakistan Code size and structure | 1,037 laws in the A–Z listing; each listing entry carries category, Act number and promulgation date; per-year chronological pages (`LGu0xBD?year=YYYY`) and a "Latest Ordinances" page (`KmTY5e.php`) expose new laws |
| Pakistan Code robots and terms | robots.txt disallows `/pdffiles/` for Googlebot only; disclaimer says texts are "for general informational purposes only… not… authentic", Gazette prevails |
| ICT | No separate official statute portal and no ICT category on Pakistan Code; 46 ICT-titled laws sit in the federal list |
| Punjab Code | 746 laws; listing shows "Last Updated On" dates and a `recently_updated` page; robots.txt returns HTTP 403 (no readable rules) |
| Sindh Code | 1,383 Acts/Ordinances via letter filter (unfiltered paging is unstable); robots.txt `Allow: /`; Rules listing exists |
| Sindh Civil Courts Ordinance 1962 | **Found:** consolidated to Sindh Act VI of 2025 at the Sindh Judicial Academy (sja.gos.pk), 19-page text PDF — official but secondary (tier 2) |
| Sindh Land Revenue Act 1967 | **Still missing:** Board of Revenue Sindh site unreachable; not on Sindh Code or SJA |
| Assemblies | National Assembly `/en/acts-tenure.php` (132 PDFs, to 2026); Sindh Assembly `/acts/details/…` |

**Still open:** Sindh Land Revenue Act 1967; Punjab crawl rules (robots.txt 403); rules/SRO and Urdu inventories; an online federal Gazette archive; what blncode.pitb.gov.pk is.

## E2. Inaccessible or unverified sources

| Source | Problem | Consequence |
|---|---|---|
| www.supremecourt.gov.pk (PDFs, robots, WP listings) | HTTP 403 (Akamai); TLS failure without www | SC PDF format, extractability and on-face citation unverified; need a manual browser download |
| scp.gov.pk/JudgmentsSearch | reCAPTCHA v3 | Total SC count and earliest year unknown |
| fccp.gov.pk | JS-only SPA, no robots | Federal Constitutional Court output unprofiled |
| api.bhc.gov.pk/v2/judgments | 302 to login on direct call | BHC portal coverage (all vs reported) unknown |
| bhc.gov.pk/media/ | robots disallow | BHC PDF format untested |
| fst.gov.pk | Account suspended | No FST decisions; alternative domain unknown |
| atir.gov.pk | Empty; official status unconfirmed (donor-built) | No ATIR decisions online |
| gba.gov.pk; GB Assembly PDFs | Expired certificate; 404s | GB Acts largely unobtainable online |
| blncode.pitb.gov.pk | TCP connect fails | Identity unknown |
| SHC Report001 | Embedded 404 | Seat-wise totals unavailable |
| pid.gov.pk press release (National Law Digest) | TLS certificate error | Status of 2023 "National Law Digest" proposal unknown |
| Eastern Book Co. v. Modak primary sources | Connection refused/reset | Headnote-copyright reasoning known only from snippet |
| NJPMC AI guidelines (Feb 2026) | Not fetched | Unknown whether they address third-party AI use of judgments |

## E3. Unresolved questions

| Domain | Open question |
|---|---|
| Legal | Do website terms and robots signals (LHC, SHC, SC, BHC) bind reuse that s.57(1)(q) permits? Does s.57(1)(q)(ii) cover adaptation (translation, AI summaries)? Does s.376A PPC have a superior-court Explanation like JJSA s.13? Are consolidated portal texts (not Gazette prints) covered by s.57(1)(q)(i)? Has s.57 been amended since 2000 (the Pakistan Code PDF matches the quoted text, but amendment history was not traced)? |
| Courts | When and by what instrument were LHC, SHC, PHC and SC neutral citations introduced? Are non-AFR LHC PDFs at predictable URLs (deliberately not probed)? Total counts and earliest years for IHC, SC and SHC (including former judges)? Share of scanned PDFs per court (samples of 1–3 only)? Are any court orders restricting publication flagged anywhere machine-readably? |
| Tribunals | Provincial service tribunals, AJK/GB service tribunals, banking, consumer and environmental forums: not covered or shallowly searched. No standalone CAT website found. |
| Statutes | Legal status of KP merged-district Continuation Acts 2018/2019; list of federal laws extended to GB or the merged districts; whether the AJK Interim Constitution PDF includes all amendments; KP Code disclaimer text; GB Order 2018's current constitutional status. |
| Datasets | D1 record count and duplicate rate; D3 source of 3,478 chat rows and the LEGAL-UQA licence; how many records in the federal sibling `ipfs_pakistan_laws` came from Common Crawl; content of Zenodo 21671415. |
| Data protection | Stage of the Personal Data Protection Bill; family-court confidentiality rules; provincial child-protection media bars (e.g. KP 2010 Act). |

---

# Part F — Final summary and actionable conclusions

**Bottom line.** PJN can lawfully start building a judgment corpus this week from about 8,300 openly published official documents. The corpus becomes nationally representative only once the Supreme, Lahore, Sindh and Balochistan High Courts grant permission. The statute corpus is now tracked automatically from the official code sites (Part E1 and the source-sync pipeline); it still needs alternative official sourcing for GB and for the Sindh Land Revenue Act 1967. The pipeline must handle OCR, headnote stripping, anonymisation and self-built version history from day one.

| Priority | Action | Why | Basis |
|---|---|---|---|
| 1 | Ingest Tier 1 now with a polite, identified crawler: PHC (one POST), FSC listing, AJK SC via REST, AJK HC, SAC GB, GBCC, CCP/CAT, FTO curated decisions | About 8,300 documents with no robots or CAPTCHA barrier | Parts A, C1, C2 |
| 1 | Start a daily FTO signed-findings collector immediately | The full feed only persists for 15 days; every day lost is unrecoverable | D15 |
| 1 | Send formal permission letters to the SC Registrar / Research Centre (request data feed or API), the LHC Registrar / Director IT, the SHC Registrar and the BHC Registrar. Cite their notices, PJN's attribution and link-back terms, and no-alteration commitments | Unlocks ~90% of identifiable volume plus apex precedent | D1–D3, D7, D10, D12 |
| 1 | Run the source-sync pipeline (`backend/scripts/sync_sources.py`) on a schedule so the inventory of ~5,500 official statutes stays current and new laws are fetched automatically | Statute coverage verified (E1); new laws must not wait for manual work | E1 |
| 2 | Ingest the Sindh Civil Courts Ordinance 1962 from the Sindh Judicial Academy (tier 2); obtain the Sindh Land Revenue Act 1967 from the Gazette or Board of Revenue | One core Sindh statute found, one still missing | E1 |
| 2 | IHC: ingest via JSON endpoints at ≤1 request per 2–5 s off-peak, and send a courtesy permission letter | Technically open; fragile server; disclaimer | D6 |
| 2 | KP and Balochistan statutes: ingest from KP Code + KP Assembly and Balochistan Code + Assembly. Use D2 as the gap-finder and check its `pdf_sha256` values against fresh fetches | Covers the 6-month KP lag and Balochistan's as-enacted model | D21, D22, D26 |
| 2 | AJK statutes: ingest law.gok.pk Acts, Ordinances and the Adopted Laws table, with OCR for the 2023 scans | Broadest regional collection | D25 |
| 2 | GB: request the statute corpus from the GB Law and Prosecution Department or Assembly (FOI/RTI if needed); tag federal laws as "applies in GB only if adapted" | No working online code | D24 |
| 2 | Build pipeline safeguards: English + Urdu OCR; PLD/reporter headnote stripping; anonymisation of juveniles, rape victims and their families (mandatory for subordinate-court material, best practice for all sexual-offence, juvenile and family cases); PII redaction (IBANs, CNICs) | Criminal exposure under JJSA s.13 and s.376A; personal data in PDFs | D5, D18, D19 |
| 2 | Data model: take citations from listing metadata; allow multiple neutral and reporter citations per document; key on listing row + SHA-256; store fetch URL and date; re-check robots.txt before every run | Citations not in PDFs; filenames unstable; spam injection on PHC/BHC; SHC could switch on content signals | D30, Part A |
| 3 | Build point-in-time statute versions from principal Acts plus dated amendment instruments; curate repeal status manually | No official source offers it | Part A statutes |
| 3 | Commission counsel review of: the effect of site terms versus s.57(1)(q); adaptation and translation; the s.376A Explanation; consolidated portal text under (q)(i). Also read the NJPMC AI guidelines | Unresolved legal questions | E3 |
| 3 | Datasets: adopt D2 as a KP/Balochistan gap-finder only. Vet `endomorphosis/ipfs_pakistan_laws` as a federal cross-check. Use the Zenodo lawyer questions (CC-BY-4.0, with attribution) and D3 rows 0–7716 base fields as internal evaluation prompts only, after licence clearance for D3. Use the GitHub 1,000-case list as an SC regression set once official access exists. Drop D1. Do not train on any of them | None is citable; each has a narrow supporting use | Part A datasets, C4 |
| 3 | Do not use pakistanlawsite.com, pakistancaselaw.com or pakcaselaw.duckdns.org as sources, and do not use the SHC raw-IP hosts with embedded credentials | Terms prohibit it; unofficial or insecure | D17 |
