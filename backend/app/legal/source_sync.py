"""Keep an inventory of every law published by the official code websites, and detect what changed.

Inputs / outputs (all under frontend/data/sources/):

  official_sources.csv   registry: one row per official source, with its real listing URL and the adapter that
                         reads it (edit this file to enable/disable sources; never put unofficial hosts here)
  law_inventory.csv/.json  one row per law found: title, year, Act No., promulgation date, the site's own
                         "last updated" date, the detail page and the DIRECT PDF link, first/last seen dates
  changes/YYYY-MM-DD.json  what changed in that run (new, listing_changed, pdf_changed, removed, reappeared)
  changes.csv            the same changes appended as one cumulative log
  sync_state.json        which sources already have a baseline (the first crawl of a source is a baseline,
                         so the existing back catalogue is not reported as "new")

The sync never downloads documents; scripts/sync_sources.py --ingest turns changes into manifest updates and
then runs the normal acquire -> validate -> index steps.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app.core.config import settings
from app.legal.catalog import name_key, slug, year_of
from app.legal.manifest_io import csv_text, write_text
from app.legal.official_codes import SITES, Fetcher, Listing, pdf_url

SOURCES_DIR = settings.manifest_path.parent / "sources"
REGISTRY_PATH = SOURCES_DIR / "official_sources.csv"
INVENTORY_CSV = SOURCES_DIR / "law_inventory.csv"
INVENTORY_JSON = SOURCES_DIR / "law_inventory.json"
CHANGES_DIR = SOURCES_DIR / "changes"
CHANGES_CSV = SOURCES_DIR / "changes.csv"
STATE_PATH = SOURCES_DIR / "sync_state.json"

INVENTORY_FIELDS = [
    "law_key", "source_id", "jurisdiction", "title", "year", "instrument_type", "is_amendment", "site_marked_repealed",
    "act_number", "promulgation_date", "category", "site_status", "source_last_updated",
    "detail_url", "pdf_url", "urdu_pdf_url", "pdf_checked_at",
    "first_seen", "last_seen", "last_changed", "removed", "listing_hash", "manifest_id",
]
CHANGE_FIELDS = ["run_date", "change", "law_key", "source_id", "jurisdiction", "title", "instrument_type",
                 "is_amendment", "pdf_url", "previous", "detail_url"]
# Below this share of the previous count, a crawl is treated as partial and nothing is marked removed.
PARTIAL_CRAWL_RATIO = 0.8
# More new/removed/re-linked laws than this in one run (per source) is treated as an anomaly, not as law.
ANOMALY_MIN_CHANGES = 25
ANOMALY_SHARE = 0.05
RECHECK_MISSING_PDF_DAYS = 30


# --------------------------------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------------------------------

@dataclass
class Source:
    source_id: str
    name: str
    jurisdiction: str
    content_type: str
    source_tier: int
    listing_url: str
    adapter: str
    collection_status: str
    refresh: str
    enabled: bool
    auto_ingest: bool
    extra: dict = field(default_factory=dict)

    @property
    def syncable(self) -> bool:
        return self.enabled and self.adapter in SITES and self.collection_status == "open"


def load_registry(path: Path | None = None) -> list[Source]:
    with (path or REGISTRY_PATH).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    sources = []
    for row in rows:
        sources.append(Source(
            source_id=row["source_id"], name=row["name"], jurisdiction=row["jurisdiction"],
            content_type=row["content_type"], source_tier=int(row.get("source_tier") or 1),
            listing_url=row["listing_url"], adapter=row["adapter"], collection_status=row["collection_status"],
            refresh=row["refresh"], enabled=row["enabled"].strip().lower() == "true",
            auto_ingest=row["auto_ingest"].strip().lower() == "true", extra=row))
    return sources


# --------------------------------------------------------------------------------------------------
# Turning a listing into an inventory record
# --------------------------------------------------------------------------------------------------

_ACT_NO = re.compile(r"\b((?:Act|Ordinance|Order|Regulation|P\.?O\.?)\s*(?:No\.?\s*)?)?([IVXLCDM]+|\d+)\s+of\s+(\d{4})\b", re.I)
_PROMULGATED = re.compile(r"Promulgation Date:\s*([^|]+?)\s*(?:\||$)")
_UPDATED = re.compile(r"Last Updated On:\s*([^|]+?)\s*(?:\||$)")
_VOLATILE = re.compile(r"\|?\s*(Views|Archive)\s*:?\s*\d+", re.I)

INSTRUMENT_PATTERNS = [
    ("Constitution", r"\bconstitution of\b"),
    # "S. R." / "SR" = Service Rules in Balochistan Code titles
    ("Rules", r"\brules?\b|\bS\.\s?R\b\.?|\bSR\b|\bmanual\b"),
    ("Regulations", r"\bregulations?\b"),
    ("Notification", r"\bnotification\b|\bS\.?R\.?O\b"),
    ("Policy", r"\bpolicy\b|\bguidelines?\b"),
    # including the abbreviation "Ord" and misspellings seen on the Balochistan Code
    ("Ordinance", r"\bord(?:inance|ianace|iance|ninace|inanace)?\b"),
    ("Order", r"\border\b"),
    ("Code", r"\bcode\b"),
    ("Act", r"\bact\b|\(amendment\) ac$"),
]
PRINCIPAL_TYPES = {"Constitution", "Ordinance", "Order", "Code", "Act"}


def _classify(text: str) -> str:
    for kind, pattern in INSTRUMENT_PATTERNS:
        if re.search(pattern, text, re.I):
            return kind
    return "Other"


def instrument_type(title: str) -> str:
    """Instrument kind from the title, ignoring parenthetical notes such as "(Repealed by Ord. 52 of 2001)"
    or "(Order XXXIX)", which would otherwise decide the type; falls back to the full title."""
    lowered = re.sub(r"\.(pdf|docx?)$", "", title.strip().lower())
    core = re.sub(r"\([^)]*\)|\([^)]*$", " ", lowered)
    kind = _classify(core)
    if kind != "Other":
        return kind
    return _classify(re.sub(r"\([^)]*repeal[^)]*\)?", " ", lowered))  # never classify by a repeal note


def is_amendment(title: str) -> bool:
    return bool(re.search(r"\bamend(ment|ing)?\b|\bamndt\b|\bvalidation\b|\bextension\b", title, re.I))


def site_marked_repealed(title: str, meta: str) -> bool:
    return bool(re.search(r"\(\s*repealed|repealed by|\bstatus:\s*repealed", f"{title} {meta}", re.I))


def parse_meta(meta: str) -> dict:
    consolidated = re.search(r"amended up to:\s*([^|]+)", meta, re.I)
    searchable = re.sub(r"amended up to:[^|]*", "", meta, flags=re.I)  # the amending Act is not this law's number
    act = _ACT_NO.search(searchable)
    promulgated = _PROMULGATED.search(meta)
    updated = _UPDATED.search(meta)
    first = meta.split("|")[0].strip()
    category = "" if (not first or _ACT_NO.search(first) or "Promulgation" in first) else first
    status = f"Consolidated, amended up to {consolidated.group(1).strip()}" if consolidated else ""
    for label in ("Under Review", "Published", "Repealed"):
        if label.lower() in searchable.lower():
            status = label
    return {
        "act_number": re.sub(r"\s+", " ", act.group(0)).strip() if act else "",
        "promulgation_date": promulgated.group(1).strip().rstrip(".") if promulgated else "",
        "source_last_updated": updated.group(1).strip() if updated else "",
        "category": category if len(category) < 80 else "",
        "site_status": status,
    }


# Sites whose detail-page URL changes on every visit (Punjab Code encodes the article id with a per-request
# token: the same law appeared under a different URL on each crawl), so the key must come from the listing text.
UNSTABLE_URL_SITES = {"punjab_code"}


def law_identity(listing: Listing) -> str:
    """Stable per-source id for a law: the site's own id where its URLs are stable, else title + Act No. + date."""
    if listing.site in UNSTABLE_URL_SITES:
        meta = parse_meta(listing.meta)
        return "~".join(slug(part) for part in (listing.title, meta["act_number"], meta["promulgation_date"]))
    parsed = urlparse(listing.detail_url)
    if listing.site == "balochistan_code":
        return parse_qs(parsed.query).get("docid", [parsed.query])[0]
    tail = parsed.path.rstrip("/").rsplit("/", 1)[-1]
    return tail or listing.detail_url


