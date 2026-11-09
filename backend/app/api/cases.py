"""Case management (Phase 9). Every route requires authentication and is owner-scoped.

Non-owners receive 404 (not 403) so case IDs cannot be probed.
"""
from __future__ import annotations

import hashlib
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, File, Query, Request, UploadFile
from fastapi.responses import Response

from urllib.parse import quote

from app.core.config import settings
from app.core.errors import AppError
from app.core.rate_limit import client_ip, limiter, rate_limit
from app.core.security import CurrentUser, get_current_user
from app.documents.processing import process_document
from app.documents.storage import get_storage, object_path
from app.documents.validation import UploadRejected, validate_upload
from app.api.routes import read_limited
from app.repositories import get_repository
from app.repositories.base import ConflictError
from app.schemas.cases import CaseCreate, CaseList, CaseOut, CaseUpdate, DocumentOut, MessageCreate, MessageOut
from app.schemas.triage import Language, TriageRequest
from app.services.triage_service import TriageService

router = APIRouter(prefix="/cases", tags=["cases"], dependencies=[Depends(rate_limit("cases"))])
triage_service = TriageService()

LANG_TO_TRIAGE = {"en": Language.english, "roman-ur": Language.roman_urdu, "ur": Language.urdu}


def _not_found() -> AppError:
    return AppError(404, "Case not found.", "case_not_found")


def _doc_out(row: dict) -> DocumentOut:
    analysis = dict(row.get("analysis_payload") or {})
    return DocumentOut(
        id=row["id"], case_id=row["case_id"], original_file_name=row["original_file_name"],
        mime_type=row.get("mime_type"), status=row["status"], size_bytes=row.get("size_bytes"),
        sha256=row.get("sha256"), page_count=row.get("page_count"), error=row.get("error"),
        analysis=analysis, created_at=row["created_at"], updated_at=row.get("updated_at"),
    )


@router.post("", response_model=CaseOut, status_code=201)
async def create_case(payload: CaseCreate, request: Request, user: CurrentUser = Depends(get_current_user)) -> CaseOut:
    data = payload.model_dump(exclude={"run_triage", "description"})
    data["raw_description"] = payload.description
    if payload.run_triage:
        if settings.rate_limit_enabled:  # triage via case creation shares the AI budget
            limiter.check(f"triage:{client_ip(request)}", settings.rate_limit_ai_per_minute)
        result = await triage_service.analyze(
            TriageRequest(message=payload.description, language=LANG_TO_TRIAGE[payload.language]),
            request_id=getattr(request.state, "request_id", ""))
        data["category"] = data.get("category") or result.category
        data["summary"] = data.get("summary") or result.summary
        data["urgency"] = data.get("urgency") or result.urgency.value
        data["status"] = "analysis" if payload.status == "intake" else payload.status
        data["structured_payload"] = {**data.get("structured_payload", {}), "triage": result.model_dump(mode="json")}
    try:
        row = await get_repository().create_case(user, data)
    except ConflictError as exc:
        raise AppError(409, "A case with this public_case_id already exists.", "case_exists") from exc
    return CaseOut(**row)


@router.get("", response_model=CaseList)
async def list_cases(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0, le=10_000),
                     user: CurrentUser = Depends(get_current_user)) -> CaseList:
    rows = await get_repository().list_cases(user, limit, offset)
    return CaseList(items=[CaseOut(**row) for row in rows], limit=limit, offset=offset)


@router.get("/{case_id}", response_model=CaseOut)
async def get_case(case_id: str, user: CurrentUser = Depends(get_current_user)) -> CaseOut:
    row = await get_repository().get_case(user, case_id[:64])
    if row is None:
        raise _not_found()
    return CaseOut(**row)


@router.patch("/{case_id}", response_model=CaseOut)
async def update_case(case_id: str, payload: CaseUpdate, user: CurrentUser = Depends(get_current_user)) -> CaseOut:
    row = await get_repository().update_case(user, case_id[:64], payload.model_dump(exclude_none=True))
    if row is None:
        raise _not_found()
    return CaseOut(**row)


