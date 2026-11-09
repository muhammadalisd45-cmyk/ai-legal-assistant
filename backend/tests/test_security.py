import json
import logging
import re

import httpx
import pytest

from app.core.config import BACKEND_DIR, INSECURE_DEFAULT_SECRET, REPO_DIR, Settings, settings
from app.core.logging import JsonFormatter, redact
from app.core.security import CurrentUser
from app.repositories.supabase_repo import SupabaseCaseRepository

MIGRATIONS = REPO_DIR / "frontend" / "supabase" / "migrations"


def test_health_and_ready(client):
    assert client.get("/health").json()["status"] == "ok"
    ready = client.get("/health/ready")
    assert ready.status_code == 200
    checks = ready.json()["checks"]
    assert checks["legal_index"]["chunks"] == 4 and checks["legal_index"]["embedding_dim"] == 384
    assert checks["case_store"]["ok"] is True


def test_security_headers_and_request_id(client):
    response = client.get("/health", headers={"X-Request-ID": "trace-12345678"})
    assert response.headers["x-request-id"] == "trace-12345678"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "default-src 'none'" in response.headers["content-security-policy"]
    # Malformed request IDs are replaced, not reflected.
    assert client.get("/health", headers={"X-Request-ID": "<script>"}).headers["x-request-id"] != "<script>"


def test_error_envelope_includes_request_id(client):
    body = client.post("/v1/search", json={"query": "a"}).json()
    assert body["error"]["code"] == "validation_error" and len(body["error"]["request_id"]) >= 8
    assert body["detail"]


def test_cors_allowlist(client):
    allowed = client.options("/v1/search", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST"})
    assert allowed.headers.get("access-control-allow-origin") == "http://localhost:3000"
    blocked = client.options("/v1/search", headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"})
    assert "access-control-allow-origin" not in blocked.headers


def test_request_body_limit(client, monkeypatch):
    from app import main

    small = main.RequestContextMiddleware(main.app, max_body_bytes=100)
    from starlette.testclient import TestClient

    with TestClient(small) as tc:
        response = tc.post("/v1/search", content=b"x" * 500, headers={"content-type": "application/json"})
    assert response.status_code == 413 and response.json()["error"]["code"] == "payload_too_large"


def test_rate_limiting(client, monkeypatch):
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "rate_limit_per_minute", 3)
    statuses = [client.post("/v1/search", json={"query": "bail offence"}).status_code for _ in range(4)]
    assert statuses == [200, 200, 200, 429]
    limited = client.post("/v1/search", json={"query": "bail offence"})
    assert int(limited.headers["retry-after"]) >= 1 and limited.json()["error"]["code"] == "rate_limited"


def test_ai_rate_limit_is_separate_and_stricter(client, monkeypatch):
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "rate_limit_ai_per_minute", 2)
    codes = [client.post("/api/v1/triage", json={"message": "landlord problem"}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]


def test_unhandled_errors_do_not_leak_internals(client, monkeypatch):
    from app.legal import search_service

    async def boom(*args, **kwargs):
        raise RuntimeError("secret database password=hunter2")

    monkeypatch.setattr("app.api.legal.search", boom)
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app, raise_server_exceptions=False) as tc:
        response = tc.post("/v1/search", json={"query": "bail offence"})
    assert response.status_code == 500
    assert "hunter2" not in response.text and response.json()["error"]["code"] == "internal_error"


def test_log_redaction():
    text = "Call 0300-1234567 or mail ali@example.com, CNIC 35202-1234567-1, Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.abc"
    clean = redact(text)
    for secret in ("1234567", "ali@example.com", "35202", "eyJhbGci"):
        assert secret not in clean
    record = logging.LogRecord("t", logging.INFO, __file__, 1, "user %s", ("ali@example.com",), None)
    assert "ali@example.com" not in JsonFormatter().format(record)