def listing_hash(listing: Listing) -> str:
    stable_meta = _VOLATILE.sub("", listing.meta)
    return hashlib.sha1(f"{listing.title}|{stable_meta}".encode("utf-8")).hexdigest()[:16]


def record_from_listing(listing: Listing, source: Source) -> dict:
    meta = parse_meta(listing.meta)
    year = year_of(listing.title) or year_of(meta["promulgation_date"])
    return {
        "law_key": f"{source.source_id}:{law_identity(listing)}",
        "source_id": source.source_id, "jurisdiction": source.jurisdiction, "title": listing.title, "year": year,
        "instrument_type": instrument_type(listing.title), "is_amendment": str(is_amendment(listing.title)).lower(),
        "site_marked_repealed": str(site_marked_repealed(listing.title, listing.meta)).lower(),
        **meta,
        "detail_url": listing.detail_url, "pdf_url": listing.pdf_url, "urdu_pdf_url": listing.urdu_pdf_url,
        "listing_hash": listing_hash(listing),
    }


def to_listing(row: dict, source: Source) -> Listing:
    return Listing(source.adapter, row["jurisdiction"], row["title"], row["detail_url"],
                   pdf_url=row["pdf_url"] if source.adapter in {"sindh_code", "sja_updated_laws"} else "")


