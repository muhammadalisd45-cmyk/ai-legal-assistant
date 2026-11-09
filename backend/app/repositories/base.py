"""Case persistence interface. Every method is scoped to the calling user: implementations must never
return or mutate rows owned by someone else (the SQLite store filters by user_id; the Supabase store
forwards the user's JWT so Postgres RLS enforces the same rule)."""
from __future__ import annotations

import secrets
import uuid
from abc import ABC, abstractmethod
from typing import Any

from app.core.security import CurrentUser

_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def new_public_case_id() -> str:
    return "PJN-" + "".join(secrets.choice(_ALPHABET) for _ in range(8))


def parse_uuid(value: str) -> str | None:
    try:
        return str(uuid.UUID(value))
    except (ValueError, AttributeError, TypeError):
        return None


class ConflictError(Exception):
    pass


class CaseRepository(ABC):
    name: str = "base"

    @abstractmethod
    async def create_case(self, user: CurrentUser, data: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    async def list_cases(self, user: CurrentUser, limit: int, offset: int) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def get_case(self, user: CurrentUser, case_ref: str) -> dict[str, Any] | None:
        """`case_ref` is the UUID primary key or the public case ID."""

    @abstractmethod
    async def update_case(self, user: CurrentUser, case_id: str, patch: dict[str, Any]) -> dict[str, Any] | None: ...

    @abstractmethod
    async def add_message(self, user: CurrentUser, case_id: str, data: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    async def list_messages(self, user: CurrentUser, case_id: str, limit: int) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def add_document(self, user: CurrentUser, case_id: str, data: dict[str, Any]) -> dict[str, Any]: ...

    @abstractmethod
    async def update_document(self, user: CurrentUser, document_id: str, patch: dict[str, Any]) -> dict[str, Any] | None: ...

    @abstractmethod
    async def list_documents(self, user: CurrentUser, case_id: str) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def get_document(self, user: CurrentUser, case_id: str, document_id: str) -> dict[str, Any] | None: ...

    async def health(self) -> dict[str, Any]:
        return {"store": self.name, "ok": True}
