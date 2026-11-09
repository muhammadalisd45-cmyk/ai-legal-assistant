"""Upload validation and malware-screening strategy.

Layers (all must pass):
1. Size: non-empty and <= MAX_UPLOAD_BYTES (also enforced while streaming the request body).
2. Type: extension allow-list AND magic-byte signature must agree; the client-declared MIME type is not trusted.
3. PDF structure: must parse, must not be encrypted, page count bounded, and must not contain active
   content (JavaScript, launch actions, embedded files, XFA/rich media). Checked both in the raw bytes and
   in the parsed document catalog.
4. Antivirus: when CLAMAV_HOST is configured, the bytes are streamed to clamd (INSTREAM). If the scanner is
   configured but unreachable the upload fails closed.
Files are stored under random names; the original name is only kept as sanitised metadata.
"""
from __future__ import annotations

import io
import re
import socket
import struct
import unicodedata
from dataclasses import dataclass, field
from pathlib import PurePosixPath, PureWindowsPath

from pypdf import PdfReader

from app.core.config import settings

ALLOWED = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}
SIGNATURES = {
    "application/pdf": (b"%PDF-",),
    "image/png": (b"\x89PNG\r\n\x1a\n",),
    "image/jpeg": (b"\xff\xd8\xff",),
}
ACTIVE_CONTENT_MARKERS = (b"/JavaScript", b"/JS ", b"/JS(", b"/JS<", b"/Launch", b"/EmbeddedFile",
                          b"/RichMedia", b"/XFA", b"/SubmitForm", b"/ImportData")


class UploadRejected(Exception):
    def __init__(self, code: str, message: str, status_code: int = 422):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


@dataclass
class ValidatedUpload:
    safe_name: str
    extension: str
    mime_type: str
    size: int
    page_count: int | None = None
    notes: list[str] = field(default_factory=list)


def sanitize_filename(name: str | None) -> str:
    raw = name or "document"
    base = PureWindowsPath(PurePosixPath(raw).name).name  # strip any directory component (/ or \)
    base = unicodedata.normalize("NFC", base)
    base = re.sub(r"[\x00-\x1f\x7f<>:\"/\\|?*]", "_", base).strip(" .")
    return (base or "document")[:150]


def _sniff(content: bytes) -> str | None:
    head = content[:16]
    for mime, sigs in SIGNATURES.items():
        if any(head.startswith(sig) for sig in sigs):
            return mime
    # Tolerate a short preamble before %PDF (allowed by the spec, max 1024 bytes).
    if b"%PDF-" in content[:1024]:
        return "application/pdf"
    return None


def _pdf_checks(content: bytes) -> tuple[int, list[str]]:
    for marker in ACTIVE_CONTENT_MARKERS:
        if marker in content:
            raise UploadRejected("pdf_active_content", "PDFs containing scripts, embedded files or active content are not accepted.")
    try:
        reader = PdfReader(io.BytesIO(content), strict=False)
    except Exception as exc:  # noqa: BLE001
        raise UploadRejected("pdf_unreadable", "The PDF could not be read. It may be corrupted.") from exc
    if reader.is_encrypted:
        raise UploadRejected("pdf_encrypted", "Password-protected PDFs are not accepted. Upload an unlocked copy.")
    try:
        pages = len(reader.pages)
        root = reader.trailer.get("/Root", {})
        root = root.get_object() if hasattr(root, "get_object") else root
        names = root.get("/Names", {}) if hasattr(root, "get") else {}
        names = names.get_object() if hasattr(names, "get_object") else names
    except Exception as exc:  # noqa: BLE001
        raise UploadRejected("pdf_unreadable", "The PDF structure is invalid.") from exc
    if hasattr(names, "keys") and any(key in names for key in ("/JavaScript", "/EmbeddedFiles")):
        raise UploadRejected("pdf_active_content", "PDFs containing scripts, embedded files or active content are not accepted.")
    if hasattr(root, "keys") and ("/AA" in root or "/AcroForm" in root and "/XFA" in str(root.get("/AcroForm"))):
        raise UploadRejected("pdf_active_content", "PDFs containing automatic actions or XFA forms are not accepted.")
    if pages == 0:
        raise UploadRejected("pdf_empty", "The PDF has no pages.")
    if pages > settings.max_pdf_pages:
        raise UploadRejected("pdf_too_many_pages", f"PDFs are limited to {settings.max_pdf_pages} pages.")
    return pages, []


def clamav_scan(content: bytes) -> None:
    if not settings.clamav_host:
        return
    try:
        with socket.create_connection((settings.clamav_host, settings.clamav_port), timeout=15) as sock:
            sock.sendall(b"zINSTREAM\0")
            for start in range(0, len(content), 64 * 1024):
                chunk = content[start:start + 64 * 1024]
                sock.sendall(struct.pack("!L", len(chunk)) + chunk)
            sock.sendall(struct.pack("!L", 0))
            reply = sock.recv(4096).decode("utf-8", "replace")
    except OSError as exc:
        raise UploadRejected("scan_unavailable", "The malware scanner is unavailable. Please retry later.", 503) from exc
    if "FOUND" in reply:
        raise UploadRejected("malware_detected", "The file was rejected by the malware scanner.")
    if "OK" not in reply:
        raise UploadRejected("scan_failed", "The file could not be scanned. Please retry later.", 503)


def validate_upload(filename: str | None, content: bytes, declared_mime: str | None = None) -> ValidatedUpload:
    if not content:
        raise UploadRejected("empty_file", "The uploaded file is empty.")
    if len(content) > settings.max_upload_bytes:
        raise UploadRejected("file_too_large", f"Files are limited to {settings.max_upload_bytes // (1024 * 1024)} MB.", 413)
    safe = sanitize_filename(filename)
    ext = PurePosixPath(safe.lower()).suffix
    if ext not in ALLOWED:
        raise UploadRejected("unsupported_type", "Only PDF, PNG and JPEG files are accepted.", 415)
    expected = ALLOWED[ext]
    sniffed = _sniff(content)
    if sniffed != expected:
        raise UploadRejected("type_mismatch", "The file content does not match its extension.", 415)
    notes = []
    if declared_mime and declared_mime.split(";")[0].strip().lower() not in {expected, "application/octet-stream"}:
        notes.append("declared_mime_ignored")
    pages = None
    if expected == "application/pdf":
        pages, extra = _pdf_checks(content)
        notes.extend(extra)
    clamav_scan(content)
    if not settings.clamav_host:
        notes.append("antivirus_not_configured")
    return ValidatedUpload(safe_name=safe, extension=ext, mime_type=expected, size=len(content), page_count=pages, notes=notes)
