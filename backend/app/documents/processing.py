"""Background processing of uploaded case documents: queued → processing → analyzed | failed."""
from __future__ import annotations

import asyncio
import io
import logging

from pypdf import PdfReader

from app.core.security import CurrentUser
from app.core.text import detect_language
from app.legal.extraction import clean_page_text
from app.repositories.base import CaseRepository

logger = logging.getLogger("pjn.documents")

MAX_STORED_TEXT = 60_000


def extract_pdf_text(content: bytes) -> dict:
    reader = PdfReader(io.BytesIO(content), strict=False)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = clean_page_text(page.extract_text() or "")
        pages.append({"page": number, "chars": len(text), "text": text})
    full = "\n\n".join(f"[page {p['page']}]\n{p['text']}" for p in pages if p["text"])
    total = sum(p["chars"] for p in pages)
    return {
        "kind": "pdf",
        "pages": len(pages),
        "extracted_chars": total,
        "needs_ocr": total / max(1, len(pages)) < 80,
        "detected_language": detect_language(full[:4000]) if full else None,
        "text": full[:MAX_STORED_TEXT],
        "text_truncated": len(full) > MAX_STORED_TEXT,
        "empty_pages": [p["page"] for p in pages if not p["chars"]][:50],
    }


async def process_document(repo: CaseRepository, user: CurrentUser, document_id: str, content: bytes,
                           mime_type: str, timeout_seconds: float = 60.0) -> None:
    try:
        await repo.update_document(user, document_id, {"status": "processing"})
        if mime_type == "application/pdf":
            analysis = await asyncio.wait_for(asyncio.to_thread(extract_pdf_text, content), timeout=timeout_seconds)
            if analysis["needs_ocr"]:
                analysis["note"] = "Little or no selectable text was found; the PDF may be scanned and needs OCR."
        else:
            analysis = {"kind": "image", "note": "Image stored securely. Text recognition (OCR) is not enabled."}
        await repo.update_document(user, document_id, {"status": "analyzed", "analysis_payload": analysis,
                                                       "page_count": analysis.get("pages")})
    except asyncio.TimeoutError:
        logger.warning("document_processing_timeout", extra={"document_id": document_id})
        await _fail(repo, user, document_id, "Processing timed out.")
    except Exception as exc:  # noqa: BLE001
        logger.warning("document_processing_failed", extra={"document_id": document_id, "exc_type": type(exc).__name__})
        await _fail(repo, user, document_id, "The document could not be processed.")


async def _fail(repo: CaseRepository, user: CurrentUser, document_id: str, message: str) -> None:
    try:
        await repo.update_document(user, document_id, {"status": "failed", "error": message})
    except Exception:  # noqa: BLE001
        logger.exception("document_status_update_failed", extra={"document_id": document_id})