def test_production_configuration_guard():
    unsafe = Settings(environment="production", auth_mode="local", local_jwt_secret=INSECURE_DEFAULT_SECRET,
                      cors_allowed_origins=["*"], _env_file=None)
    problems = unsafe.production_problems()
    assert any("LOCAL_JWT_SECRET" in p for p in problems) and any("CORS" in p for p in problems)
    safe = Settings(environment="production", auth_mode="supabase", case_store="supabase",
                    supabase_url="https://x.supabase.co", supabase_anon_key="anon",
                    cors_allowed_origins=["https://app.example.pk"], rate_limit_enabled=True, _env_file=None)
    assert safe.production_problems() == []


def test_cors_origins_parse_from_comma_separated_env(monkeypatch):
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "https://a.pk, https://b.pk")
    assert Settings(_env_file=None).cors_allowed_origins == ["https://a.pk", "https://b.pk"]


def test_secrets_are_not_committed():
    gitignore = (BACKEND_DIR / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gitignore
    example = (BACKEND_DIR / ".env.example").read_text(encoding="utf-8")
    assert re.search(r"(?m)^SUPABASE_SECRET_KEY=\s*$", example)
    assert re.search(r"(?m)^LLM_API_KEY=\s*$", example)


# ---------------- Supabase: RLS is enforced with the end user's JWT ----------------

class Recorder(httpx.AsyncBaseTransport):
    def __init__(self, response):
        self.response, self.requests = response, []

    async def handle_async_request(self, request):
        self.requests.append(request)
        return httpx.Response(200, json=self.response)


@pytest.mark.anyio
async def test_supabase_repo_forwards_user_jwt_not_service_key(monkeypatch):
    monkeypatch.setattr(settings, "supabase_url", "https://proj.supabase.co")
    monkeypatch.setattr(settings, "supabase_anon_key", "anon-key")
    monkeypatch.setattr(settings, "supabase_secret_key", "SERVICE-ROLE-SECRET")
    transport = Recorder([])
    repo = SupabaseCaseRepository(transport=transport)
    user = CurrentUser(id="6f0c3c1e-0000-4000-8000-000000000000", token="user-jwt", mode="supabase")
    assert await repo.get_case(user, "PJN-ABCD1234") is None
    request = transport.requests[0]
    assert request.headers["authorization"] == "Bearer user-jwt"
    assert request.headers["apikey"] == "anon-key"
    assert "SERVICE-ROLE-SECRET" not in json.dumps(dict(request.headers))
    assert "user_id=eq.6f0c3c1e-0000-4000-8000-000000000000" in str(request.url)


@pytest.fixture
def anyio_backend():
    return "asyncio"


# ---------------- static RLS verification of the migrations ----------------

def _sql() -> str:
    return "\n".join(path.read_text(encoding="utf-8-sig") for path in sorted(MIGRATIONS.glob("*.sql"))).lower()


def test_every_public_table_has_rls_enabled():
    sql = _sql()
    tables = set(re.findall(r"create table if not exists public\.(\w+)", sql))
    assert {"cases", "case_messages", "case_documents", "legal_documents", "legal_chunks"} <= tables
    for table in tables:
        assert f"alter table public.{table} enable row level security" in sql, table


def test_user_tables_are_owner_scoped():
    sql = _sql()
    for table in ("cases", "case_messages", "case_documents"):
        policies = re.findall(rf"create policy \"[^\"]+\"\s+on public\.{table} for (\w+)\s+to (\w+)\s+(.*?);", sql, re.S)
        assert policies, table
        for command, role, body in policies:
            assert role == "authenticated", (table, command)
            assert "auth.uid()" in body, (table, command)
    assert "for delete" not in re.sub(r"--.*", "", sql.split("storage.objects")[0])  # no client deletes of case data


def test_corpus_tables_are_not_writable_by_browser_roles():
    sql = _sql()
    assert "revoke all on table public.legal_chunks from anon, authenticated" in sql
    assert "revoke insert, update, delete on table public.legal_documents from anon, authenticated" in sql
    assert "grant execute on function public.match_legal_chunks" in sql and "to service_role" in sql


def test_storage_bucket_is_private_and_folder_scoped():
    sql = _sql()
    assert "'case-documents', 'case-documents', false" in sql
    assert "(storage.foldername(name))[1] = auth.uid()::text" in sql
    assert "role in ('citizen', 'assistant')" in sql  # citizens cannot forge system messages
