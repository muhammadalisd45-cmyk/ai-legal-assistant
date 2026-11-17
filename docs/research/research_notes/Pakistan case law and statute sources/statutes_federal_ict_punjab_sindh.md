# Statute sources: Federal, Islamabad Capital Territory, Punjab, Sindh (gap #1 fill)

Collected 2026-11-12/13 by direct HTTP fetches from this workstation (curl / httpx, polite single requests).
This replaces the research track that stopped early. Everything below marked **fetched** was actually downloaded;
nothing here is from search snippets. Counts come from full listing crawls run by
`backend/app/legal/official_codes.py` on 2026-11-12.

## 1. Source inventory

| Title | URL | Organisation | Category | Date / last updated | Credibility | Access status |
|---|---|---|---|---|---|---|
| Pakistan Code – alphabetical listing | https://pakistancode.gov.pk/english/LGu0xAD?alp=A&page=1&action=inactive (A–Z) | Ministry of Law and Justice | Federal statutes (listing) | crawled 2026-11-12 | Official, primary | fetched |
| Pakistan Code – chronological listing | https://pakistancode.gov.pk/english/LGu0xBD?year=2026&page=1&action=inactive | Ministry of Law and Justice | Federal statutes (by year) | crawled 2026-11-13 | Official, primary | fetched |
| Pakistan Code – latest ordinances | https://pakistancode.gov.pk/english/KmTY5e.php | Ministry of Law and Justice | New-law feed | crawled 2026-11-13 | Official, primary | fetched |
| Pakistan Code – category-wise | https://pakistancode.gov.pk/english/LGu0xVD.php | Ministry of Law and Justice | 23 subject categories | crawled 2026-11-13 | Official | fetched |
| Pakistan Code – Urdu section | https://pakistancode.gov.pk/english/UHyrdu.php | Ministry of Law and Justice | Urdu translations (PDF) | crawled 2026-11-13 | Official | fetched |
| Pakistan Code – disclaimer | https://pakistancode.gov.pk/english/Xki72HF.php | Ministry of Law and Justice | Terms | crawled 2026-11-13 | Official | fetched |
| Pakistan Code – robots.txt | https://pakistancode.gov.pk/robots.txt | Ministry of Law and Justice | Crawl rules | fetched 2026-11-13 | Official | fetched |
| Pakistan Code – sitemap | https://pakistancode.gov.pk/sitemap.xml | Ministry of Law and Justice | Crawl aid | lastmod 2026-03-04 | Official | fetched |
| Punjab Code – alphabetical | https://punjabcode.punjab.gov.pk/en/alphabetical (+ /all/100/{offset}) | Government of the Punjab (PITB) | Punjab statutes | crawled 2026-11-12 | Official, primary | fetched |
| Punjab Code – recently updated | https://punjabcode.punjab.gov.pk/en/recently_updated | Government of the Punjab | Amendment/new-law feed | crawled 2026-11-13 | Official | fetched |
| Punjab Code – rules | https://punjabcode.punjab.gov.pk/en/get_rules | Government of the Punjab | Rules | crawled 2026-11-13 | Official | fetched (structure only) |
| Sindh Code – Acts / Ordinances / Rules | https://sindhlaws.gov.pk/Alpha.aspx?pg=ACT · ?pg=ORDINANCE · ?pg=RULE | Government of Sindh | Sindh statutes | crawled 2026-11-12 | Official, primary | fetched |
| Sindh Code – robots.txt | https://sindhlaws.gov.pk/robots.txt | Government of Sindh | Crawl rules | fetched 2026-11-13 | Official | fetched |
| Sindh Judicial Academy – Updated Laws | https://sja.gos.pk/updated-laws/ | Sindh Judicial Academy (Govt of Sindh) | Consolidated texts | page fetched 2026-11-13 | Official, secondary compilation | fetched |
| National Assembly – Acts | https://www.na.gov.pk/en/acts-tenure.php | National Assembly of Pakistan | Acts as passed | fetched 2026-11-13 | Official | fetched |
| Provincial Assembly of Sindh – Acts | https://pas.gov.pk/acts | Provincial Assembly of Sindh | Acts as passed | fetched 2026-11-13 | Official | fetched |
| Provincial Assembly of the Punjab | https://www.pap.gov.pk/ | Provincial Assembly of the Punjab | Assembly site | fetched 2026-11-13 | Official | fetched (robots.txt 403) |
| Board of Revenue Sindh | https://borsindh.gov.pk/ | Board of Revenue, Sindh | Land revenue | 2026-11-13 | Official | **inaccessible** (connection failed, http and https) |
| Ministry of Law and Justice | https://molaw.gov.pk/robots.txt | Ministry of Law and Justice | Crawl rules | 2026-11-13 | Official | robots.txt 404 |

