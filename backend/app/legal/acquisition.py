"""Download and validate official legal PDFs, recording provenance.

TLS is always verified. Some government servers omit intermediate certificates; the OS trust store
(via `truststore`) can complete those chains, so it is used when available. Verification is never disabled.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import ssl
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
from pypdf import PdfReader

from app.legal.manifest import OFFICIAL_HOSTS, ManifestRow, destination

USER_AGENT = "PakistanJusticeNavigator/0.2 (+legal-information research corpus)"
MAX_PDF_BYTES = 60 * 1024 * 1024


def ssl_context() -> ssl.SSLContext | bool:
    try:
        import truststore

        return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    except Exception:  # noqa: BLE001
        return True  # httpx default (certifi) — still verified


@dataclass
class Validation:
    is_pdf: bool = False
    opens: bool = False
    encrypted: bool = False
    pages: int = 0
    text_chars: int = 0
    avg_chars_per_page: float = 0.0
    needs_ocr: bool = False
    title_match: bool = False
    title_terms_found: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.is_pdf and self.opens and not self.encrypted and self.pages > 0 and not self.needs_ocr


_STOP = {"the", "of", "and", "act", "code", "order", "ordinance", "for", "in", "on", "a", "an", "to", "at"}


def _title_terms(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z]{4,}", title)
    return [w.lower() for w in words if w.lower() not in _STOP][:5]


def validate_pdf(content: bytes, title: str) -> Validation:
    v = Validation()
    v.is_pdf = content[:1024].lstrip().startswith(b"%PDF")
    if not v.is_pdf:
        v.problems.append("not_a_pdf")
        return v
    try:
        reader = PdfReader(io.BytesIO(content))
        v.encrypted = bool(reader.is_encrypted)
        if v.encrypted:
            try:
                v.encrypted = not reader.decrypt("")
            except Exception:  # noqa: BLE001
                v.encrypted = True
        v.pages = len(reader.pages)
        v.opens = True
        sample_pages = list(range(min(v.pages, 6)))
        sample_text = ""
        total = 0
        for idx in range(v.pages):
            text = reader.pages[idx].extract_text() or ""
            total += len(text.strip())
            if idx in sample_pages:
                sample_text += " " + text
        v.text_chars = total
        v.avg_chars_per_page = round(total / max(1, v.pages), 1)
        v.needs_ocr = v.avg_chars_per_page < 150
        if v.needs_ocr:
            v.problems.append("little_extractable_text_needs_ocr")
        terms = _title_terms(title)
        lowered = sample_text.lower()
        v.title_terms_found = [t for t in terms if t in lowered]
        v.title_match = bool(terms) and len(v.title_terms_found) >= max(1, (len(terms) + 1) // 2)
        if not v.title_match:
            v.problems.append("title_not_found_in_first_pages")
    except Exception as exc:  # noqa: BLE001
        v.opens = False
        v.problems.append(f"unreadable_pdf:{type(exc).__name__}")
    return v


def load_provenance(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"generated_by": "backend/scripts/acquire_corpus.py", "documents": {}}


def save_provenance(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def acquire(rows: list[ManifestRow], corpus_dir: Path, provenance_path: Path, force: bool = False,
            client: httpx.Client | None = None, log=print) -> dict:
    provenance = load_provenance(provenance_path)
    docs = provenance.setdefault("documents", {})
    summary = {"downloaded": [], "unchanged": [], "failed": {}, "skipped": {}}
    own_client = client is None
    client = client or httpx.Client(timeout=90, follow_redirects=True, verify=ssl_context(),
                                    headers={"User-Agent": USER_AGENT})
    try:
        for row in rows:
            if row.is_placeholder:
                summary["skipped"][row.document_id] = "placeholder"
                continue
            if not row.acquirable:
                summary["skipped"][row.document_id] = f"not_acquirable:{row.status}"
                continue
            path = destination(corpus_dir, row)
            existing = docs.get(row.document_id)
            if path.exists() and existing and not force and sha256(path.read_bytes()) == existing.get("sha256"):
                summary["unchanged"].append(row.document_id)
                continue
            try:
                response = client.get(row.source_url)
                response.raise_for_status()
                final_host = (urlparse(str(response.url)).hostname or "").lower()
                if final_host not in OFFICIAL_HOSTS:
                    raise RuntimeError(f"redirected to non-official host {final_host}")
                content = response.content
                if len(content) > MAX_PDF_BYTES:
                    raise RuntimeError("file exceeds size limit")
                validation = validate_pdf(content, row.title)
                if not (validation.is_pdf and validation.opens and not validation.encrypted and validation.pages):
                    raise RuntimeError("validation failed: " + ",".join(validation.problems))
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)
                docs[row.document_id] = {
                    "document_id": row.document_id,
                    "title": row.title,
                    "source_url": row.source_url,
                    "final_url": str(response.url),
                    "source_name": row.source_name,
                    "file": path.relative_to(corpus_dir).as_posix(),
                    "sha256": sha256(content),
                    "bytes": len(content),
                    "content_type": response.headers.get("content-type", ""),
                    "last_modified": response.headers.get("last-modified", ""),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "validation": {**asdict(validation), "ok": validation.ok},
                }
                summary["downloaded"].append(row.document_id)
                log(f"OK   {row.document_id} {validation.pages}p {len(content):,}B title_match={validation.title_match}")
            except Exception as exc:  # noqa: BLE001
                summary["failed"][row.document_id] = str(exc)[:300]
                log(f"FAIL {row.document_id}: {exc}")
    finally:
        if own_client:
            client.close()
        save_provenance(provenance_path, provenance)
    return summary
