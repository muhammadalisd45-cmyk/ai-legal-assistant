from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.text import sanitize_text

EvidenceLevel = Literal["chunk", "metadata"]
SearchMode = Literal["supabase-hybrid", "local-hybrid", "local-lexical", "local-ingested-chunks", "metadata-only"]


class SearchFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    jurisdiction: str | None = Field(default=None, max_length=60)
    document_type: str | None = Field(default=None, max_length=60)
    document_ids: list[str] | None = Field(default=None, max_length=30)


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: str = Field(min_length=3, max_length=1200)
    limit: int = Field(default=6, ge=1, le=10)
    filters: SearchFilters | None = None
    include_metadata_fallback: bool = True

    @field_validator("query")
    @classmethod
    def _clean(cls, value: str) -> str:
        clean = sanitize_text(value, 1200)
        if len(clean) < 3:
            raise ValueError("query must contain at least 3 visible characters")
        return clean


class Provenance(BaseModel):
    source_url: str
    page_url: str = ""
    file_sha256: str = ""
    fetched_at: str = ""
    source_tier: int = 1


class Relevance(BaseModel):
    term_coverage: float = 0.0
    semantic_similarity: float | None = None
    strong_match: bool = False


class SearchResult(BaseModel):
    # Legacy fields (consumed by the Next.js research UI) — keep names stable.
    document_id: str
    title: str
    document_type: str = ""
    jurisdiction: str = ""
    authority: str = ""
    court: str = ""
    bench: str = ""
    citation: str = ""
    source_name: str = ""
    source_url: str = ""
    section_or_article: str = ""
    status: str = ""
    score: float = 0.0
    evidence_level: EvidenceLevel
    snippet: str = ""
    # New, additive fields
    chunk_id: str | None = None
    section_heading: str = ""
    section_confidence: str = ""
    page_start: int | None = None
    page_end: int | None = None
    page_reference: str = ""
    is_legal_provision: bool = False
    match_reasons: list[str] = Field(default_factory=list)
    relevance: Relevance | None = None
    provenance: Provenance | None = None


class SearchResponse(BaseModel):
    query: str
    mode: SearchMode
    detected_language: str
    results: list[SearchResult]
    evidence_summary: dict[str, int]
    low_confidence: bool = False
    warning: str | None = None
    fallback_reason: str | None = None
    retrieval: dict = Field(default_factory=dict)
    request_id: str = ""