# --------------------------------------------------------------------------------------------------
# Inventory persistence
# --------------------------------------------------------------------------------------------------

def load_inventory(path: Path | None = None) -> dict[str, dict]:
    path = path or INVENTORY_CSV  # resolved at call time so the location can be overridden
    if not path.exists():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row["law_key"]: row for row in csv.DictReader(handle)}


def save_inventory(inventory: dict[str, dict]) -> None:
    rows = sorted(inventory.values(), key=lambda r: (r["source_id"], r["title"].lower(), r["law_key"]))
    write_text(INVENTORY_CSV, csv_text(INVENTORY_FIELDS, rows))
    write_text(INVENTORY_JSON, json.dumps([{k: r.get(k, "") for k in INVENTORY_FIELDS} for r in rows],
                                          indent=1, ensure_ascii=False) + "\n")


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else {"baselines": {}, "runs": []}


def save_state(state: dict) -> None:
    write_text(STATE_PATH, json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def save_changes(changes: list[dict], run_date: str) -> Path | None:
    if not changes:
        return None
    CHANGES_DIR.mkdir(parents=True, exist_ok=True)
    path = CHANGES_DIR / f"{run_date}.json"
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    write_text(path, json.dumps(existing + changes, indent=1, ensure_ascii=False) + "\n")
    new_file = not CHANGES_CSV.exists()
    with CHANGES_CSV.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHANGE_FIELDS, lineterminator="\n", extrasaction="ignore")
        if new_file:
            writer.writeheader()
        writer.writerows(changes)
    return path


# --------------------------------------------------------------------------------------------------
# Sync
# --------------------------------------------------------------------------------------------------

@dataclass
class SyncReport:
    run_date: str
    sources: dict = field(default_factory=dict)   # source_id -> stats
    changes: list[dict] = field(default_factory=list)


def _change(run_date: str, kind: str, row: dict, previous: str = "") -> dict:
    return {"run_date": run_date, "change": kind, "law_key": row["law_key"], "source_id": row["source_id"],
            "jurisdiction": row["jurisdiction"], "title": row["title"], "instrument_type": row["instrument_type"],
            "is_amendment": row["is_amendment"], "pdf_url": row.get("pdf_url", ""), "previous": previous,
            "detail_url": row["detail_url"]}


