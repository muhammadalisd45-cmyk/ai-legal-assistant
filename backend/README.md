# Pakistan Justice Navigator — Backend API

FastAPI service for legal intake/triage, evidence-aware legal search over official Pakistani law,
citation-backed answers, and case management. **Legal information only — never a substitute for a lawyer or a court.**

## Quick start

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env               # works as-is for local development

# Corpus (one-time, ~10–15 min): download official PDFs → extract → chunk → embed
python scripts/acquire_corpus.py   # 13 Pakistan Code PDFs, SHA-256 provenance
python scripts/build_index.py      # 3,388 chunks + 384-d embeddings

uvicorn app.main:app --reload --port 8000
python scripts/smoke_test.py       # 17 live end-to-end checks
```

Swagger UI: http://localhost:8000/docs (disabled when `ENVIRONMENT=production`).
Frontend: set `BACKEND_API_URL=http://localhost:8000` and `LEGAL_RAG_API_URL=http://localhost:8000` in `frontend/.env.local`.

Without an LLM key every AI endpoint still works through transparent fallbacks (deterministic triage,
quote-only extractive answers). Responses always say which mode produced them.

## API

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | – | Liveness |
| GET | `/health/ready` | – | Readiness: case store, corpus index, embeddings, LLM, config problems |
| POST | `/api/v1/triage` | – | Legal-issue triage (EN / Urdu / Roman Urdu, urgency indicators) |
| POST | `/v1/search` | – | Evidence-aware legal search (alias `/api/v1/search`) |
| POST | `/api/v1/answer` | – | Grounded, citation-backed answer |
| POST | `/api/v1/auth/anonymous` | – | `AUTH_MODE=local` only: signed anonymous session |
| GET | `/api/v1/auth/me` | ✓ | Current user |
| POST | `/api/v1/cases` | ✓ | Create a case (`run_triage: true` to triage and store the result) |
| GET | `/api/v1/cases` | ✓ | List own cases |
| GET / PATCH | `/api/v1/cases/{case_id}` | ✓ | Retrieve / update (UUID or public case ID) |
| POST / GET | `/api/v1/cases/{case_id}/messages` | ✓ | Save / list case messages |
| POST / GET | `/api/v1/cases/{case_id}/documents` | ✓ | Upload (202, async processing) / list documents |
| GET | `/api/v1/cases/{case_id}/documents/{id}` | ✓ | Status + extracted text |
| GET | `/api/v1/cases/{case_id}/documents/{id}/content` | ✓ | Download (owner only) |
| POST | `/api/v1/document` | – | Legacy stateless PDF text extraction (nothing stored) |

Errors share one envelope: `{"error": {"code", "message", "request_id"}, "detail": message}`.
Non-owners get `404` for other users' cases (no ID probing).

## How the guarantees are enforced

| Requirement | Mechanism |
|---|---|
| No fabricated law | `app/legal/citation_guard.py` removes sentences citing sections/articles not in the cited evidence and any case-law citation not in the corpus; unknown evidence IDs are stripped; quotes are verified verbatim. A fully ungrounded model answer is replaced by the extractive answer. |
| Uncertainty | Only *strong* matches (calibrated semantic ≥ 0.48, or ≥ 60 % term coverage lexical-only) count as evidence. Otherwise `mode: "no_evidence"`, `grounded: false`, plain-language "I will not guess". |
| Metadata ≠ evidence | `evidence_level: "chunk"` (official text with page numbers) vs `"metadata"` (document pointer only, `is_legal_provision: false`). Placeholders are never indexed or returned. |
| Source traceability | Each chunk carries document ID, provision label, page range, `#page=N` deep link, PDF SHA-256 and fetch time (`frontend/pakistan_legal_corpus/provenance.json`). |
| Urgency ≠ legal assessment | Rule-based multilingual indicators set a floor the LLM cannot lower; `urgency_note` states it is intake priority only; critical cases get Police 15 / Rescue 1122 guidance. |
| Prompt injection | User text and evidence are delimited and tag-escaped; injection patterns are detected and flagged; the model is told such content is data. |
| LLM failure | Strict-schema JSON, retries on 429/5xx, hard timeout; any failure → labelled fallback, never a 5xx. |

## Configuration
See `.env.example`. Production refuses to start with unsafe settings (default JWT secret, `*` CORS, rate limiting off,
Supabase mode without credentials).

## Tests
```bash
python -m pytest -q          # 159 tests; corpus tests run when the real index exists
python scripts/evaluate_retrieval.py --markdown docs/RETRIEVAL_EVAL.md
```

## Docs
* `docs/PHASES_4_12_PLAN.md` — plan and decisions
* `docs/RETRIEVAL_EVAL.md` — retrieval quality per language
* `docs/SECURITY_CHECKLIST.md` — security controls and verification
* `docs/DEPLOYMENT_AND_OPERATIONS.md` — deployment, monitoring, backup/recovery, maintenance
* `docs/TEST_REPORT.md` — latest test run
