import os
import shutil
import sys
from pathlib import Path

# Hermetic test configuration — must be set before the app is imported.
os.environ.update({
    "ENVIRONMENT": "test",
    "LLM_API_KEY": "",
    "LLM_MODEL": "",
    "AUTH_MODE": "local",
    "LOCAL_JWT_SECRET": "test-secret-test-secret-test-secret-1234",
    "CASE_STORE": "sqlite",
    "RATE_LIMIT_ENABLED": "false",
    "SUPABASE_URL": "",
    "SUPABASE_ANON_KEY": "",
    "SUPABASE_SECRET_KEY": "",
    "CLAMAV_HOST": "",
    "LOG_LEVEL": "WARNING",
})
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.core.config import REPO_DIR, settings  # noqa: E402
from app.core.rate_limit import limiter  # noqa: E402
from app.documents.storage import LocalStorage, set_storage  # noqa: E402
from app.legal import embeddings as embeddings_module  # noqa: E402
from app.legal.embeddings import HashingEmbedder, set_embedder  # noqa: E402
from app.legal.index import clear_index_cache, write_index  # noqa: E402
from app.main import app  # noqa: E402
from app.repositories import set_repository  # noqa: E402
from app.repositories.sqlite_repo import SQLiteCaseRepository  # noqa: E402
from helpers import FIXTURE_CHUNKS  # noqa: E402

REAL_DATA_DIR = REPO_DIR / "frontend"


@pytest.fixture(autouse=True)
def _isolation(tmp_path, monkeypatch):
    """Fresh in-memory DB, temp upload dir, fixture corpus, hashing embedder and no LLM for every test."""
    monkeypatch.setattr(settings, "llm_api_key", "")
    monkeypatch.setattr(settings, "llm_model", "")
    monkeypatch.setattr(settings, "llm_base_url", "https://llm.test/v1")
    monkeypatch.setattr(settings, "llm_fallback_models", "")
    monkeypatch.setattr(settings, "llm_free_only", True)
    monkeypatch.setattr(settings, "llm_response_format", "json_schema")
    monkeypatch.setattr(settings, "rate_limit_enabled", False)
    monkeypatch.setattr(settings, "supabase_secret_key", "")
    monkeypatch.setattr(settings, "upload_dir", tmp_path / "uploads")
    set_repository(SQLiteCaseRepository(":memory:"))
    set_storage(LocalStorage(tmp_path / "uploads"))

    data_dir = tmp_path / "legal"
    (data_dir / "data" / "rag_index").mkdir(parents=True)
    shutil.copy(REAL_DATA_DIR / "data" / "member4_manifest.csv", data_dir / "data" / "member4_manifest.csv")
    monkeypatch.setattr(settings, "legal_data_dir", data_dir)
    embedder = HashingEmbedder()
    write_index([dict(c) for c in FIXTURE_CHUNKS], settings.chunks_path, settings.embeddings_path,
                settings.embeddings_meta_path, embedder, log=lambda *_: None)
    set_embedder(embedder)
    clear_index_cache()
    limiter.reset()
    yield
    clear_index_cache()
    set_repository(None)
    set_storage(None)
    embeddings_module._default = None
    embeddings_module._default_failed = False


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def empty_index():
    settings.chunks_path.write_text("", encoding="utf-8")
    for path in (settings.embeddings_path, settings.embeddings_meta_path):
        if path.exists():
            path.unlink()
    clear_index_cache()


@pytest.fixture
def llm(monkeypatch):
    """Configure a fake LLM provider; returns a function that installs a scripted transport."""
    from app.api import legal as legal_api
    from app.api import routes as routes_api
    from app.services.llm_client import LLMClient

    monkeypatch.setattr(settings, "llm_api_key", "test-key")
    monkeypatch.setattr(settings, "llm_model", "test-model:free")
    monkeypatch.setattr(settings, "llm_timeout_seconds", 2.0)
    monkeypatch.setattr(settings, "llm_max_retries", 1)

    def install(transport):
        client = LLMClient(transport=transport)
        monkeypatch.setattr(routes_api.service, "llm", client)
        monkeypatch.setattr(legal_api.answer_service, "llm", client)
        from app.api import cases as cases_api

        monkeypatch.setattr(cases_api.triage_service, "llm", client)
        return transport

    return install


def auth_headers(client) -> dict:
    token = client.post("/api/v1/auth/anonymous").json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
