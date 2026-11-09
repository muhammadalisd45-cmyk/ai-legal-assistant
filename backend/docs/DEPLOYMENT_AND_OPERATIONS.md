# Deployment and Operations

## 1. Production configuration

| Variable | Production value |
|---|---|
| `ENVIRONMENT` | `production` (enables HSTS, hides `/docs`, enforces config guard) |
| `AUTH_MODE` | `supabase` (recommended) — or `local` with a ≥ 32-char random `LOCAL_JWT_SECRET` |
| `CASE_STORE` | `supabase` (RLS-enforced) — `sqlite` only for single-node pilots with a persistent volume |
| `SUPABASE_URL`, `SUPABASE_ANON_KEY` | project values |
| `SUPABASE_SECRET_KEY` | service-role key, **server only**, used for corpus retrieval/ingestion |
| `CORS_ALLOWED_ORIGINS` | exact frontend origin(s), e.g. `https://navigator.example.pk` |
| `LLM_*` | provider settings; leave empty to run on fallbacks |
| `TRUST_PROXY_HEADERS` | `true` only behind a proxy that overwrites `X-Forwarded-For` |
| `CLAMAV_HOST` | clamd sidecar host (recommended) |

The app refuses to start if the configuration is unsafe (`/health/ready` also lists `config_problems`).

## 2. Supabase production integration

1. Apply migrations in order: `frontend/supabase/migrations/001…005`, then `seed.sql`.
2. Enable Anonymous sign-ins (the citizen flow uses anonymous sessions).
3. Ingest the corpus into pgvector:
   ```bash
   python scripts/acquire_corpus.py && python scripts/build_index.py
   SUPABASE_URL=… SUPABASE_SECRET_KEY=… python scripts/push_to_supabase.py
   ```
   With `RETRIEVAL_BACKEND=auto` the backend uses Supabase hybrid retrieval when the secret key is set and falls back to
   the bundled local index automatically.
4. Run the RLS live verification in `SECURITY_CHECKLIST.md` on staging.

## 3. Backend deployment

```bash
docker build -f backend/Dockerfile -t pjn-backend .     # from repo root; bakes corpus index + embedding model
docker run -p 8000:8000 --env-file backend/.env.production -v pjn-state:/srv/state pjn-backend
```
* The container runs as a non-root user, with a `HEALTHCHECK` on `/health`.
* Two uvicorn workers; the in-process rate limiter is per worker. With several replicas, add limits at the proxy/CDN.
* Any container host works (Render, Railway, Fly.io, Azure Container Apps, a VM). Put TLS termination in front.

## 4. Frontend–backend connection

In the Next.js deployment set `BACKEND_API_URL` and `LEGAL_RAG_API_URL` to the backend's internal URL (server-side
variables; the browser never calls the backend or the LLM directly for triage/search). Verify with:

```bash
BACKEND_API_URL=https://api… NEXT_APP_URL=https://app… npm run test:integration   # in frontend/
python scripts/smoke_test.py --base https://api…                                  # in backend/
```

## 5. Health checks and monitoring

| Signal | Source | Alert when |
|---|---|---|
| Liveness | `GET /health` | non-200 for 2 min |
| Readiness | `GET /health/ready` | `status != ready`, `legal_index.chunks == 0`, `embeddings == false` |
| Error rate | JSON access logs (`status`, `path`, `duration_ms`, `request_id`) | 5xx > 1 % over 10 min |
| Latency | `duration_ms` | p95 > 3 s on `/v1/search`, > 15 s on `/api/v1/answer` |
| AI degradation | `triage_llm_failed`, `answer_llm_fallback` log events (`reason`) | > 20 % of AI requests fall back |
| Abuse | `429` counts per path | sustained spikes |
| Uploads | `document_processing_failed` events | any spike; `scan_unavailable` at all |

Logs are JSON on stdout (ship to Loki/CloudWatch/Datadog). They contain no request bodies, and PII patterns are redacted.
Every response has `X-Request-ID`; clients may send their own for tracing.

## 6. Backup and recovery

| Data | Backup | Recovery |
|---|---|---|
| Supabase Postgres (cases, messages, documents metadata, corpus) | Supabase daily backups + PITR (Pro plan); weekly `pg_dump` to separate storage | Restore PITR to a new project → update `SUPABASE_URL`/keys → smoke test |
| Supabase Storage (`case-documents`) | Scheduled copy to a second bucket/region | Re-sync objects; paths are deterministic (`user/case/doc`) |
| SQLite pilot (`/srv/state/pjn.sqlite3`) | `sqlite3 pjn.sqlite3 ".backup '/backups/pjn-$(date +%F).sqlite3'"` nightly + uploads dir | Stop container, replace file, start, smoke test |
| Legal corpus | Reproducible: `acquire_corpus.py` (hash-checked) + `build_index.py`; `provenance.json` and the chunk JSONL are versioned in git | Rebuild index; compare SHA-256 in provenance |

Run a restore drill each quarter and record the time-to-recover.

## 7. Maintenance plan

* **Monthly:** re-run `acquire_corpus.py`. A changed SHA-256 means the official PDF was amended. Rebuild the index,
  re-run `evaluate_retrieval.py`, review the diff, then push to Supabase.
* **Corpus growth:** add rows to `frontend/data/member4_manifest.csv` only with an official, verified PDF URL. Then run
  `npm run test:member4` in `frontend/` and `pytest` in `backend/`. Placeholder and metadata-only rows are never ingested.
* **Quarterly:** dependency audit (`pip-audit`, `npm audit`), secret rotation (`LOCAL_JWT_SECRET`, Supabase keys,
  LLM key), restore drill, and a review of the retrieval evaluation against new real-world queries.
* **On LLM model change:** run the answer/triage tests against the provider in staging and spot-check
  `unsupported_claims_removed` rates in logs.
