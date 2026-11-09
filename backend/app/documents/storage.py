"""Object storage for case documents. Paths are `<user_id>/<case_id>/<document_id><ext>` — never user-supplied."""
from __future__ import annotations

import asyncio
import uuid
from pathlib import Path

import httpx

from app.core.config import settings
from app.core.errors import AppError
from app.core.security import CurrentUser


def object_path(user_id: str, case_id: str, document_id: str, extension: str) -> str:
    for part in (user_id, case_id, document_id):
        uuid.UUID(part)  # raises for anything that is not a UUID → no traversal possible
    if extension not in {".pdf", ".png", ".jpg", ".jpeg"}:
        raise ValueError("unsupported extension")
    return f"{user_id}/{case_id}/{document_id}{extension}"


class LocalStorage:
    name = "local"

    def __init__(self, root: Path):
        self.root = root.resolve()

    def _resolve(self, path: str) -> Path:
        target = (self.root / path).resolve()
        if self.root not in target.parents:
            raise AppError(400, "Invalid storage path.")
        return target

    async def put(self, user: CurrentUser, path: str, content: bytes, mime_type: str) -> None:
        target = self._resolve(path)

        def write():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)

        await asyncio.to_thread(write)

    async def get(self, user: CurrentUser, path: str) -> bytes:
        target = self._resolve(path)
        if not path.startswith(f"{user.id}/") or not target.exists():
            raise AppError(404, "Document not found.")
        return await asyncio.to_thread(target.read_bytes)


class SupabaseStorage:
    """Uses the user's token so storage RLS policies (migration 005) enforce folder ownership."""

    name = "supabase"

    def __init__(self, transport: httpx.AsyncBaseTransport | None = None):
        self._transport = transport

    def _url(self, path: str) -> str:
        return f"{settings.supabase_url.rstrip('/')}/storage/v1/object/{settings.supabase_storage_bucket}/{path}"

    async def put(self, user: CurrentUser, path: str, content: bytes, mime_type: str) -> None:
        headers = {"apikey": settings.supabase_anon_key, "Authorization": f"Bearer {user.token}",
                   "Content-Type": mime_type, "x-upsert": "false"}
        try:
            async with httpx.AsyncClient(timeout=30, transport=self._transport) as client:
                response = await client.post(self._url(path), headers=headers, content=content)
        except httpx.HTTPError as exc:
            raise AppError(503, "Document storage is temporarily unavailable.") from exc
        if response.status_code >= 400:
            raise AppError(503, "Document storage rejected the upload.")

    async def get(self, user: CurrentUser, path: str) -> bytes:
        headers = {"apikey": settings.supabase_anon_key, "Authorization": f"Bearer {user.token}"}
        try:
            async with httpx.AsyncClient(timeout=30, transport=self._transport) as client:
                response = await client.get(self._url(path).replace("/object/", "/object/authenticated/"), headers=headers)
        except httpx.HTTPError as exc:
            raise AppError(503, "Document storage is temporarily unavailable.") from exc
        if response.status_code in (400, 401, 403, 404):
            raise AppError(404, "Document not found.")
        if response.status_code >= 400:
            raise AppError(503, "Document storage is temporarily unavailable.")
        return response.content


_storage = None


def get_storage():
    global _storage
    if _storage is None:
        _storage = SupabaseStorage() if settings.case_store == "supabase" else LocalStorage(settings.upload_dir)
    return _storage


def set_storage(storage) -> None:
    global _storage
    _storage = storage