## 2. Raw extracted facts (quoted / measured, no interpretation)

### Pakistan Code (federal + ICT)
- Alphabetical crawl A–Z: **1,037 distinct law links** (each detail page links one direct PDF under `https://pakistancode.gov.pk/pdffiles/`).
- Each listing entry carries a metadata line, e.g. Contract Act: `Civil Laws | IX of 1872 | Promulgation Date: April 25 1872. … | Archive 0 | … Under Review`.
- Chronological page for 2026 lists **18** laws, first entry `Virtual Assets Act, 2026` — `General Laws | XIII of 2026 | Promulgation Date: March 04 2026`.
- "Latest Ordinances" page (fetched) lists, first: `Oil and Gas Regulatory Authority (Amendment) Ordinance, 2026`, `Islamabad Capital Territory Local Government (Amendment) Ordinance, 2026`, `Defence Industrial Production and Regulatory Authority of Pakistan Ordinance, 2026`.
- 23 subject categories (`catid=1..23`): Criminal, Civil, Family, Service, Labour, Police, Companies, Land/Property, Islamic/Religious, Banking/Financial, Evidence, Rent, International, Tenancy, Land Reform, Minorities, Excise/Taxation, Military, Health/Medical, Media, Election, Departmental, General. **No Islamabad Capital Territory category.**
- ICT laws are mixed into the federal list: 46 titles in the alphabetical crawl contain "Islamabad", "Capital Territory" or "ICT" (e.g. `ICT Rights of Persons with Disability Act, 2020`, `Islamabad Capital Territory (Prohibition of Plastic Book Covers) Act, 2026`).
- Some titles carry repeal notes, e.g. `Capital Territory Local Government Ordinance, 1979(Repealed by Act,X at 2015)`; tax laws carry `(Same as on the official website of FBR dated 30-06-2025)`.
- Disclaimer (verbatim): "All laws on the website are currently under review. They are for general informational purposes only, and should not be taken as authentic or error-free legislative instruments. If you have any questions about the accuracy or completeness of a law, please refer to the original source i.e. the relevant Gazette notification(s)."
- robots.txt (verbatim, complete): `https://pakistancode.gov.pk/sitemap.xml` / `User-agent: googlebot` / `Disallow: /pdffiles/`. No rule for other user agents; no Content-Signal line.
- sitemap.xml lists 5 navigation pages only (lastmod 2026-03-04), not individual laws.
- Urdu section links Urdu PDFs under `/pdffiles/administratorcurdu…pdf`.

### Punjab Code
- Alphabetical crawl (`/en/alphabetical/all/100/{offset}`): **746** laws; PDFs under `/uploads/articles/`.
- Listing metadata line, e.g. `Higher Education | Act LXXI of 2025 | Promulgation Date: Mon Aug 11, 2025 | Views: 3264 | Last Updated On: Tue Sep 02, 2025`.
- `/en/recently_updated` lists recently changed laws, e.g. `AGA KHAN PROPERTIES (SUCCESSION AND TRANSFER) ACT 2026` (`Board of Revenue | Act XLVI of 2026 | Promulgation Date: Wed Jun 24, 2026`), and older laws re-updated: `PUNJAB PRIVATE EDUCATIONAL INSTITUTIONS (PROMOTION AND REGULATION) ORDINANCE, 1984`.
- `/robots.txt` returned **HTTP 403** (Apache "Forbidden"); `law.punjab.gov.pk/robots.txt` and `pap.gov.pk/robots.txt` also 403. No crawl rules could be read.
- `PUNJAB LOCAL GOVERNMENT ACT 2022` is listed with no repeal marker; it is the only principal local-government Act in the listing.

