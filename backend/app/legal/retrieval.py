"""Hybrid legal retrieval: BM25 lexical + 384-d semantic vectors, fused with Reciprocal Rank Fusion.

Multilingual handling: Urdu / Roman-Urdu queries are bridged to English legal vocabulary for the lexical
leg (the corpus is English), while the multilingual embedding model handles the semantic leg.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

import httpx
import numpy as np

from app.core.config import settings
from app.core.text import bridge_terms, detect_language, normalize_roman_urdu, sanitize_text
from app.legal.embeddings import Embedder
from app.legal.index import LocalIndex, tokenize

logger = logging.getLogger("pjn.retrieval")

RRF_K = 60
_SECTION_REF = re.compile(
    r"(?P<kind>section|sec\.?|s\.|dafa|dafah|دفعہ|article|art\.?|aarticle|شق|آرٹیکل|order|rule)\s*(?P<num>\d{1,4}\s?[a-z]{0,2})\b",
    re.IGNORECASE,
)
_SECTION_REF_TRAILING = re.compile(r"(?P<num>\d{1,4}[a-z]{0,2})\s*(?P<kind>dafa|دفعہ)", re.IGNORECASE)

DOCUMENT_ALIASES = {
    "PK-001": ["constitution", "aain", "aaeen", "آئین", "dastoor", "fundamental rights", "bunyadi huqooq"],
    "PK-002": ["ppc", "penal code", "pakistan penal code", "tazeerat", "تعزیرات"],
    "PK-003": ["crpc", "cr.p.c", "criminal procedure", "zabta faujdari", "ضابطہ فوجداری"],
    "PK-004": ["cpc", "c.p.c", "civil procedure", "zabta diwani", "ضابطہ دیوانی"],
    "PK-007": ["specific relief"],
    "PK-008": ["limitation", "miyad", "معیاد"],
    "PK-010": ["registration act", "registry"],
    "PK-015": ["money laundering", "aml"],
    "PK-016": ["terrorism", "ata", "دہشت گردی"],
    "PK-017": ["workplace harassment", "harassment of women", "ہراسانی"],
    "PK-018": ["electronic transactions", "e-signature", "electronic signature"],
    "PK-019": ["juvenile", "child offender", "nabaligh", "نابالغ"],
    "PK-020": ["legal aid", "qanooni madad", "قانونی امداد", "free lawyer", "muft wakeel"],
}


# Curated terminology bridge for colloquial terms that never appear in the statute text itself
# (e.g. the CrPC says "information relating to the commission of a cognizable offence", never "FIR").
# Hints only re-rank; the evidence returned is always the retrieved official text.
CONCEPT_PROVISIONS: dict[str, list[tuple[str, str]]] = {
    "fir": [("PK-003", "Section 154")],
    "ایف آئی آر": [("PK-003", "Section 154")],
    "first information report": [("PK-003", "Section 154")],
    "stay order": [("PK-004", "Order XXXIX, Rule 1"), ("PK-004", "Order XXXIX, Rule 2")],
    "writ": [("PK-001", "Article 199")],
    "حکم امتناعی": [("PK-004", "Order XXXIX, Rule 1")],
}
# Theft / robbery in everyday words (incl. common misspellings) → the defining and penal provisions, plus how the
# incident is reported to the police (CrPC s.154). Labels verified against the built index.
_THEFT = [("PK-002", "Section 378"), ("PK-002", "Section 379"), ("PK-003", "Section 154")]
_ROBBERY = [("PK-002", "Section 390"), ("PK-002", "Section 392"), ("PK-003", "Section 154")]
for _key in ("theft", "thief", "theif", "thieves", "stolen", "stole", "steal", "pickpocket", "chori", "churaya",
             "چوری", "چور"):
    CONCEPT_PROVISIONS[_key] = _THEFT
for _key in ("robbery", "robbed", "rob", "robber", "snatched", "snatching", "mugged", "cheena", "chheena",
             "چھین"):
    CONCEPT_PROVISIONS[_key] = _ROBBERY


@dataclass
class QueryAnalysis:
    original: str
    language: str
    lexical_terms: list[str]
    semantic_text: str
    bridged_terms: list[str]
    section_refs: list[tuple[str, str]]
    document_hints: list[str]
    concept_hints: list[tuple[str, str]] = field(default_factory=list)


@dataclass
class Retrieved:
    chunk: dict[str, Any]
    score: float
    lexical_rank: int | None = None
    semantic_rank: int | None = None
    lexical_score: float = 0.0
    semantic_score: float | None = None
    reasons: list[str] = field(default_factory=list)
    term_coverage: float = 0.0
    strong: bool = False


# Calibrated on the real corpus (backend/docs/RETRIEVAL_EVAL.md): relevant top hits score >= 0.48 cosine with the
# multilingual model, off-corpus questions (tax, passports, insurance, family law) peak at ~0.43.
SEMANTIC_STRONG = 0.48
COVERAGE_STRONG = 0.6


def assess(item: Retrieved, analysis: QueryAnalysis, semantic_strong: float = SEMANTIC_STRONG) -> Retrieved:
    """Absolute relevance (RRF scores are rank-based): term coverage + semantic similarity + exact references."""
    terms = set(analysis.lexical_terms)
    c = item.chunk
    tokens = set(tokenize(" ".join(filter(None, [c.get("title", ""), c.get("section_or_article", ""),
                                                 c.get("section_heading", ""), c.get("content") or c.get("snippet", "")]))))
    item.term_coverage = round(len(terms & tokens) / len(terms), 3) if terms else 0.0
    exact = bool({"section_reference", "terminology_hint"} & set(item.reasons))
    if item.semantic_score is not None:
        item.strong = exact or item.semantic_score >= semantic_strong
    else:
        item.strong = exact or (item.term_coverage >= COVERAGE_STRONG and len(terms & tokens) >= min(2, len(terms)))
    return item


def analyze_query(query: str) -> QueryAnalysis:
    clean = sanitize_text(query, 1200)
    language = detect_language(clean)
    bridged = bridge_terms(clean)
    normalized = normalize_roman_urdu(clean) if language == "roman_urdu" else clean
    terms = tokenize(normalized) + tokenize(" ".join(bridged))
    refs: list[tuple[str, str]] = []
    for match in list(_SECTION_REF.finditer(clean)) + list(_SECTION_REF_TRAILING.finditer(clean)):
        kind = match.group("kind").lower().rstrip(".")
        kind = {"sec": "section", "s": "section", "dafa": "section", "dafah": "section", "دفعہ": "section",
                "art": "article", "aarticle": "article", "شق": "article", "آرٹیکل": "article"}.get(kind, kind)
        refs.append((kind, match.group("num").replace(" ", "").lower()))
    lowered = clean.lower()
    hints = [doc for doc, aliases in DOCUMENT_ALIASES.items() if any(alias in lowered for alias in aliases)]
    semantic = clean if not bridged else f"{clean}\n{' '.join(bridged)}"
    concepts: list[tuple[str, str]] = []
    for key, targets in CONCEPT_PROVISIONS.items():
        if (re.fullmatch(r"[a-z ]+", key) and re.search(rf"\b{re.escape(key)}\b", lowered)) or (
                not re.fullmatch(r"[a-z ]+", key) and key in clean):
            concepts.extend(targets)
    return QueryAnalysis(clean, language, terms, semantic, bridged, list(dict.fromkeys(refs)), hints,
                         list(dict.fromkeys(concepts)))


def _passes(chunk: dict, filters: dict[str, Any]) -> bool:
    if not filters:
        return True
    if filters.get("jurisdiction") and chunk.get("jurisdiction", "").lower() != filters["jurisdiction"].lower():
        return False
    if filters.get("document_type") and filters["document_type"].lower() not in chunk.get("document_type", "").lower():
        return False
    if filters.get("document_ids") and chunk.get("document_id") not in filters["document_ids"]:
        return False
    return True


def rrf_fuse(rankings: list[list[int]], weights: list[float]) -> dict[int, float]:
    fused: dict[int, float] = {}
    for ranking, weight in zip(rankings, weights):
        for rank, idx in enumerate(ranking):
            fused[idx] = fused.get(idx, 0.0) + weight / (RRF_K + rank + 1)
    return fused


def search_local(index: LocalIndex, analysis: QueryAnalysis, limit: int, embedder: Embedder | None,
                 filters: dict[str, Any] | None = None, pool: int = 50) -> tuple[list[Retrieved], dict]:
    filters = filters or {}
    info = {"lexical": True, "semantic": False}
    if not index.size:
        return [], info
    semantic_strong = getattr(embedder, "strong_threshold", SEMANTIC_STRONG)
    allowed = np.array([_passes(c, filters) for c in index.chunks], dtype=bool)

    lexical = index.bm25(analysis.lexical_terms)
    lexical[~allowed] = 0
    lex_order = [int(i) for i in np.argsort(-lexical)[:pool] if lexical[i] > 0]

    sem_order: list[int] = []
    semantic = None
    if embedder is not None and index.embeddings is not None and index.embedding_model == embedder.name:
        try:
            qvec = embedder.embed([analysis.semantic_text])[0]
            semantic = index.embeddings @ qvec
            semantic[~allowed] = -1
            # Without any lexical evidence, require a meaningful similarity to avoid returning noise.
            floor = 0.25 if lex_order else 0.45
            sem_order = [int(i) for i in np.argsort(-semantic)[:pool] if semantic[i] >= floor]
            info["semantic"] = True
        except Exception:  # noqa: BLE001
            logger.warning("semantic_leg_failed")

    # Exact section/article references and document hints are strong signals.
    boosted: list[int] = []
    for kind, num in analysis.section_refs:
        for i in index.by_section.get((kind, num), []):
            if allowed[i] and (not analysis.document_hints or index.chunks[i]["document_id"] in analysis.document_hints):
                boosted.append(i)
    concept: list[int] = []
    for document_id, label in analysis.concept_hints:
        for i in index.by_label.get((document_id, label.lower()), []):
            if allowed[i]:
                concept.append(i)
    fused = rrf_fuse([lex_order, sem_order, boosted, concept], [1.0, 0.9 if lex_order else 1.0, 2.5, 1.5])
    if analysis.document_hints:
        for i in list(fused):
            if index.chunks[i]["document_id"] in analysis.document_hints:
                fused[i] *= 1.35

    lex_rank = {idx: r for r, idx in enumerate(lex_order)}
    sem_rank = {idx: r for r, idx in enumerate(sem_order)}
    ordered = sorted(fused.items(), key=lambda item: item[1], reverse=True)
    results: list[Retrieved] = []
    per_doc: dict[str, int] = {}
    for idx, score in ordered:
        chunk = index.chunks[idx]
        # Diversity: at most 3 chunks per document unless the user asked for a specific provision.
        if not analysis.section_refs and per_doc.get(chunk["document_id"], 0) >= 3:
            continue
        per_doc[chunk["document_id"]] = per_doc.get(chunk["document_id"], 0) + 1
        reasons = []
        if idx in lex_rank:
            reasons.append("lexical")
        if idx in sem_rank:
            reasons.append("semantic")
        if idx in boosted:
            reasons.append("section_reference")
        if idx in concept:
            reasons.append("terminology_hint")
        results.append(assess(Retrieved(
            chunk=chunk, score=round(score, 6), lexical_rank=lex_rank.get(idx), semantic_rank=sem_rank.get(idx),
            lexical_score=round(float(lexical[idx]), 4),
            semantic_score=round(float(semantic[idx]), 4) if semantic is not None else None, reasons=reasons,
        ), analysis, semantic_strong))
        if len(results) >= limit:
            break
    return results, info


# --------------------------------------------------------------------------------------------------
# Supabase (pgvector) retrieval — server-side secret key, corpus tables only
# --------------------------------------------------------------------------------------------------

async def search_supabase(analysis: QueryAnalysis, limit: int, embedder: Embedder | None,
                          transport: httpx.AsyncBaseTransport | None = None) -> tuple[list[Retrieved], dict] | None:
    url, secret = settings.supabase_url.rstrip("/"), settings.supabase_secret_key
    if not url or not secret:
        return None
    headers = {"apikey": secret, "Authorization": f"Bearer {secret}", "Content-Type": "application/json"}
    lexical_query = " or ".join(dict.fromkeys(analysis.lexical_terms[:24])) or analysis.original
    info = {"lexical": True, "semantic": False}
    try:
        async with httpx.AsyncClient(timeout=12, transport=transport) as client:
            lex = await client.post(f"{url}/rest/v1/rpc/search_legal_chunks_lexical", headers=headers,
                                    json={"query_text": lexical_query, "match_count": 20})
            lex_rows = lex.json() if lex.status_code < 400 else []
            sem_rows: list[dict] = []
            if embedder is not None:
                vector = embedder.embed([analysis.semantic_text])[0]
                sem = await client.post(f"{url}/rest/v1/rpc/match_legal_chunks", headers=headers, json={
                    "query_embedding": "[" + ",".join(f"{v:.6f}" for v in vector.tolist()) + "]",
                    "match_threshold": 0.3, "match_count": 20})
                if sem.status_code < 400:
                    sem_rows = sem.json()
                    info["semantic"] = True
    except (httpx.HTTPError, ValueError):
        logger.warning("supabase_retrieval_failed")
        return None
    if lex.status_code >= 400 and not sem_rows:
        return None

    def key(row: dict) -> str:
        return row.get("chunk_id") or f"{row.get('document_id')}|{row.get('page_start')}|{row.get('snippet', '')[:80]}"

    pool: dict[str, dict] = {}
    lex_keys = [key(r) for r in lex_rows]
    sem_keys = [key(r) for r in sem_rows]
    for row in lex_rows + sem_rows:
        pool.setdefault(key(row), row)
    ids = list(pool)
    position = {k: i for i, k in enumerate(ids)}
    fused = rrf_fuse([[position[k] for k in lex_keys], [position[k] for k in sem_keys]], [1.0, 0.9])
    results = []
    for idx, score in sorted(fused.items(), key=lambda item: item[1], reverse=True)[:limit]:
        row = dict(pool[ids[idx]])
        row.setdefault("content", row.get("snippet", ""))
        semantic_score = next((float(r.get("score", 0)) for r in sem_rows if key(r) == ids[idx]), None)
        results.append(assess(Retrieved(
            chunk=row, score=round(score, 6), semantic_score=semantic_score,
            reasons=[r for r, keys in (("lexical", lex_keys), ("semantic", sem_keys)) if ids[idx] in keys]), analysis,
            getattr(embedder, "strong_threshold", SEMANTIC_STRONG)))
    return results, info
