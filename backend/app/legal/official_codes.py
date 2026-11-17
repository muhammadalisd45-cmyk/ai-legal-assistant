"""Read the public law listings of Pakistan's official code websites and find each law's direct PDF.

Used by scripts/resolve_catalog.py to turn catalog rows (title + year, no text) into manifest rows that
point at a direct official PDF, so scripts/acquire_corpus.py can download and validate the real text.

Every site here is a government portal; nothing is fetched from reporters or third-party mirrors.
Listings give (title, detail page); the PDF link is read from the detail page only for laws we need.
"""
from __future__ import annotations

import html
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import urljoin

import httpx

from app.legal.acquisition import ssl_context

USER_AGENT = "PakistanJusticeNavigator/0.3 (+legal-information research corpus)"


@dataclass
class Listing:
    site: str           # pakistan_code | punjab_code | kp_code | balochistan_code | sindh_code
    jurisdiction: str   # Federal | Punjab | Khyber Pakhtunkhwa | Balochistan | Sindh
    title: str
    detail_url: str     # page that shows the law (may equal pdf_url)
    pdf_url: str = ""   # filled directly when the listing links the PDF
    meta: str = ""      # the listing's metadata line (category | Act No. | promulgation date | last updated ...)
    urdu_pdf_url: str = ""


