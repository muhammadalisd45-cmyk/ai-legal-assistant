"""Corpus manifest (frontend/data/member4_manifest.csv is the single source of truth)."""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

OFFICIAL_HOSTS = frozenset({
    "pakistancode.gov.pk", "www.pakistancode.gov.pk",
    "sindhlaws.gov.pk", "www.sindhlaws.gov.pk",
    "caselaw.shc.gov.pk",
    "supremecourt.gov.pk", "www.supremecourt.gov.pk",
    "lhc.gov.pk", "www.lhc.gov.pk", "data.lhc.gov.pk",
    "ihc.gov.pk", "www.ihc.gov.pk", "mis.ihc.gov.pk",
    "punjabcode.punjab.gov.pk", "www.punjabcode.punjab.gov.pk",
    "kpcode.kp.gov.pk", "www.kpcode.kp.gov.pk",
    "balochistancode.gob.pk", "www.balochistancode.gob.pk",
    "na.gov.pk", "www.na.gov.pk", "senate.gov.pk", "www.senate.gov.pk",
})

# Statuses that may never be treated as legal evidence.
NON_EVIDENCE_STATUSES = frozenset({"placeholder", "metadata_only"})


@dataclass
class ManifestRow:
    document_id: str
    title: str
    document_type: str
    jurisdiction: str
    court: str
    authority: str
    citation: str
    source_name: str
    source_url: str
    file_name: str
    status: str
    priority: str
    source_tier: int
    bench: str = ""
    section_or_article: str = ""
    language: str = "English"
    extra: dict = field(default_factory=dict)

    @property
    def host(self) -> str:
        return (urlparse(self.source_url).hostname or "").lower()

    @property
    def is_official_host(self) -> bool:
        return self.host in OFFICIAL_HOSTS and urlparse(self.source_url).scheme == "https"

    @property
    def is_placeholder(self) -> bool:
        return self.status == "placeholder"

    @property
    def acquirable(self) -> bool:
        """A direct, official PDF whose URL has been verified by the corpus team."""
        return (self.status in {"source_url_verified", "verified", "ingested"} and self.is_official_host
                and self.source_url.lower().split("?")[0].endswith(".pdf") and bool(self.file_name))

    def public_metadata(self) -> dict:
        return {
            "document_id": self.document_id, "title": self.title, "document_type": self.document_type,
            "jurisdiction": self.jurisdiction, "authority": self.authority, "court": self.court,
            "bench": self.bench, "citation": self.citation, "source_name": self.source_name,
            "source_url": self.source_url, "section_or_article": self.section_or_article,
            "status": self.status, "priority": self.priority, "source_tier": self.source_tier,
        }


def load_manifest(path: Path) -> list[ManifestRow]:
    if not path.exists():
        return []
    rows: list[ManifestRow] = []
    with path.open(encoding="utf-8-sig") as handle:
        for raw in csv.DictReader(handle):
            raw = {k: (v or "").strip() for k, v in raw.items() if k}
            try:
                tier = int(raw.get("source_tier") or 1)
            except ValueError:
                tier = 1
            rows.append(ManifestRow(
                document_id=raw.get("document_id", ""), title=raw.get("title", ""),
                document_type=raw.get("document_type", ""), jurisdiction=raw.get("jurisdiction", ""),
                court=raw.get("court", ""), authority=raw.get("authority", ""), citation=raw.get("citation", ""),
                source_name=raw.get("source_name", ""), source_url=raw.get("source_url", ""),
                file_name=raw.get("file_name", ""), status=raw.get("status", ""), priority=raw.get("priority", ""),
                source_tier=tier, bench=raw.get("bench", ""), section_or_article=raw.get("section_or_article", ""),
                language=raw.get("language", "English") or "English",
                extra={k: v for k, v in raw.items() if k in {"case_number", "case_year", "date", "parties"} and v},
            ))
    return rows


def destination(corpus_dir: Path, row: ManifestRow) -> Path:
    """Same folder routing as frontend/scripts/fetch_initial_official_docs.py."""
    document_id = row.document_id.upper()
    document_type = row.document_type.lower()
    court = row.court.lower()
    jurisdiction = row.jurisdiction.lower()
    if document_id == "PK-001" or "constitution" in document_type:
        folder = corpus_dir / "constitution"
    elif document_id.startswith("SD-") or ("sindh" in jurisdiction and not court):
        folder = corpus_dir / "sindh_laws"
    elif "supreme court" in court:
        folder = corpus_dir / "supreme_court"
    elif "sindh high court" in court:
        folder = corpus_dir / "high_courts" / "sindh"
    elif "lahore high court" in court:
        folder = corpus_dir / "high_courts" / "lahore"
    elif "islamabad high court" in court:
        folder = corpus_dir / "high_courts" / "islamabad"
    else:
        folder = corpus_dir / "federal_laws"
    safe_name = Path(row.file_name).name  # never allow path traversal from manifest data
    return folder / safe_name