### Sindh Code
- Letter-filtered crawl of Acts + Ordinances: **1,383** entries; English PDFs under `/setup/Publications_SindhCode/`. A Rules listing exists (`Alpha.aspx?pg=RULE`).
- The unfiltered grid returns rows in an unstable order across ASP.NET postbacks (paging it directly yielded only 146 unique rows); filtering by letter first is required.
- robots.txt (verbatim): `User-agent: *` / `Disallow: /admin/` `/App_Data/` `/bin/` `/obj/` `/scripts/` / `Allow: /` / `Sitemap: https://www.sindhlaws.gov.pk/sitemap.xml`.
- Principal **Sindh Civil Courts Ordinance, 1962** and **Sindh/West Pakistan Land Revenue Act, 1967** are not listed (only amendments, e.g. `SINDH CIVIL COURTS (AMENDMENT) ACT, 2021`, `THE SINDH CIVIL COURTS (AMENDMENT) ACT, 2025`).

### Sindh Judicial Academy (official, secondary)
- `https://sja.gos.pk/updated-laws/` links consolidated PDFs, including
  `https://sja.gos.pk/assets/Updated_Laws/Sindh%20Civil%20Court%20Ordinance%2C1962%20Final.pdf` — fetched: HTTP 200, `application/pdf`, 986,844 bytes, 19 pages, text layer (2,234 chars/page), cover: "The Sindh Civil Courts Ordinance, 1962 — Amendment up to date Sindh Act (No. VI of 2025) … SINDH JUDICIAL ACADEMY LIBRARY … Amendment up to date till 1st Mar, 2025".
- Also lists consolidated Sindh Rented Premises Ordinance 1979, Sindh Consumer Protection Act 2014 + Rules 2017, Sindh Child Marriages Restraint Act 2013, QSO 1984 (amended to 2025) and others.
- robots.txt: `Disallow: /wp-admin/`, `Disallow: /wp-content/uploads/wpforms/` only.
- No land-revenue law on the page.

### Assemblies
- National Assembly `/en/acts-tenure.php`: 132 PDF links; years present up to 2026.
- Provincial Assembly of Sindh `/acts`: detail pages `https://pas.gov.pk/acts/details/{a}/{b}` (e.g. `The Registration (Sindh Amendment) Act, 2024`).

## 3. Analysis

- **Change detection is feasible from official listings alone.** Pakistan Code's chronological year page and "Latest Ordinances" page, Punjab Code's `recently_updated` page and "Last Updated On" field, and full letter crawls of Sindh/KP/Balochistan give a complete diffable inventory. The sitemap is too coarse to help.
- **ICT has no separate official statute portal**; ICT law is identified by title within Pakistan Code. A jurisdiction tag "Islamabad Capital Territory" can be derived from the title for filtering.
- **Pakistan Code texts are non-authentic by the Ministry's own disclaimer**; the Gazette prevails. The product should keep the disclaimer next to citations, and treat "Under Review" status as a flag.
- **Crawl permission:** Pakistan Code restricts only Googlebot from `/pdffiles/`; Sindh Code allows all. Punjab's robots.txt is unreadable (403), so no explicit rule exists. Polite, identified, low-rate crawling is consistent with what is published.
- **The missing Sindh Civil Courts Ordinance has an official consolidated copy** at the Sindh Judicial Academy; it is a library compilation, so it should be tier 2 (official, secondary), not tier 1.
- **Sindh Land Revenue Act 1967 is still unavailable** from any official Sindh host reachable on 2026-11-13. The KP and Balochistan Codes carry their own copies of the West Pakistan Land Revenue Act 1967, but they are not authority for Sindh's text.

## 4. Gaps / unresolved

- Sindh Land Revenue Act 1967: Board of Revenue Sindh site unreachable; re-try, or obtain the Gazette copy.
- Punjab robots.txt returns 403; ask PITB for crawl guidance if collecting at scale.
- Rules / SROs: listings exist (Punjab `get_rules`, Sindh `pg=RULE`), not yet inventoried; FBR SROs not examined.
- Federal Gazette archive online: not located in this pass.
- Urdu versions: Pakistan Code has an Urdu PDF section; coverage not counted.
