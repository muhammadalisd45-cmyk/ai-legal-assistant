from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import json
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = BACKEND_DIR.parent

INSECURE_DEFAULT_SECRET = "dev-only-change-me-dev-only-change-me"


FREE_ROUTER_MODEL = "openrouter/free"


def is_free_model(model_id: str) -> bool:
    model_id = model_id.strip()
    return model_id.endswith(":free") or model_id == FREE_ROUTER_MODEL


class Settings(BaseSettings):
    environment: Literal["development", "test", "production"] = "development"
    log_level: str = "INFO"

    # LLM (OpenAI-compatible chat completions)
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = ""
    llm_timeout_seconds: float = 30.0
    llm_max_retries: int = Field(default=1, ge=0, le=3)
    # json_schema = strict structured outputs; json_object = providers without schema support
    llm_response_format: Literal["json_schema", "json_object"] = "json_schema"
    # Comma-separated backup models (OpenRouter tries them in order if the main one is busy/rate-limited).
    llm_fallback_models: str = ""
    # Cost guard: only allow free models (OpenRouter ids ending in ":free", or the "openrouter/free" router).
    # On OpenRouter every request is also capped at a max price of $0 server-side.
    llm_free_only: bool = True

    # Auth: "local" issues signed anonymous tokens (dev / self-hosted);
    # "supabase" verifies Supabase Auth access tokens.
    auth_mode: Literal["local", "supabase"] = "local"
    local_jwt_secret: str = INSECURE_DEFAULT_SECRET
    local_token_ttl_seconds: int = 60 * 60 * 24 * 7

    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    # Server-side only — used for corpus retrieval RPCs; never for user data.
    supabase_secret_key: str = ""
    supabase_storage_bucket: str = "case-documents"

    # Persistence
    case_store: Literal["sqlite", "supabase"] = "sqlite"
    sqlite_path: Path = BACKEND_DIR / "data" / "pjn.sqlite3"
    upload_dir: Path = BACKEND_DIR / "uploads"

    # Legal corpus (manifest stays the single source of truth under frontend/data)
    legal_data_dir: Path = REPO_DIR / "frontend"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_dim: int = 384
    semantic_search_enabled: bool = True
    retrieval_backend: Literal["auto", "local", "supabase"] = "auto"

    # Uploads
    max_upload_bytes: int = 10 * 1024 * 1024
    max_pdf_pages: int = 300
    clamav_host: str = ""
    clamav_port: int = 3310

    # HTTP hardening
    cors_allowed_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]
    )
    max_request_body_bytes: int = 12 * 1024 * 1024
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    rate_limit_ai_per_minute: int = 20
    trust_proxy_headers: bool = False

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _split_origins(cls, value):
        if isinstance(value, str):
            text = value.strip()
            if text.startswith("["):
                return json.loads(text)
            return [item.strip() for item in text.split(",") if item.strip()]
        return value

    # ---- derived paths -------------------------------------------------
    @property
    def manifest_path(self) -> Path:
        return self.legal_data_dir / "data" / "member4_manifest.csv"

    @property
    def corpus_dir(self) -> Path:
        return self.legal_data_dir / "pakistan_legal_corpus"

    @property
    def index_dir(self) -> Path:
        return self.legal_data_dir / "data" / "rag_index"

    @property
    def chunks_path(self) -> Path:
        return self.index_dir / "legal_chunks.jsonl"

    @property
    def embeddings_path(self) -> Path:
        return self.index_dir / "legal_chunk_embeddings.npy"

    @property
    def embeddings_meta_path(self) -> Path:
        return self.index_dir / "legal_chunk_embeddings.meta.json"

    @property
    def provenance_path(self) -> Path:
        return self.corpus_dir / "provenance.json"

    @property
    def llm_configured(self) -> bool:
        return bool(self.llm_api_key and self.llm_model)

    @property
    def llm_models(self) -> list[str]:
        """Primary model first, then fallbacks, de-duplicated."""
        models = [self.llm_model, *self.llm_fallback_models.split(",")]
        return list(dict.fromkeys(m.strip() for m in models if m and m.strip()))

    @property
    def llm_is_openrouter(self) -> bool:
        return "openrouter.ai" in self.llm_base_url

    def llm_paid_models(self) -> list[str]:
        """Configured models that are not free (empty when the free-only guard is off)."""
        if not self.llm_free_only:
            return []
        return [m for m in self.llm_models if not is_free_model(m)]

    @property
    def supabase_configured(self) -> bool:
        return bool(self.supabase_url and self.supabase_anon_key)

    def production_problems(self) -> list[str]:
        """Configuration that must never reach production."""
        problems: list[str] = []
        if self.environment != "production":
            return problems
        if self.auth_mode == "local" and self.local_jwt_secret == INSECURE_DEFAULT_SECRET:
            problems.append("LOCAL_JWT_SECRET must be set (or use AUTH_MODE=supabase) in production")
        if self.auth_mode == "local" and len(self.local_jwt_secret) < 32:
            problems.append("LOCAL_JWT_SECRET must be at least 32 characters")
        if self.auth_mode == "supabase" and not self.supabase_configured:
            problems.append("AUTH_MODE=supabase requires SUPABASE_URL and SUPABASE_ANON_KEY")
        if self.case_store == "supabase" and not self.supabase_configured:
            problems.append("CASE_STORE=supabase requires SUPABASE_URL and SUPABASE_ANON_KEY")
        if "*" in self.cors_allowed_origins:
            problems.append("CORS_ALLOWED_ORIGINS must not contain '*' in production")
        if not self.rate_limit_enabled:
            problems.append("Rate limiting must be enabled in production")
        return problems


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
