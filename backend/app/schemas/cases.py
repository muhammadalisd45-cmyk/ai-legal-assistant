from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.text import sanitize_text

CaseLanguage = Literal["en", "roman-ur", "ur"]
CaseStatus = Literal["intake", "analysis", "ready_for_lawyer", "closed"]
CaseUrgency = Literal["low", "medium", "high", "critical", "unknown"]
DocumentStatus = Literal["uploaded", "queued", "processing", "analyzed", "failed"]

PUBLIC_CASE_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9-]{3,39}$"
MAX_PAYLOAD_BYTES = 256 * 1024


def _bounded_json(value: dict[str, Any]) -> dict[str, Any]:
    if len(json.dumps(value, ensure_ascii=False, default=str).encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise ValueError(f"structured payload must be under {MAX_PAYLOAD_BYTES // 1024} KB")
    return value


class CaseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    description: str = Field(min_length=1, max_length=12000)
    language: CaseLanguage = "en"
    public_case_id: str | None = Field(default=None, pattern=PUBLIC_CASE_ID_PATTERN)
    category: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None, max_length=4000)
    urgency: CaseUrgency | None = None
    status: CaseStatus = "intake"
    structured_payload: dict[str, Any] = Field(default_factory=dict)
    run_triage: bool = False

    @field_validator("description")
    @classmethod
    def _desc(cls, value: str) -> str:
        clean = sanitize_text(value)
        if not clean:
            raise ValueError("description must contain visible text")
        return clean

    @field_validator("structured_payload")
    @classmethod
    def _payload(cls, value: dict[str, Any]) -> dict[str, Any]:
        return _bounded_json(value)


class CaseUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str | None = Field(default=None, max_length=200)
    summary: str | None = Field(default=None, max_length=4000)
    urgency: CaseUrgency | None = None
    status: CaseStatus | None = None
    structured_payload: dict[str, Any] | None = None

    @field_validator("structured_payload")
    @classmethod
    def _payload(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        return None if value is None else _bounded_json(value)


class CaseOut(BaseModel):
    id: str
    public_case_id: str
    language: str
    category: str | None = None
    summary: str | None = None
    urgency: str | None = None
    status: str
    raw_description: str
    structured_payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | str
    updated_at: datetime | str


class CaseList(BaseModel):
    items: list[CaseOut]
    limit: int
    offset: int


class MessageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role: Literal["citizen", "assistant"] = "citizen"
    content: str = Field(min_length=1, max_length=8000)
    language: CaseLanguage = "en"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("content")
    @classmethod
    def _content(cls, value: str) -> str:
        clean = sanitize_text(value)
        if not clean:
            raise ValueError("content must contain visible text")
        return clean

    @field_validator("metadata")
    @classmethod
    def _meta(cls, value: dict[str, Any]) -> dict[str, Any]:
        if len(json.dumps(value, default=str)) > 16 * 1024:
            raise ValueError("metadata must be under 16 KB")
        return value


class MessageOut(BaseModel):
    id: str
    case_id: str
    role: str
    language: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | str


class DocumentOut(BaseModel):
    id: str
    case_id: str
    original_file_name: str
    mime_type: str | None = None
    status: DocumentStatus
    size_bytes: int | None = None
    sha256: str | None = None
    page_count: int | None = None
    error: str | None = None
    analysis: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime | str
    updated_at: datetime | str | None = None
