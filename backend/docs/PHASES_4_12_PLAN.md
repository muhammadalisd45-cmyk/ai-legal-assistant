# Backend Phases 4–12 — Implementation Plan

Status baseline (pulled `origin/main` @ `84c552e`, 2026-11-08):

* `backend/` — FastAPI triage module only (`/health`, `/api/v1/triage`, `/api/v1/document`), 6 tests.
* `frontend/services/legal-rag/` — separate lexical-only search prototype; `data/rag_index/legal_chunks.jsonl` is **empty** (no corpus ingested).
* Supabase schema exists (migrations 001–004) but no credentials are configured; the frontend writes cases to Supabase directly.
* LLM client sends a non-strict JSON schema with `strict: true`, which OpenAI-compatible providers reject → triage silently always fell back.

Decision: `backend/` becomes the single production API. It mounts every endpoint in the API table, owns the corpus
pipeline, and keeps the existing frontend contracts (`/api/v1/triage`, `/v1/search` response fields) backward compatible.
The manifest (`frontend/data/member4_manifest.csv`) remains the single source of truth for corpus metadata.

## Phase 4 — Triage
* `app/core/text.py`: script-based language detection (Urdu / Roman Urdu / English), Roman-Urdu spelling normalisation.
* `app/services/urgency.py`: rule-based urgency indicators (arrest/custody, violence, threats, imminent hearing/eviction, self-harm) in EN / Roman Urdu / Urdu. Server-side urgency floor is applied on top of LLM output.
* Expanded deterministic fallback: 10 categories, language-matched questions, message-derived summary.
* LLM: strict-compatible schema generator, retry on 429/5xx, hard timeout, JSON-object mode option.
* Response adds `detected_language`, `urgency_indicators`, `request_id` (additive; frontend adapter unaffected).

## Phase 5 — Official documents
* `scripts/acquire_corpus.py`: official-host allowlist, OS trust store (`truststore`) instead of disabling TLS, `%PDF` + pypdf validation, SHA-256, `provenance.json`.
* `app/legal/extraction.py`: per-page extraction, cleaning (page numbers, hyphenation, whitespace), section/article detection with page carry-over.
* Placeholders and `metadata_only` rows are never ingested as evidence.

## Phase 6 — RAG
* Section-aware chunking with page ranges and stable `chunk_id`s.
* Embeddings: `paraphrase-multilingual-MiniLM-L12-v2` (384-d, multilingual, local ONNX via fastembed). Dimension asserted on build and load; embeddings aligned to chunks by content hash.
* Local hybrid retrieval: BM25 + cosine, fused with Reciprocal Rank Fusion; multilingual query expansion.
* Supabase path: lexical RPC + `match_legal_chunks` fused the same way; push script uploads embeddings.
* `scripts/evaluate_retrieval.py`: hit@k / MRR per language (en / roman-ur / ur), reported separately.

## Phase 7 — `POST /v1/search`
Validation, filters, page numbers, `#page=` deep links, `evidence_level` (`chunk` vs `metadata`), provenance, fallback chain Supabase → local index → metadata-only with explicit `warning` and `fallback_reason`.

## Phase 8 — `POST /api/v1/answer`
Retrieve → evidence blocks `[E1..En]` → LLM JSON → citation guard (unknown evidence IDs dropped; section/article/case citations not present in cited evidence are removed and flagged). No evidence → explicit uncertainty response. No LLM → extractive, quote-only answer. Prompt-injection detection + evidence delimiting.

## Phase 9 — Cases and documents
`/api/v1/cases` CRUD, messages, document upload. Repository abstraction: SQLite (local/dev) and Supabase PostgREST with the **user's JWT** so RLS is enforced. Uploads: size/extension/magic/MIME checks, active-content PDF rejection, optional ClamAV, random storage names, processing status (`queued → processing → analyzed | failed`), owner-only access.

## Phase 10 — Security
Auth (`local` signed HS256 anonymous tokens or `supabase` token verification), owner checks everywhere, rate limiting, CORS allowlist, security headers, body-size limit, request IDs, PII-redacting logs, uniform error envelope, production config validation, migration 005 (storage bucket + policies), static RLS verification test, backup/recovery doc.

## Phase 11 — Tests
Unit, API, DB-repository, auth/access-control, RAG retrieval, citation guard, multilingual, security, failure/timeout, frontend↔backend contract integration (runs the frontend adapter against a live backend).

## Phase 12 — Deployment
Dockerfile, `/health` + `/health/ready`, JSON logs, deployment + monitoring/maintenance docs, env templates.
