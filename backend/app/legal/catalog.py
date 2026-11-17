"""Team law catalogs (frontend/data/catalog/*.json) -> manifest rows backed by direct official PDFs.

The catalogs list laws by title, year and jurisdiction, but carry no legal text and no direct PDF link
(official_pdf_url is empty and most links point to a portal home page). This module:

  * separates real instruments from portal/search-page entries,
  * applies corrections for catalog titles that do not exist as written on the official code sites,
  * matches each instrument to its listing on the official code website of its jurisdiction.

Matching is strict: same site, same normalised name, same year. Anything unmatched stays metadata-only.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from app.legal.official_codes import Listing

# Catalog entries whose title/year is not how the law exists on the official code site.
# key: (jurisdiction, catalog title)  ->  (title to match on the official site, display title, note)
CORRECTIONS: dict[tuple[str, str], tuple[str, str, str]] = {
    ("Federal", "Consumer Protection Act, 2019"): (
        "Islamabad Consumers Protection Act, 1995", "Islamabad Consumers Protection Act, 1995",
        "Pakistan Code has no federal 'Consumer Protection Act, 2019'. Consumer protection is provincial; "
        "the federal-capital law is the Islamabad Consumers Protection Act, 1995."),
    ("Federal", "Minimum Wages and Modes of Payment Ordinance, 1961"): (
        "Minimum Wages Ordinance, 1961", "Minimum Wages Ordinance, 1961",
        "Official title is 'Minimum Wages Ordinance, 1961'."),
    ("Federal", "Workers' Welfare Fund Ordinance, 2001"): (
        "Workers' Welfare Fund Ordinance, 1971", "Workers' Welfare Fund Ordinance, 1971",
        "The Workers' Welfare Fund Ordinance is of 1971, not 2001."),
    ("Federal", "Right to Information Act, 2002"): (
        "Right of Access to Information Act, 2017", "Right of Access to Information Act, 2017",
        "The Freedom of Information Ordinance, 2002 was replaced by the Right of Access to Information Act, 2017."),
    ("Federal", "National Accountability Bureau Ordinance, 1999"): (
        "National Accountability Ordinance, 1999", "National Accountability Ordinance, 1999",
        "Official title is 'National Accountability Ordinance, 1999'."),
    ("Khyber Pakhtunkhwa", "Khyber Pakhtunkhwa Consumer Protection Act, 2020"): (
        "Consumers Protection Act, 1997", "Khyber Pakhtunkhwa Consumers Protection Act, 1997",
        "KP Code lists no 2020 Act; the consumer law it publishes is the Consumers Protection Act, 1997."),
    ("Khyber Pakhtunkhwa", "Khyber Pakhtunkhwa Land Revenue Act"): (
        "West Pakistan Land Revenue Act, 1967", "West Pakistan Land Revenue Act, 1967 (Khyber Pakhtunkhwa)",
        "KP Code publishes it as 'The West Pakistan Land-Revenue Act, 1967'."),
    ("Sindh", "Sindh Consumer Protection Act, 2015"): (
        "Sindh Consumer Protection Act, 2014", "Sindh Consumer Protection Act, 2014",
        "The Act is titled 2014 on the Sindh Code (it was published in 2015)."),
}

# Catalog rows that are not a single law (a policy area, not an instrument).
NOT_INSTRUMENTS = {("Sindh", "Sindh Labour Policy / Labour Laws")}

ID_PREFIX = {"Federal": "PK", "Punjab": "PB", "Khyber Pakhtunkhwa": "KP", "Balochistan": "BL", "Sindh": "SD"}
SOURCE_NAME = {"Federal": "Pakistan Code", "Punjab": "Punjab Code", "Khyber Pakhtunkhwa": "KP Code",
               "Balochistan": "Balochistan Code", "Sindh": "Sindh Code"}
PROVINCE_LABEL = {"Punjab": "Punjab", "Khyber Pakhtunkhwa": "KP", "Balochistan": "Balochistan", "Sindh": "Sindh"}
PORTAL_HOME = {"Federal": "https://pakistancode.gov.pk/english/", "Punjab": "https://punjabcode.punjab.gov.pk/",
               "Khyber Pakhtunkhwa": "https://kpcode.kp.gov.pk/", "Balochistan": "https://balochistancode.gob.pk/",
               "Sindh": "https://www.sindhlaws.gov.pk/SindhIndex.aspx"}
HIGH_PRIORITY_CATEGORIES = {
    "constitutional", "criminal procedure", "civil procedure", "criminal law", "evidence / procedure", "cybercrime",
    "consumer protection", "family law", "family / child protection", "land / revenue", "property / criminal",
    "gender / workplace",
}

_PROVINCE_WORDS = re.compile(r"\b(the|west pakistan|punjab|sindh|sind|khyber pakhtunkhwa|nwfp|kp|balochistan|baln|"
                             r"islamabad capital territory)\b")
_ABBREVIATION = re.compile(r"\([A-Z][A-Za-z]?[A-Z]{1,4}\)")          # (PPC) (CrPC) (QSO) (PECA)
_SITE_NOTE = re.compile(r"\([^)]*(?:same as|under review|repealed|amendment-)[^)]*\)", re.I)


def _strip_notes(text: str) -> str:
    return _SITE_NOTE.sub(" ", _ABBREVIATION.sub(" ", text))


def plain(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("‘", "'")).strip()


def year_of(title: str, fallback: str = "") -> str:
    # Ignore years inside site notes such as "(Repealed by Act X of 2012)" or "(... FBR dated 30-06-2025)".
    years = re.findall(r"\b(1[89]\d\d|20\d\d)\b", _strip_notes(title))
    if years:
        return years[-1]
    return fallback if re.fullmatch(r"1[89]\d\d|20\d\d", fallback or "") else ""


def name_key(title: str) -> str:
    """Comparable name without year, province prefix, abbreviations or site notes."""
    text = _strip_notes(plain(title)).lower()
    text = re.sub(r"\b(1[89]\d\d|20\d\d)\b", " ", text)
    text = text.replace("land- revenue", "land revenue").replace("'", "")
    text = _PROVINCE_WORDS.sub(" ", text)
    words = re.findall(r"[a-z0-9]+", text)
    words = [w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w for w in words]
    return " ".join(words)


@dataclass
class Target:
    jurisdiction: str
    display_title: str
    match_title: str
    year: str
    category: str = ""
    catalog_titles: list[str] = field(default_factory=list)
    existing_id: str = ""        # manifest row this upgrades, if any
    note: str = ""

    @property
    def key(self) -> tuple[str, str, str]:
        return self.jurisdiction, name_key(self.match_title), self.year


def is_portal(entry: dict) -> bool:
    return (entry.get("instrument_type") in {"Source", "Judgments"} or entry.get("category") == "All Categories"
            or "—" in entry.get("title", ""))


def load_catalogs(paths: list[Path]) -> tuple[list[Target], list[dict], list[dict]]:
    """Return (instrument targets deduplicated, portal entries, skipped entries)."""
    targets: dict[tuple[str, str, str], Target] = {}
    portals: dict[str, dict] = {}
    skipped: list[dict] = []
    for path in paths:
        for entry in json.loads(path.read_text(encoding="utf-8")):
            jurisdiction = entry.get("jurisdiction", "")
            title = plain(entry.get("title", ""))
            if is_portal(entry):
                portals.setdefault(entry.get("official_text_url", ""), {
                    "jurisdiction": jurisdiction, "title": title, "url": entry.get("official_text_url", ""),
                    "authority": entry.get("source_authority", ""), "catalog": path.name})
                continue
            if (jurisdiction, title) in NOT_INSTRUMENTS or jurisdiction not in ID_PREFIX:
                skipped.append({"jurisdiction": jurisdiction, "title": title, "catalog": path.name,
                                "reason": "not a single legal instrument"})
                continue
            match_title, display, note = CORRECTIONS.get((jurisdiction, title), (title, title, ""))
            target = Target(jurisdiction, display, match_title, year_of(match_title, entry.get("year", "")),
                            entry.get("category", ""), [title], note=note)
            existing = targets.get(target.key)
            if existing:
                if title not in existing.catalog_titles:
                    existing.catalog_titles.append(title)
            else:
                targets[target.key] = target
    return list(targets.values()), list(portals.values()), skipped


def match(target: Target, listings: list[Listing]) -> list[Listing]:
    wanted_name, wanted_year = name_key(target.match_title), target.year
    return [item for item in listings if name_key(item.title) == wanted_name and year_of(item.title) == wanted_year
            and not re.search(r"\brepeal", item.title, re.I)]  # never ingest a version the site marks repealed


def slug(title: str) -> str:
    text = _strip_notes(plain(title)).lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")[:80]


def document_type(jurisdiction: str, title: str) -> str:
    kind = "Order" if re.search(r"\border\b", title, re.I) else (
        "Ordinance" if re.search(r"\bordinance\b", title, re.I) else "Act")
    if jurisdiction == "Federal":
        return f"Federal {kind}"
    return f"{PROVINCE_LABEL[jurisdiction]} Law"


def authority(jurisdiction: str, title: str) -> str:
    is_act = not re.search(r"\b(ordinance|order)\b", title, re.I)
    if jurisdiction == "Federal":
        return "Parliament of Pakistan" if is_act else "Government of Pakistan"
    if jurisdiction == "Khyber Pakhtunkhwa":
        return "Provincial Assembly of Khyber Pakhtunkhwa" if is_act else "Government of Khyber Pakhtunkhwa"
    if jurisdiction == "Punjab":
        return "Provincial Assembly of the Punjab" if is_act else "Government of the Punjab"
    return f"Provincial Assembly of {jurisdiction}" if is_act else f"Government of {jurisdiction}"


def priority(category: str) -> str:
    return "High" if category.lower() in HIGH_PRIORITY_CATEGORIES else "Medium"
