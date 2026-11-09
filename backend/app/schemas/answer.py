from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.text import sanitize_text
from app.schemas.search import SearchFilters, SearchResult
from app.schemas.triage import Language, Warning


class AnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=3, max_length=2000)
    language: Language = Language.auto
    limit: int = Field(default=5, ge=1, le=8)
    filters: SearchFilters | None = None

    @field_validator("question")
    @classmethod
    def _clean(cls, value: str) -> str:
        clean = sanitize_text(value, 2000)
        if len(clean) < 3:
            raise ValueError("question must contain at least 3 visible characters")
        return clean


class LLMCitation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence_id: str
    quote: str = ""


class AnswerLLMOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    answer: str
    citations: list[LLMCitation] = Field(default_factory=list)
    uncertainty: str = ""
    insufficient_evidence: bool = False
    needs_lawyer: bool = True


class Citation(BaseModel):
    evidence_id: str
    chunk_id: str | None = None
    document_id: str
    title: str
    section_or_article: str = ""
    page_reference: str = ""
    page_url: str = ""
    source_url: str = ""
    quote: str = ""
    quote_verified: bool = False


class AnswerResponse(BaseModel):
    answer: str
    mode: Literal["live", "extractive_fallback", "no_evidence"]
    grounded: bool
    language: str
    detected_language: str
    citations: list[Citation] = Field(default_factory=list)
    uncertainty: str = ""
    needs_lawyer: bool = True
    unsupported_claims_removed: list[str] = Field(default_factory=list)
    warnings: list[Warning] = Field(default_factory=list)
    evidence: list[SearchResult] = Field(default_factory=list)
    search_mode: str = ""
    fallback_reason: str = ""
    request_id: str = ""
    disclaimer: str = (
        "Legal information only, not legal advice. Check the cited official text and consult a qualified lawyer "
        "or your district legal-aid authority before acting."
    )