def _needs_pdf_check(row: dict, mode: str, today: str, flagged: set[str]) -> bool:
    if mode == "none" or row.get("removed") == "true":
        return False
    if mode == "all" or row["law_key"] in flagged or row.get("manifest_id"):
        return True
    if not row.get("pdf_url"):
        checked = row.get("pdf_checked_at", "")
        if not checked:
            return True
        try:
            return (date.fromisoformat(today) - date.fromisoformat(checked[:10])).days >= RECHECK_MISSING_PDF_DAYS
        except ValueError:
            return True
    return False


def sync_source(source: Source, inventory: dict[str, dict], previous: dict[str, dict], state: dict, run_date: str,
                resolve: str, fetcher: Fetcher, log=print) -> tuple[dict, list[dict]]:
    """Crawl one source, merge it into the inventory (mutated in place) and return (stats, changes).

    `previous` is this source's rows snapshotted before any thread started, because other sources' threads
    insert into the shared inventory concurrently.
    """
    listings = SITES[source.adapter](fetcher)
    baseline = source.source_id not in state["baselines"]
    previous_active = sum(1 for r in previous.values() if r.get("removed") != "true")
    changes: list[dict] = []
    flagged: set[str] = set()
    seen: set[str] = set()

    for listing in listings:
        record = record_from_listing(listing, source)
        key, occurrence = record["law_key"], 2
        while key in seen:  # the site lists the same law twice (e.g. two uploads): keep both, in listing order
            key, occurrence = f"{record['law_key']}~{occurrence}", occurrence + 1
        record["law_key"] = key
        seen.add(key)
        old = inventory.get(key)
        if old is None:
            record.update(first_seen=run_date, last_seen=run_date, last_changed=run_date, removed="false",
                          pdf_checked_at="", manifest_id="")
            inventory[key] = record
            flagged.add(key)
            if not baseline:
                changes.append(_change(run_date, "new", record))
            continue
        if old.get("removed") == "true":
            changes.append(_change(run_date, "reappeared", record))
            old["removed"] = "false"
        if old["listing_hash"] != record["listing_hash"]:
            changes.append(_change(run_date, "listing_changed", record,
                                   previous=f"{old['title']} | updated {old.get('source_last_updated', '')}".strip()))
            old["last_changed"] = run_date
            flagged.add(key)
        for name in ("title", "year", "instrument_type", "is_amendment", "site_marked_repealed", "act_number",
                     "promulgation_date", "category", "site_status", "source_last_updated", "detail_url",
                     "urdu_pdf_url", "listing_hash"):
            old[name] = record[name]
        if record["pdf_url"]:  # listing links the PDF directly (Sindh Code, SJA)
            if old.get("pdf_url") and old["pdf_url"] != record["pdf_url"]:
                changes.append(_change(run_date, "pdf_changed", record, previous=old["pdf_url"]))
                old["last_changed"] = run_date
            old["pdf_url"] = record["pdf_url"]
        old["last_seen"] = run_date

    partial = previous_active and len(seen) < PARTIAL_CRAWL_RATIO * previous_active
    if not partial:
        for key, row in previous.items():
            if key not in seen and row.get("removed") != "true":
                row["removed"] = "true"
                row["last_changed"] = run_date
                changes.append(_change(run_date, "removed", row))
    else:
        log(f"WARN {source.source_id}: only {len(seen)} of {previous_active} laws listed - partial crawl, "
            "nothing marked removed")

    # Resolve direct PDF links from detail pages where needed.
    resolved = failed = 0
    for key in sorted(k for k in seen if _needs_pdf_check(inventory[k], resolve, run_date, flagged)):
        row = inventory[key]
        if row["pdf_url"] and source.adapter in {"sindh_code", "sja_updated_laws"}:
            row["pdf_checked_at"] = run_date
            continue
        try:
            url = pdf_url(fetcher, to_listing(row, source))
        except Exception as exc:  # noqa: BLE001 - one bad page must not stop the run
            log(f"FAIL pdf {key}: {exc}")
            failed += 1
            continue
        row["pdf_checked_at"] = run_date
        if url and row.get("pdf_url") and url != row["pdf_url"]:
            changes.append(_change(run_date, "pdf_changed", row | {"pdf_url": url}, previous=row["pdf_url"]))
            row["last_changed"] = run_date
        if url:
            row["pdf_url"] = url
            resolved += 1
    stats = {"listed": len(seen), "previous": previous_active, "baseline": baseline, "partial": bool(partial),
             "pdf_resolved": resolved, "pdf_failed": failed,
             "with_pdf": sum(1 for k in seen if inventory[k].get("pdf_url")),
             "changes": len(changes), "anomaly": "" if baseline else anomaly_reason(changes, previous_active)}
    if stats["anomaly"]:
        log(f"WARN {source.source_id}: {stats['anomaly']} - auto-ingest blocked for this source this run")
    if not partial:
        state["baselines"].setdefault(source.source_id, run_date)
    log(f"{source.source_id}: {stats}")
    return stats, changes


