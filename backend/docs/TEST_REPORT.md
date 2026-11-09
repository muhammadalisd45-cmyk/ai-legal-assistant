# Test Report — 2026-11-08

Environment: Windows 10, Python 3.13.5, Node 25.9, Next.js 16.3.8. Corpus: 13 official Pakistan Code PDFs →
3,388 chunks (3,093 with verified provision labels), 384-d `paraphrase-multilingual-MiniLM-L12-v2` embeddings.

## Update 2026-11-09 — intake quality fixes → **180 passed**
A real intake ("there is theif case where a person robbed my laptop…", answers "…caught the theif", "islamabad") came out
as an empty "General legal matter" with no sources. The following fixes are covered by `test_theft_and_clarifications.py` (18 tests) and
`test_retrieval_eval.py::test_colloquial_theft_finds_penal_provisions` (3 real-corpus tests):
* New Theft / Robbery category with everyday and misspelled vocabulary, tolerant of swapped letters in words of 5+ letters
  (for example "theif"). Ambiguous words ("chor" = leave, "cheen" = China) are excluded.
* Category-specific follow-up questions, missing facts and next steps, plus a medium review-priority baseline for theft.
* Clarification answers (`answers` on `POST /api/v1/triage`) are classified and resolve the questions and missing facts they answer.
* Search: colloquial theft/robbery words are bridged to statute vocabulary and point to PPC 378/379/390/392 and CrPC 154.
  "case" is no longer bridged to "suit", which had pulled in civil-procedure rules.
* Frontend: the intake re-runs triage with the answers, and the brief shows strong-match official provisions, labelled clarifications,
  the triage's next steps, and a readable summary and source panel.

## Backend automated suite — `python -m pytest -q` → **159 passed** (before the 2026-11-09 update)

| File | Tests | Covers |
|---|---|---|
| `test_triage.py` | 28 | multilingual fallback categories, language-matched questions, auto language, emergency guidance, injection, validation, live LLM (mocked), urgency floor, source boundary, tag escaping, 5xx/429/4xx/transport/timeout/invalid-JSON fallbacks, retry, strict schema |
| `test_text_and_urgency.py` | 27 | language detection, Roman-Urdu normalisation, bridging, sanitising, injection detection, urgency indicators EN/RU/UR, false-positive guards |
| `test_cases_and_documents.py` | 23 | auth required, expired/forged/`alg=none` tokens, CRUD, cross-user isolation, run_triage, validation, messages, uploads (processing, download, rejections, size limit, sanitised names, PNG), legacy extraction |
| `test_extraction_and_index.py` | 19 | page cleaning, footnote-fused numbering, TOC detection, sections/schedules/pages, chunk IDs, low-confidence labels, PDF validation, traversal, manifest rules, 384-d enforcement, embedding alignment, BM25 |
| `test_security.py` | 17 | health/readiness, security headers, request IDs, error envelope, CORS, body limit, rate limits, no internal leaks, log redaction, production config guard, Supabase JWT forwarding, static RLS checks |
| `test_answer.py` | 16 | citation guard (fabricated sections, wrong evidence, fake case law, unknown markers, quotes), no-evidence, weak-match gate, extractive fallback, live answers, ungrounded → fallback, timeout, delimiting |
| `test_search_api.py` | 13 | traceable chunk evidence, Roman Urdu / Urdu bridging, section references, filters, metadata-only fallback (no placeholders), validation, alias |
| `test_retrieval_eval.py` | 10 | real-corpus integrity, relevance gate (off-corpus vs relevant), per-language quality thresholds |
| `test_api.py`, `test_fallback.py` | 6 | original tests (one assertion updated: fallback urgency now uses indicators) |

## Retrieval quality (real corpus) — see `RETRIEVAL_EVAL.md`
Hybrid, k = 5: document hit 100 % / provision hit 100 % for English (16 queries), Roman Urdu (10) and Urdu (9).
The query set was also used for tuning, so these numbers are optimistic.

## Live end-to-end — `python scripts/smoke_test.py` → **17/17 passed**
Health/readiness, triage (Roman Urdu, critical floor), search in three languages, grounded answer, honest no-evidence
answer, auth required, case create/list/get, messages, PDF upload → analyzed, cross-user 404.

## Frontend ↔ backend — `npm run test:integration` (with `NEXT_APP_URL`) → **passed**
The frontend triage contract adapter ran against the live backend (EN/RU/UR). Search fields were checked against what the research UI renders, plus page references. Next.js `/api/triage` and `/api/legal-search` were confirmed to route to the backend, with no fallback.

## Frontend regression — `npm run test:core` and `npm run typecheck` → **passed**

## Live Supabase (project from `frontend/.env`, anon key only)
* `python scripts/verify_supabase_rls.py --env-file ../frontend/.env` → **15 passed, 0 failed, 2 pending migration 005**:
  * Owner-only read and update.
  * No ownership transfer, no forged owners, no cross-user messages, no deletes.
  * Corpus tables and retrieval RPCs closed to browser roles.
  * Pending until 005: `system`-message restriction, `case-documents` storage bucket.
* Backend with `AUTH_MODE=supabase`, `CASE_STORE=supabase`: `python scripts/smoke_test.py --skip-documents` → **17/17 passed**. Supabase tokens are verified, and cases and messages are stored under RLS with cross-user 404.
* Document upload returns a clean `503` until migration 005 creates the bucket and columns.

## Not verified here
* Live LLM provider (no key configured): the live paths are covered with a mocked OpenAI-compatible provider only.
* Migration 005, Supabase document uploads and pgvector retrieval: these need the SQL Editor (or the DB password / service key) to apply 005 and push the corpus.
* Docker image build (Docker is not installed on this machine).
* ClamAV scanning (no clamd available).