@router.post("/{case_id}/messages", response_model=MessageOut, status_code=201)
async def add_message(case_id: str, payload: MessageCreate, user: CurrentUser = Depends(get_current_user)) -> MessageOut:
    try:
        row = await get_repository().add_message(user, case_id[:64], payload.model_dump())
    except LookupError as exc:
        raise _not_found() from exc
    return MessageOut(**row)


@router.get("/{case_id}/messages", response_model=list[MessageOut])
async def list_messages(case_id: str, limit: int = Query(200, ge=1, le=500),
                        user: CurrentUser = Depends(get_current_user)) -> list[MessageOut]:
    try:
        rows = await get_repository().list_messages(user, case_id[:64], limit)
    except LookupError as exc:
        raise _not_found() from exc
    return [MessageOut(**row) for row in rows]


@router.post("/{case_id}/documents", response_model=DocumentOut, status_code=202,
             dependencies=[Depends(rate_limit("upload", ai=True))])
async def upload_document(case_id: str, background: BackgroundTasks, file: UploadFile = File(...),
                          user: CurrentUser = Depends(get_current_user)) -> DocumentOut:
    repo = get_repository()
    case = await repo.get_case(user, case_id[:64])
    if case is None:
        raise _not_found()
    content = await read_limited(file)
    try:
        validated = validate_upload(file.filename, content, file.content_type)
    except UploadRejected as exc:
        raise AppError(exc.status_code, exc.message, exc.code) from exc

    document_id = str(uuid.uuid4())
    path = object_path(user.id, case["id"], document_id, validated.extension)
    await get_storage().put(user, path, content, validated.mime_type)
    row = await repo.add_document(user, case["id"], {
        "id": document_id, "storage_path": path, "original_file_name": validated.safe_name,
        "mime_type": validated.mime_type, "status": "queued", "size_bytes": validated.size,
        "sha256": hashlib.sha256(content).hexdigest(), "page_count": validated.page_count,
        "analysis_payload": {"validation_notes": validated.notes},
    })
    background.add_task(process_document, repo, user, document_id, content, validated.mime_type)
    return _doc_out(row)


@router.get("/{case_id}/documents", response_model=list[DocumentOut])
async def list_documents(case_id: str, user: CurrentUser = Depends(get_current_user)) -> list[DocumentOut]:
    try:
        rows = await get_repository().list_documents(user, case_id[:64])
    except LookupError as exc:
        raise _not_found() from exc
    out = []
    for row in rows:
        doc = _doc_out(row)
        doc.analysis = {k: v for k, v in doc.analysis.items() if k != "text"}  # list view stays small
        out.append(doc)
    return out


@router.get("/{case_id}/documents/{document_id}", response_model=DocumentOut)
async def get_document(case_id: str, document_id: str, user: CurrentUser = Depends(get_current_user)) -> DocumentOut:
    row = await get_repository().get_document(user, case_id[:64], document_id[:64])
    if row is None:
        raise AppError(404, "Document not found.", "document_not_found")
    return _doc_out(row)


@router.get("/{case_id}/documents/{document_id}/content")
async def download_document(case_id: str, document_id: str, user: CurrentUser = Depends(get_current_user)) -> Response:
    row = await get_repository().get_document(user, case_id[:64], document_id[:64])
    if row is None:
        raise AppError(404, "Document not found.", "document_not_found")
    content = await get_storage().get(user, row["storage_path"])
    name = row["original_file_name"]
    ascii_name = name.encode("ascii", "ignore").decode().replace('"', "").strip() or "document"
    disposition = f"attachment; filename=\"{ascii_name}\"; filename*=UTF-8''{quote(name)}"
    return Response(content=content, media_type=row.get("mime_type") or "application/octet-stream",
                    headers={"Content-Disposition": disposition,
                             "X-Content-Type-Options": "nosniff"})
