"""Supabase (PostgREST) case store.

Every request carries the *end user's* access token, never the service key, so Postgres RLS
(`auth.uid() = user_id`) is the enforcing control; the explicit `user_id` filters are defence in depth.
Requires migrations 001–005.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from app.core.config import settings
from app.core.errors import AppError
from app.core.security import CurrentUser
from app.repositories.base import CaseRepository, ConflictError, new_public_case_id, parse_uuid

CASE_SELECT = ("id,public_case_id,language,category,summary,urgency,status,raw_description,"
               "structured_payload,created_at,updated_at")
DOC_SELECT = ("id,case_id,storage_path,original_file_name,mime_type,status,size_bytes,sha256,page_count,"
              "error,analysis_payload,created_at,updated_at")


class SupabaseCaseRepository(CaseRepository):
    name = "supabase"

    def __init__(self, transport: httpx.AsyncBaseTransport | None = None):
        self._transport = transport

    def _headers(self, user: CurrentUser, prefer: str | None = None) -> dict[str, str]:
        headers = {"apikey": settings.supabase_anon_key, "Authorization": f"Bearer {user.token}",
                   "Content-Type": "application/json"}
        if prefer:
            headers["Prefer"] = prefer
        return headers

    async def _request(self, method: str, path: str, user: CurrentUser, *, params=None, json=None,
                       prefer: str | None = None) -> Any:
        url = f"{settings.supabase_url.rstrip('/')}/rest/v1/{path}"
        try:
            async with httpx.AsyncClient(timeout=10, transport=self._transport) as client:
                response = await client.request(method, url, params=params, json=json, headers=self._headers(user, prefer))
        except httpx.HTTPError as exc:
            raise AppError(503, "Case storage is temporarily unavailable.", "storage_unavailable") from exc
        if response.status_code == 409:
            raise ConflictError("conflict")
        if response.status_code in (401, 403):
            raise AppError(403, "Not allowed to access this case.", "forbidden")
        if response.status_code >= 400:
            raise AppError(503, "Case storage is temporarily unavailable.", "storage_unavailable")
        if not response.content:
            return None
        return response.json()

    async def _owned_case(self, user: CurrentUser, case_ref: str) -> dict[str, Any] | None:
        as_uuid = parse_uuid(case_ref)
        column = "id" if as_uuid else "public_case_id"
        value = as_uuid or case_ref
        rows = await self._request("GET", "cases", user, params={
            "select": CASE_SELECT, column: f"eq.{value}", "user_id": f"eq.{user.id}", "limit": "1"})
        return rows[0] if rows else None

    async def create_case(self, user: CurrentUser, data: dict[str, Any]) -> dict[str, Any]:
        body = {
            "user_id": user.id,
            "public_case_id": data.get("public_case_id") or new_public_case_id(),
            "language": data.get("language", "en"), "category": data.get("category"),
            "summary": data.get("summary"), "urgency": data.get("urgency"),
            "status": data.get("status", "intake"), "raw_description": data["raw_description"],
            "structured_payload": data.get("structured_payload") or {},
        }
        rows = await self._request("POST", f"cases?select={CASE_SELECT}", user, json=body,
                                   prefer="return=representation")
        return rows[0]

    async def list_cases(self, user: CurrentUser, limit: int, offset: int) -> list[dict[str, Any]]:
        return await self._request("GET", "cases", user, params={
            "select": CASE_SELECT, "user_id": f"eq.{user.id}", "order": "updated_at.desc",
            "limit": str(limit), "offset": str(offset)})

    async def get_case(self, user: CurrentUser, case_ref: str) -> dict[str, Any] | None:
        return await self._owned_case(user, case_ref)

    async def update_case(self, user: CurrentUser, case_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        case = await self._owned_case(user, case_id)
        if case is None:
            return None
        if not patch:
            return case
        rows = await self._request("PATCH", f"cases?id=eq.{case['id']}&user_id=eq.{user.id}&select={CASE_SELECT}",
                                   user, json=patch, prefer="return=representation")
        return rows[0] if rows else None

    async def add_message(self, user: CurrentUser, case_id: str, data: dict[str, Any]) -> dict[str, Any]:
        case = await self._owned_case(user, case_id)
        if case is None:
            raise LookupError("case not found")
        rows = await self._request("POST", "case_messages?select=*", user, prefer="return=representation", json={
            "case_id": case["id"], "role": data["role"], "language": data.get("language", "en"),
            "content": data["content"], "metadata": data.get("metadata") or {}})
        return rows[0]

    async def list_messages(self, user: CurrentUser, case_id: str, limit: int) -> list[dict[str, Any]]:
        case = await self._owned_case(user, case_id)
        if case is None:
            raise LookupError("case not found")
        return await self._request("GET", "case_messages", user, params={
            "select": "*", "case_id": f"eq.{case['id']}", "order": "created_at.asc", "limit": str(limit)})

    async def add_document(self, user: CurrentUser, case_id: str, data: dict[str, Any]) -> dict[str, Any]:
        case = await self._owned_case(user, case_id)
        if case is None:
            raise LookupError("case not found")
        body = {key: data.get(key) for key in ("storage_path", "original_file_name", "mime_type", "size_bytes",
                                               "sha256", "page_count", "error")}
        body.update({"case_id": case["id"], "status": data.get("status", "queued"),
                     "analysis_payload": data.get("analysis_payload") or {}})
        if data.get("id"):
            body["id"] = data["id"]
        rows = await self._request("POST", f"case_documents?select={DOC_SELECT}", user, json=body,
                                   prefer="return=representation")
        return rows[0]

    async def update_document(self, user: CurrentUser, document_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        doc_uuid = parse_uuid(document_id)
        if not doc_uuid:
            return None
        rows = await self._request("PATCH", f"case_documents?id=eq.{doc_uuid}&select={DOC_SELECT}", user,
                                   json=patch, prefer="return=representation")
        return rows[0] if rows else None

    async def list_documents(self, user: CurrentUser, case_id: str) -> list[dict[str, Any]]:
        case = await self._owned_case(user, case_id)
        if case is None:
            raise LookupError("case not found")
        return await self._request("GET", "case_documents", user, params={
            "select": DOC_SELECT, "case_id": f"eq.{case['id']}", "order": "created_at.desc"})

    async def get_document(self, user: CurrentUser, case_id: str, document_id: str) -> dict[str, Any] | None:
        case = await self._owned_case(user, case_id)
        doc_uuid = parse_uuid(document_id)
        if case is None or not doc_uuid:
            return None
        rows = await self._request("GET", "case_documents", user, params={
            "select": DOC_SELECT, "id": f"eq.{doc_uuid}", "case_id": f"eq.{quote(case['id'])}", "limit": "1"})
        return rows[0] if rows else None

    async def health(self) -> dict[str, Any]:
        if not settings.supabase_configured:
            return {"store": self.name, "ok": False, "error": "not_configured"}
        try:
            async with httpx.AsyncClient(timeout=5, transport=self._transport) as client:
                response = await client.get(f"{settings.supabase_url.rstrip('/')}/auth/v1/health",
                                            headers={"apikey": settings.supabase_anon_key})
            return {"store": self.name, "ok": response.status_code < 500}
        except httpx.HTTPError:
            return {"store": self.name, "ok": False, "error": "unreachable"}