def anomaly_reason(changes: list[dict], previous_active: int) -> str:
    """Explain an implausibly large change set (site redesign, unstable ids, mass re-upload), else ''.

    Legislatures pass a handful of laws a week; hundreds of 'new' or 'removed' laws in one run means the
    source changed shape, not the law. Such runs are still recorded, but nothing is auto-ingested from them.
    """
    limit = max(ANOMALY_MIN_CHANGES, int(ANOMALY_SHARE * max(previous_active, 1)))
    counts = {kind: sum(1 for c in changes if c["change"] == kind) for kind in ("new", "removed", "pdf_changed")}
    over = [f"{n} {kind}" for kind, n in counts.items() if n > limit]
    return f"implausible change volume ({', '.join(over)}; limit {limit})" if over else ""


def link_manifest(inventory: dict[str, dict], manifest_rows: list[dict]) -> None:
    """Record which inventory rows are already in the corpus manifest (by PDF URL, then by name + year)."""
    by_url = {r["source_url"]: r["document_id"] for r in manifest_rows if r.get("source_url")}
    by_name = {(r["jurisdiction"], name_key(r["title"]), year_of(r["title"])): r["document_id"]
               for r in manifest_rows if r.get("status") != "placeholder" and not r.get("court")}
    for row in inventory.values():
        doc = by_url.get(row.get("pdf_url", ""))
        if not doc and row["source_id"] != "sja_updated_laws":
            doc = by_name.get((row["jurisdiction"], name_key(row["title"]), row.get("year", "")))
        row["manifest_id"] = doc or ""


def run_sync(sources: list[Source], resolve: str = "auto", cache_dir: Path | None = None, delay: float = 0.5,
             run_date: str | None = None, manifest_rows: list[dict] | None = None, log=print) -> SyncReport:
    run_date = run_date or date.today().isoformat()
    inventory = load_inventory()
    state = load_state()
    if manifest_rows is not None:
        link_manifest(inventory, manifest_rows)  # so tracked laws get their PDF re-checked this run
    report = SyncReport(run_date)
    previous_by_source = {s.source_id: {k: r for k, r in inventory.items() if r["source_id"] == s.source_id}
                          for s in sources}

    def work(source: Source):
        fetcher = Fetcher(cache_dir=cache_dir, delay=delay, log=log)
        try:
            return source.source_id, sync_source(source, inventory, previous_by_source[source.source_id], state,
                                                 run_date, resolve, fetcher, log)
        except Exception as exc:  # noqa: BLE001 - a site outage must not stop the other sources
            log(f"FAIL {source.source_id}: {type(exc).__name__}: {exc}")
            return source.source_id, ({"error": f"{type(exc).__name__}: {exc}"}, [])
        finally:
            fetcher.close()

    # One worker per source: sites are crawled in parallel, each site sequentially and politely.
    with ThreadPoolExecutor(max_workers=max(1, len(sources))) as pool:
        for source_id, (stats, changes) in pool.map(work, sources):
            report.sources[source_id] = stats
            report.changes.extend(changes)
    if manifest_rows is not None:
        link_manifest(inventory, manifest_rows)
    save_inventory(inventory)
    save_changes(report.changes, run_date)
    state["runs"] = (state.get("runs", []) + [{
        "run_at": datetime.now(timezone.utc).isoformat(), "run_date": run_date, "resolve": resolve,
        "sources": report.sources, "changes": len(report.changes)}])[-50:]
    save_state(state)
    return report
