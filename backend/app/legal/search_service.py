"""Legal search with transparent fallbacks: Supabase hybrid → local hybrid/lexical → metadata-only."""
from __future__ import annotations

import logging
import re

from app.core.config import settings
from app.core.index_state import local_index
from app.core.text import bridge_terms
from app.legal.embeddings import get_embedder
from app.legal.index import tokenize
from app.legal.manifest import load_manifest
from app.legal.retrieval import Retrieved, analyze_query, search_local, search_supabase
from app.schemas.search import Provenance, Relevance, SearchRequest, SearchResponse, SearchResult

logger = logging.getLogger("pjn.search")

METADATA_WARNING = ("No ingested legal text matched this query. Results identify source documents only and do not "
                    "assert exact legal provisions.")
METADATA_SNIPPET = "Metadata match only — exact sections and quotations require an ingested source chunk."
WEAK_WARNING = ("Only weak matches were found. The verified corpus may not cover this topic yet — treat these results as "
                "leads to check, not as the applicable law.")


def _snippet(content: str, terms: list[str], size: int = 520) -> str:
    """Window of the chunk around the first query-term hit (whole chunk start if none)."""
    text = re.sub(r"\s+", " ", content).strip()
    if len(text) <= size:
        return text
    lowered = text.lower()
    first = min((pos for pos in (lowered.find(t) for t in terms if len(t) > 3) if pos >= 0), default=0)
    start = max(0, first - size // 4)
    if start:
        space = text.find(" ", start)
        start = space + 1 if 0 <= space < start + 40 else start
    piece = text[start:start + size].strip()
    return ("…" if start else "") + piece + ("…" if start + size < len(text) else "")


def _page_url(source_url: str, page: int | None) -> str:
    if not source_url or not page:
        return source_url
    return f"{source_url.split('#')[0]}#page={page}"


def to_result(item: Retrieved, terms: list[str]) -> SearchResult:
    c = item.chunk
    page_start, page_end = c.get("page_start"), c.get("page_end")
    if page_start and page_end and page_end != page_start:
        page_ref = f"pp. {page_start}–{page_end}"
    elif page_start:
        page_ref = f"p. {page_start}"
    else:
        page_ref = ""
    return SearchResult(
        document_id=c.get("document_id", ""), title=c.get("title", ""), document_type=c.get("document_type", ""),
        jurisdiction=c.get("jurisdiction", ""), authority=c.get("authority", ""), court=c.get("court") or "",
        bench=c.get("bench") or "", citation=c.get("citation") or "", source_name=c.get("source_name", ""),
        source_url=c.get("source_url", ""), section_or_article=c.get("section_or_article") or "",
        status="ingested", score=item.score, evidence_level="chunk",
        snippet=_snippet(c.get("content") or c.get("snippet", ""), terms),
        chunk_id=c.get("chunk_id"), section_heading=c.get("section_heading") or "",
        section_confidence=c.get("section_confidence") or "", page_start=page_start, page_end=page_end,
        page_reference=page_ref, is_legal_provision=True, match_reasons=item.reasons,
        relevance=Relevance(term_coverage=item.term_coverage, semantic_similarity=item.semantic_score,
                            strong_match=item.strong),
        provenance=Provenance(source_url=c.get("source_url", ""), page_url=_page_url(c.get("source_url", ""), page_start),
                              file_sha256=c.get("file_sha256", ""), fetched_at=c.get("fetched_at", ""),
                              source_tier=int(c.get("source_tier") or 1)),
    )


def metadata_results(query: str, limit: int) -> list[SearchResult]:
    terms = set(tokenize(query + " " + " ".join(bridge_terms(query))))
    if not terms:
        return []
    scored = []
    for row in load_manifest(settings.manifest_path):
        if row.is_placeholder:
            continue  # quarantined: never surfaced, not even as metadata
        haystack = set(tokenize(" ".join([row.title, row.document_type, row.jurisdiction, row.authority, row.source_name])))
        title_terms = set(tokenize(row.title))
        score = 3.0 * len(terms & title_terms) + len(terms & haystack)
        if score > 0:
            scored.append((score, row))
    scored.sort(key=lambda item: (-item[0], item[1].title))
    return [SearchResult(**row.public_metadata() | {"score": float(score)}, evidence_level="metadata",
                         snippet=METADATA_SNIPPET, is_legal_provision=False,
                         provenance=Provenance(source_url=row.source_url, source_tier=row.source_tier))
            for score, row in scored[:limit]]


async def search(request: SearchRequest, request_id: str = "") -> SearchResponse:
    analysis = analyze_query(request.query)
    filters = request.filters.model_dump(exclude_none=True) if request.filters else {}
    embedder = get_embedder()
    retrieval_info: dict = {"bridged_terms": analysis.bridged_terms[:12], "section_refs": analysis.section_refs,
                            "document_hints": analysis.document_hints}
    fallback_reason = None
    items: list[Retrieved] = []
    mode = None

    if settings.retrieval_backend in {"auto", "supabase"} and settings.supabase_secret_key:
        remote = await search_supabase(analysis, request.limit, embedder)
        if remote and remote[0]:
            items, info = remote
            mode = "supabase-hybrid"
            retrieval_info.update(info)
        else:
            fallback_reason = "supabase_unavailable_or_empty"

    if mode is None and settings.retrieval_backend in {"auto", "local"}:
        index, status = local_index()
        retrieval_info["index"] = {"chunks": status.chunks, "documents": status.documents,
                                   "embeddings": status.embeddings, "problem": status.problem or None}
        if index.size:
            items, info = search_local(index, analysis, request.limit, embedder, filters)
            retrieval_info.update(info)
            mode = "local-hybrid" if info.get("semantic") else "local-lexical"
            if not items:
                fallback_reason = "no_matching_chunks"
        else:
            fallback_reason = fallback_reason or "index_empty"

    terms = [t for t in analysis.lexical_terms]
    results = [to_result(item, terms) for item in items]
    warning = None
    low_confidence = bool(results) and not any(r.relevance and r.relevance.strong_match for r in results)
    if low_confidence:
        warning = WEAK_WARNING
    if not results:
        mode = "metadata-only"
        warning = METADATA_WARNING
        if request.include_metadata_fallback:
            results = metadata_results(request.query, request.limit)
    summary = {"chunk": sum(r.evidence_level == "chunk" for r in results),
               "metadata": sum(r.evidence_level == "metadata" for r in results)}
    return SearchResponse(query=request.query, mode=mode, detected_language=analysis.language, results=results,
                          evidence_summary=summary, warning=warning, low_confidence=low_confidence or not results,
                          fallback_reason=fallback_reason if mode == "metadata-only" else None,
                          retrieval=retrieval_info, request_id=request_id)
