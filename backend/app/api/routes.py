"""Triage (Phase 4) and the legacy stateless PDF-extraction endpoint."""
from __future__ import annotations

from fastapi import APIRouter, Depends, File, Request, UploadFile

from app.core.config import settings
from app.core.errors import AppError
from app.core.rate_limit import rate_limit
from app.documents.processing import extract_pdf_text
from app.documents.validation import UploadRejected, validate_upload
from app.schemas.triage import TriageRequest, TriageResult
from app.services.triage_service import TriageService

router = APIRouter(tags=["legal-triage"])
service = TriageService()


@router.post("/triage", response_model=TriageResult, dependencies=[Depends(rate_limit("triage", ai=True))])
async def triage(payload: TriageRequest, request: Request) -> TriageResult:
    """Structured intake/triage. Never fails because the LLM is down — it degrades to the deterministic fallback."""
    return await service.analyze(payload, request_id=getattr(request.state, "request_id", ""))


async def read_limited(file: UploadFile) -> bytes:
    """Read an upload without ever holding more than MAX_UPLOAD_BYTES + 1 chunk in memory."""
    chunks, total = [], 0
    while True:
        chunk = await file.read(256 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > settings.max_upload_bytes:
            raise AppError(413, f"Files are limited to {settings.max_upload_bytes // (1024 * 1024)} MB.", "file_too_large")
        chunks.append(chunk)
    return b"".join(chunks)


@router.post("/document", dependencies=[Depends(rate_limit("document_extract", ai=True))])
async def upload_document(file: UploadFile = File(...)):
    """Stateless PDF text extraction (nothing is stored). Use /api/v1/cases/{id}/documents to keep files."""
    content = await read_limited(file)
    try:
        validated = validate_upload(file.filename, content, file.content_type)
    except UploadRejected as exc:
        raise AppError(exc.status_code, exc.message, exc.code) from exc
    if validated.mime_type != "application/pdf":
        raise AppError(415, "Only PDF files are supported by this endpoint.", "unsupported_type")
    analysis = extract_pdf_text(content)
    return {
        "filename": validated.safe_name,
        "pages": analysis["pages"],
        "text": analysis["text"],
        "text_truncated": analysis["text_truncated"],
        "needs_ocr": analysis["needs_ocr"],
        "status": "extracted",
    }