def clean_meta(raw: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", text).strip(" |")


def clean_title(raw: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = text.replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", text).strip(" .,")


class Fetcher:
    """Polite GET/POST with an optional on-disk cache (development only) and a small delay between calls."""

    def __init__(self, cache_dir: Path | None = None, delay: float = 0.4, log: Callable[[str], None] = print):
        self.client = httpx.Client(timeout=120, follow_redirects=True, verify=ssl_context(),
                                   headers={"User-Agent": USER_AGENT})
        self.cache_dir = cache_dir
        self.delay = delay
        self.log = log
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_path(self, key: str) -> Path | None:
        if not self.cache_dir:
            return None
        return self.cache_dir / (re.sub(r"[^A-Za-z0-9]+", "_", key)[-180:] + ".html")

    def text(self, url: str, data: dict | None = None, cache_key: str | None = None) -> str:
        path = self._cache_path(cache_key or url)
        if path and path.exists():
            return path.read_text(encoding="utf-8")
        for attempt in range(3):
            try:
                response = self.client.post(url, data=data) if data is not None else self.client.get(url)
                response.raise_for_status()
                break
            except httpx.HTTPError as exc:
                if attempt == 2:
                    raise
                self.log(f"retry {url}: {exc}")
                time.sleep(2 + attempt * 3)
        body = response.text
        if path:
            path.write_text(body, encoding="utf-8")
        time.sleep(self.delay)
        return body

    def close(self) -> None:
        self.client.close()


# --------------------------------------------------------------------------------------------------
# Listings
# --------------------------------------------------------------------------------------------------

PAKISTAN_CODE = "https://pakistancode.gov.pk/english/"
# <a href="UY2FqaJw1-...">Title</a></div> ... <div class='accordion-section-content' ...> Civil Laws | IX of 1872 | ...
_PC_ENTRY = re.compile(r'<a href="(UY2FqaJw1-[^"]+)">(?:<strong>[^<]*</strong>)?\s*([^<]+)</a>\s*</div>.*?'
                       r"accordion-section-content'[^>]*>(.*?)</div>", re.S)


def pakistan_code_listings(f: Fetcher) -> list[Listing]:
    out: dict[str, Listing] = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        page = f.text(f"{PAKISTAN_CODE}LGu0xAD?alp={letter}&page=1&action=inactive")
        for href, title, meta in _PC_ENTRY.findall(page):
            url = urljoin(PAKISTAN_CODE, href)
            out.setdefault(url, Listing("pakistan_code", "Federal", clean_title(title), url, meta=clean_meta(meta)))
    return list(out.values())


PUNJAB_CODE = "https://punjabcode.punjab.gov.pk/en/"
# Punjab and KP share the listing markup: <div class="artlist"><a href="...">Title</a></div> <div class="artdets">meta</div>
_ARTLIST = re.compile(r'<div class="artlist">\s*<a href="([^"]+)"[^>]*>([^<]+)</a>\s*</div>\s*'
                      r'<div class="artdets"\s*>(.*?)</div>', re.S)


def punjab_code_listings(f: Fetcher) -> list[Listing]:
    out: dict[str, Listing] = {}
    offset = 0
    while True:
        page = f.text(f"{PUNJAB_CODE}alphabetical/all/100/{offset}" if offset else f"{PUNJAB_CODE}alphabetical")
        new = 0
        for url, title, meta in _ARTLIST.findall(page):
            if "punjabcode.punjab.gov.pk/en/show_article/" in url and url not in out:
                out[url] = Listing("punjab_code", "Punjab", clean_title(title), url, meta=clean_meta(meta))
                new += 1
        if not new:
            break
        offset += 100
    return list(out.values())


KP_CODE = "https://kpcode.kp.gov.pk/homepage/"


def kp_code_listings(f: Fetcher) -> list[Listing]:
    out: dict[str, Listing] = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        page = f.text(f"{KP_CODE}alphabetical//{letter}")
        for url, title, meta in _ARTLIST.findall(page):
            law_id = re.search(r"/lawDetails/(\d+)$", url)
            if law_id:
                url = f"{KP_CODE}lawDetails/{law_id.group(1)}"
                out.setdefault(url, Listing("kp_code", "Khyber Pakhtunkhwa", clean_title(title), url,
                                            meta=clean_meta(meta)))
    return list(out.values())


BALOCHISTAN_CODE = "https://balochistancode.gob.pk/"


def balochistan_code_listings(f: Fetcher) -> list[Listing]:
    page = html.unescape(f.text(f"{BALOCHISTAN_CODE}laws_rules.aspx?wise=alphabetical&opento=1"))
    out: dict[str, Listing] = {}
    for href, title, meta in re.findall(r"href='(Document\.aspx\?wise=opendoc&(?:amp;)?docid=\d+&(?:amp;)?docc=\d+)'>"
                                         r"([^<]+)</a></b><br><small>(.*?)</small>", page):
        url = urljoin(BALOCHISTAN_CODE, href.replace("&amp;", "&"))
        # Titles are rendered as "Name , YEAR"; drop the trailing duplicate year and stray file suffixes.
        name = re.sub(r"\s*,\s*\d{4}\s*$", "", clean_title(title))
        name = re.sub(r"\.docx?$", "", name, flags=re.I)
        name = re.sub(r"\bBaln\b", "Balochistan", name)
        out.setdefault(url, Listing("balochistan_code", "Balochistan", name, url, meta=clean_meta(meta)))
    return list(out.values())


SINDH_CODE = "https://sindhlaws.gov.pk/"


def _aspnet_state(page: str) -> dict:
    state = {}
    for name in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"):
        match = re.search(r'id="%s" value="([^"]*)"' % name, page)
        if match:
            state[name] = html.unescape(match.group(1))
    return state


# One grid row: <td>No.</td><td width="55%">TITLE</td><td><a ... href="setup/....pdf"> English </a></td>
#               <td><a ... [href=Urdu pdf]> Urdu </a></td><td>Sindhi</td><td>DATE</td>
_SINDH_ROW = re.compile(r'<td align="center" width="5%">([^<]*)</td>\s*<td align="left" width="55%">([^<]+)</td>\s*'
                        r'<td[^>]*>\s*<a[^>]*?href="([^"]+\.pdf)"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>\s*'
                        r'<td[^>]*>.*?</td>\s*<td[^>]*>([^<]*)</td>', re.I | re.S)


def sindh_code_listings(f: Fetcher) -> list[Listing]:
    """Sindh's unfiltered grid is unordered across postbacks, so filter by letter first, then page within it."""
    out: dict[str, Listing] = {}
    grid = "ctl00$ContentPlaceHolder1$GridView1"
    for kind in ("ACT", "ORDINANCE"):
        url = f"{SINDH_CODE}Alpha.aspx?pg={kind}"
        start = f.text(url)
        for letter_no in range(1, 27):
            target = f"ctl00$ContentPlaceHolder1$rptAlphabets$ctl{letter_no:02d}$LinkButton1"
            page = f.text(url, data=_aspnet_state(start) | {"__EVENTTARGET": target, "__EVENTARGUMENT": ""},
                          cache_key=f"{url}#letter{letter_no}")
            page_no = 1
            while True:
                for number, title, href, urdu_cell, date in _SINDH_ROW.findall(page):
                    pdf = urljoin(SINDH_CODE, href)
                    name = re.sub(r"\.pdf$", "", clean_title(title), flags=re.I)
                    urdu = re.search(r'href="([^"]+\.pdf)"', urdu_cell)
                    meta = f"{kind.title()} {number.strip()} | Promulgation Date: {date.strip()}"
                    out.setdefault(pdf, Listing("sindh_code", "Sindh", name, pdf, pdf, meta=meta,
                                                urdu_pdf_url=urljoin(SINDH_CODE, urdu.group(1)) if urdu else ""))
                page_no += 1
                if f"Page${page_no}" not in html.unescape(page) or page_no > 60:
                    break
                page = f.text(url, data=_aspnet_state(page) | {"__EVENTTARGET": grid, "__EVENTARGUMENT": f"Page${page_no}"},
                              cache_key=f"{url}#letter{letter_no}#page{page_no}")
    return list(out.values())


SJA_UPDATED_LAWS = "https://sja.gos.pk/updated-laws/"


def sja_updated_laws_listings(f: Fetcher) -> list[Listing]:
    """Sindh Judicial Academy's consolidated ("amendments up to date") texts: official but secondary (tier 2)."""
    page = f.text(SJA_UPDATED_LAWS)
    out: dict[str, Listing] = {}
    # Rows are <td class="column-2"><a href="...pdf">Title</a></td><td class="column-3">(amended by ...)</td>;
    # the page sometimes closes links with a malformed "<a/>", so parse whole cells rather than anchors.
    for cell, note in re.findall(r'<td class="column-2">(.*?)</td>\s*<td class="column-3">(.*?)</td>', page, re.S):
        link = re.search(r'href="\s*h?(https://sja\.gos\.pk/[^"]+\.pdf)"', cell)
        name = clean_title(cell)
        if not link or len(name) < 6:
            continue
        url = link.group(1).strip().replace(" ", "%20")
        note = clean_meta(note).strip("() ")
        meta = "Sindh Judicial Academy consolidation" + (f" | amended up to: {note}" if note else "")
        out.setdefault(url, Listing("sja_updated_laws", "Sindh", name, url, url, meta=meta))
    return list(out.values())


SITES: dict[str, Callable[[Fetcher], list[Listing]]] = {
    "pakistan_code": pakistan_code_listings,
    "punjab_code": punjab_code_listings,
    "kp_code": kp_code_listings,
    "balochistan_code": balochistan_code_listings,
    "sindh_code": sindh_code_listings,
    "sja_updated_laws": sja_updated_laws_listings,
}

SITE_FOR_JURISDICTION = {
    "Federal": "pakistan_code", "Punjab": "punjab_code", "Khyber Pakhtunkhwa": "kp_code",
    "Balochistan": "balochistan_code", "Sindh": "sindh_code",
}


# --------------------------------------------------------------------------------------------------
# Direct PDF on a detail page
# --------------------------------------------------------------------------------------------------

_PDF_PATTERNS = {
    "pakistan_code": r'href="(https://pakistancode\.gov\.pk/pdffiles/[^"]+\.pdf)"',
    "punjab_code": r'href="(https://punjabcode\.punjab\.gov\.pk/uploads/articles/[^"]+\.pdf)"',
    "kp_code": r'(https://kpcode\.kp\.gov\.pk/uploads/[^"\'\s]+\.pdf)',
    "balochistan_code": r'(https?://balochistancode\.gob\.pk/lawdir/[^"\'\s]+\.pdf)',
}


def pdf_url(f: Fetcher, listing: Listing) -> str:
    if listing.pdf_url:
        return listing.pdf_url
    page = f.text(listing.detail_url)
    match = re.search(_PDF_PATTERNS[listing.site], page)
    if not match:
        return ""
    url = html.unescape(match.group(1))
    return url.replace("http://", "https://", 1)  # same host serves the file over verified TLS


def crawl(sites: Iterable[str], f: Fetcher) -> list[Listing]:
    listings: list[Listing] = []
    for site in sites:
        found = SITES[site](f)
        f.log(f"{site}: {len(found)} laws listed")
        listings.extend(found)
    return listings
