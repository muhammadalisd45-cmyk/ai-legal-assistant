"""Turn inventory changes into corpus manifest updates.

Policy (deliberately conservative — the corpus is legal evidence):
  * ADD a law automatically only if it is NEW since the source's baseline, the source has auto_ingest=true,
    it is a principal instrument (Act / Ordinance / Order / Code / Constitution), it is not an amendment or a
    repealed law, it has a direct PDF on an official host, and the same law (jurisdiction + name + year) is not
    already in the manifest.
  * UPDATE a manifest row when the official PDF behind a law already in the corpus changed (re-download).
  * Amendments are never added on their own; they are linked to the principal law they amend, whose
    consolidated PDF is re-checked on every run anyway.
  * Backfill (explicit, opt-in) adds existing back-catalogue laws under the same eligibility rules.
After download, any PDF that fails validation (scanned / title not found) is quarantined as metadata_only so
it never reaches search results.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from app.legal.catalog import authority, document_type, name_key, slug, year_of
from app.legal.manifest import OFFICIAL_HOSTS
from app.legal.manifest_io import next_id
from app.legal.source_sync import PRINCIPAL_TYPES, Source

SOURCE_NAMES = {"pakistan_code": "Pakistan Code", "punjab_code": "Punjab Code", "sindh_code": "Sindh Code",
                "kp_code": "KP Code", "balochistan_code": "Balochistan Code",
                "sja_updated_laws": "Sindh Judicial Academy"}
SMALL_WORDS = {"of", "and", "the", "in", "for", "on", "to", "by", "at", "with", "or", "a", "an", "as", "from"}
ROMAN = re.compile(r"^[IVXLCDM]+$")


def display_title(title: str) -> str:
    """Title-case ALL-CAPS titles from Punjab/Sindh/KP listings, keeping roman numerals and short words."""
    title = re.sub(r"\.(pdf|docx?)$", "", title.strip(), flags=re.I).strip()
    if not title.isupper():
        return title
    words = title.lower().split()
    out = []
    for index, word in enumerate(words):
        bare = re.sub(r"[^A-Za-z]", "", word).upper()
        if bare and ROMAN.match(bare) and len(bare) <= 5 and bare not in {"DI", "MID", "LID", "CIVIL"}:
            out.append(word.upper())
        elif index and word in SMALL_WORDS:
            out.append(word)
        else:
            out.append(re.sub(r"[a-z]", lambda m: m.group(0).upper(), word, count=1))
    return re.sub(r"\s+,", ",", " ".join(out))


def official(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").lower() in OFFICIAL_HOSTS


def eligibility(row: dict, include_amendments: bool = False) -> str:
    """Return '' if the law may be added to the corpus, else the reason it may not."""
    if row.get("removed") == "true":
        return "removed from source listing"
    if row["instrument_type"] not in PRINCIPAL_TYPES:
        return f"not a principal instrument ({row['instrument_type']})"
    if row["is_amendment"] == "true" and not include_amendments:
        return "amendment (tracked via its principal law)"
    if row["site_marked_repealed"] == "true":
        return "marked repealed on the source"
    if not row.get("pdf_url"):
        return "no direct PDF link found"
    if not official(row["pdf_url"]):
        return f"PDF host not on the official allow-list ({urlparse(row['pdf_url']).hostname})"
    return ""


@dataclass
class IngestPlan:
    add: list[dict] = field(default_factory=list)        # inventory rows
    update: list[tuple[str, str, str]] = field(default_factory=list)  # (document_id, new pdf url, law_key)
    linked_amendments: list[tuple[str, str]] = field(default_factory=list)  # (amendment title, principal doc id)
    skipped: list[tuple[str, str, str]] = field(default_factory=list)  # (law_key, title, reason)
    # link-only corpus rows (metadata_only) that now have an official PDF: (document_id, inventory row)
    upgrade: list[tuple[str, dict]] = field(default_factory=list)
    blocked_sources: dict[str, str] = field(default_factory=dict)  # source_id -> anomaly reason


def _principal_key(title: str) -> str:
    stripped = re.sub(r"\((?:[^)]*\b(?:amendment|amending|validation|extension)\b[^)]*)\)", " ", title, flags=re.I)
    stripped = re.sub(r"\b(amendment|amending)\b", " ", stripped, flags=re.I)
    return re.sub(r"\b(act|ordinance|order|regulation)\b", " ", name_key(stripped)).strip()


MAX_AUTO_ADD = 25  # per run; anything beyond is deferred to the next run and reported


def plan_ingest(changes: list[dict], inventory: dict[str, dict], sources: dict[str, Source],
                manifest_rows: list[dict], include_amendments: bool = False,
                backfill_keys: list[str] | None = None, source_stats: dict | None = None,
                max_add: int = MAX_AUTO_ADD) -> IngestPlan:
    plan = IngestPlan()
    for source_id, stats in (source_stats or {}).items():
        if isinstance(stats, dict) and stats.get("anomaly"):
            plan.blocked_sources[source_id] = stats["anomaly"]
    existing = {(r["jurisdiction"], name_key(r["title"]), year_of(r["title"])): r for r in manifest_rows
                if r.get("status") != "placeholder" and not r.get("court")}
    principals = {}
    for r in manifest_rows:
        if r.get("status") != "placeholder" and not r.get("court"):
            principals.setdefault((r["jurisdiction"], _principal_key(r["title"])), r["document_id"])
    planned: set[str] = set()

    def consider(row: dict) -> None:
        if row["law_key"] in planned:
            return
        reason = eligibility(row, include_amendments)
        identity = (row["jurisdiction"], name_key(row["title"]), row.get("year", ""))
        if not reason and identity in existing:
            match = existing[identity]
            if match.get("status") == "metadata_only" and match["document_id"] not in {d for d, _ in plan.upgrade}:
                plan.upgrade.append((match["document_id"], row))  # link-only row gets its official PDF
                planned.add(row["law_key"])
                return
            reason = "already in the corpus"
        if not reason and len(plan.add) + len(plan.upgrade) >= max_add:
            reason = f"deferred: per-run cap of {max_add} additions reached"
        if reason:
            plan.skipped.append((row["law_key"], row["title"], reason))
            if row["is_amendment"] == "true":
                doc = principals.get((row["jurisdiction"], _principal_key(row["title"])))
                if doc:
                    plan.linked_amendments.append((row["title"], doc))
            return
        plan.add.append(row)
        planned.add(row["law_key"])
        existing[identity] = {"document_id": "", "status": "planned"}

    for change in changes:
        row = inventory.get(change["law_key"])
        if not row:
            continue
        blocked = plan.blocked_sources.get(row["source_id"])
        if blocked and change["change"] in {"new", "pdf_changed", "listing_changed"}:
            plan.skipped.append((row["law_key"], row["title"], f"source anomaly: {blocked}"))
            continue
        if change["change"] == "new" and sources[row["source_id"]].auto_ingest:
            consider(row)
        elif change["change"] in {"pdf_changed", "listing_changed"} and row.get("manifest_id") and row.get("pdf_url"):
            if official(row["pdf_url"]):
                plan.update.append((row["manifest_id"], row["pdf_url"], row["law_key"]))
    for key in backfill_keys or []:
        if key in inventory:
            consider(inventory[key])
    return plan


def apply_plan(plan: IngestPlan, fields: list[str], rows: list[dict], sources: dict[str, Source]) -> tuple[list[str], list[str]]:
    """Mutate manifest rows; return (added ids incl. upgraded link-only rows, updated ids)."""
    by_id = {r["document_id"]: r for r in rows}
    used_files = {r["file_name"] for r in rows if r.get("file_name")}
    added, updated = [], []
    for row in plan.add:
        title = display_title(row["title"])
        jurisdiction = row["jurisdiction"]
        file_name = slug(title) + ".pdf"
        if file_name in used_files:
            file_name = f"{row['source_id']}_{file_name}"
        used_files.add(file_name)
        doc = {key: "" for key in fields}
        doc.update({
            "document_id": next_id(rows, jurisdiction), "title": title,
            "document_type": "Federal Order" if title.startswith("Qanun-e-Shahadat") else document_type(jurisdiction, title),
            "jurisdiction": jurisdiction, "authority": authority(jurisdiction, title), "language": "English",
            "source_name": SOURCE_NAMES.get(row["source_id"], row["source_id"]), "source_url": row["pdf_url"],
            "file_name": file_name, "status": "source_url_verified", "priority": "Medium",
            "source_tier": str(sources[row["source_id"]].source_tier),
        })
        rows.append(doc)
        by_id[doc["document_id"]] = doc
        row["manifest_id"] = doc["document_id"]
        added.append(doc["document_id"])
    for document_id, row in plan.upgrade:
        doc = by_id.get(document_id)
        if not doc:
            continue
        file_name = doc.get("file_name") or slug(doc["title"]) + ".pdf"
        if file_name in used_files and not doc.get("file_name"):
            file_name = f"{row['source_id']}_{file_name}"
        used_files.add(file_name)
        doc.update({"source_url": row["pdf_url"], "status": "source_url_verified", "file_name": file_name,
                    "source_name": SOURCE_NAMES.get(row["source_id"], row["source_id"]),
                    "source_tier": str(sources[row["source_id"]].source_tier)})
        row["manifest_id"] = document_id
        added.append(document_id)
    for document_id, url, _key in plan.update:
        doc = by_id.get(document_id)
        if doc and doc["source_url"] != url:
            doc["source_url"] = url
            doc["status"] = "source_url_verified"
            updated.append(document_id)
    return added, updated


def quarantine(rows: list[dict], provenance_docs: dict, document_ids: list[str]) -> list[tuple[str, str]]:
    """Downgrade rows whose downloaded PDF failed validation; return (id, reason) pairs."""
    by_id = {r["document_id"]: r for r in rows}
    out = []
    for document_id in document_ids:
        prov = provenance_docs.get(document_id)
        doc = by_id.get(document_id)
        if not doc:
            continue
        if not prov:
            reason = "download failed"
        else:
            validation = prov.get("validation", {})
            reason = ("needs OCR (scanned)" if validation.get("needs_ocr") else
                      "title not found in PDF" if not validation.get("title_match") else "")
        if reason:
            doc["status"] = "metadata_only"
            out.append((document_id, reason))
    return out
