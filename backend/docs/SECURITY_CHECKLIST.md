# Security Checklist

Status legend: ✅ implemented and covered by an automated test · 🟡 implemented, needs verification in the target environment · ⬜ open.

| # | Control | Status | Where / how verified |
|---|---|---|---|
| 1 | Input validation: strict schemas (`extra="forbid"`), length limits, control/bidi character stripping, enum languages | ✅ | `schemas/*`, `core/text.py` · `test_triage.py::test_invalid_requests_rejected`, `test_search_api.py::test_query_validation` |
| 2 | Validation errors never echo submitted text | ✅ | `core/errors.py` · `test_invalid_requests_rejected` |
| 3 | Authentication on all case/document routes | ✅ | `core/security.py` · `test_case_routes_require_auth` |
| 4 | Token verification: expired, forged-signature and `alg=none` tokens rejected | ✅ | `test_invalid_expired_and_tampered_tokens_rejected` |
| 5 | Authorization: owner-only access, 404 for non-owners (cases, messages, documents, downloads, uploads) | ✅ | `test_users_cannot_see_or_modify_each_others_cases`, `test_upload_to_someone_elses_case_is_404`, `test_pdf_upload_processing_and_owner_only_download` |
| 6 | Database RLS: every public table has RLS; user tables owner-scoped via `auth.uid()`; no client deletes; corpus tables not writable by browser roles | ✅ (static) 🟡 (live) | `test_security.py::test_every_public_table_has_rls_enabled` etc. Live check: run the SQL in *RLS live verification* below against staging. |
| 7 | Supabase calls for user data use the **user's JWT** (RLS applies), never the service key | ✅ | `test_supabase_repo_forwards_user_jwt_not_service_key` |
| 8 | Citizens cannot forge `system` messages (API + RLS) | ✅ | `test_messages`, migration 005 policy |
| 9 | Storage: private bucket, per-user folder policy, random object names, immutable uploads | ✅ (static) 🟡 (live) | migration 005 · `test_storage_bucket_is_private_and_folder_scoped` |
| 10 | Upload security: size cap while streaming, extension + magic-byte agreement, MIME not trusted, encrypted/JS/embedded-file/XFA PDFs rejected, page cap, filename sanitised, `Content-Disposition: attachment`, `nosniff` | ✅ | `test_upload_rejections`, `test_upload_size_limit`, `test_upload_filename_is_sanitised` |
| 11 | Malware scanning: ClamAV INSTREAM when `CLAMAV_HOST` set; fails closed if unreachable | 🟡 | `documents/validation.py::clamav_scan` — deploy clamd and run the EICAR test file |
| 12 | Rate limiting (general and stricter AI budget) with `Retry-After` | ✅ | `test_rate_limiting`, `test_ai_rate_limit_is_separate_and_stricter`. In-process: use edge/proxy limits or Redis for multi-replica deployments. |
| 13 | CORS allow-list, no credentials, `*` refused in production | ✅ | `test_cors_allowlist`, `test_production_configuration_guard` |
| 14 | Security headers (nosniff, DENY framing, no-referrer, CSP on API responses, HSTS in production, `no-store`) | ✅ | `test_security_headers_and_request_id` |
| 15 | Request body size limit (413 before parsing) | ✅ | `test_request_body_limit` |
| 16 | Secret management: env-only, `.env` gitignored, empty secrets in templates, service key server-side only, unsafe production config refuses to start | ✅ | `test_secrets_are_not_committed`, `test_production_configuration_guard`, `main.lifespan` |
| 17 | Logging without private data: no bodies/query strings logged, PII redaction (email, phone, CNIC, JWT), exception text truncated | ✅ | `core/logging.py` · `test_log_redaction` |
| 18 | Internal errors never leak details (uniform envelope + request ID) | ✅ | `test_unhandled_errors_do_not_leak_internals` |
| 19 | Timeouts: LLM (per-request + wall clock, retries), Supabase (8–12 s), document processing (60 s), frontend proxies (12 s) | ✅ | `test_llm_failures_degrade_to_fallback`, `test_llm_timeout_falls_back` |
| 20 | Prompt-injection handling (delimiting, tag escaping, detection, model instructions) | ✅ | `test_prompt_injection_is_flagged_and_ignored`, `test_user_text_cannot_break_out_of_prompt_tags`, `test_evidence_is_delimited_and_injection_flagged` |
| 21 | Corpus integrity: official-host allow-list (https only), redirect host re-checked, TLS always verified (OS trust store), SHA-256 provenance checked at index time | ✅ | `test_manifest_acquirable_rules`, `build_chunk_rows` provenance check |
| 22 | Path traversal: manifest file names, storage paths (UUID-only), download paths | ✅ | `test_manifest_destination_blocks_path_traversal`, `storage.object_path` |
| 23 | Dependency audit | ⬜ | Run `pip-audit -r requirements.txt` and `npm audit` in CI |
| 24 | Backups and restore drill | 🟡 | See `DEPLOYMENT_AND_OPERATIONS.md` § Backup & recovery |

## RLS live verification (run against staging with two test users)

```sql
-- as user A (set request.jwt.claims to A) create a case, then as user B:
select count(*) from public.cases;                         -- expect 0
update public.cases set status = 'closed';                 -- expect 0 rows
insert into public.case_messages (case_id, role, content)
  values ('<A case id>', 'citizen', 'x');                   -- expect RLS violation
insert into public.case_messages (case_id, role, content)
  values ('<B case id>', 'system', 'x');                    -- expect RLS violation (role)
select * from public.legal_chunks limit 1;                  -- anon/authenticated: permission denied
```
