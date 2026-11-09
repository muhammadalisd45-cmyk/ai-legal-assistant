"""Health, readiness and auth endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.index_state import local_index
from app.core.rate_limit import rate_limit
from app.core.security import CurrentUser, get_current_user, issue_local_token
from app.repositories import get_repository

health_router = APIRouter(tags=["system"])
auth_router = APIRouter(prefix="/auth", tags=["auth"])

VERSION = "1.0.0"


@health_router.get("/health")
def health():
    """Liveness: the process is up. Kept dependency-free so it never flaps."""
    return {"status": "ok", "module": "ai-legal-triage", "service": "pakistan-justice-navigator-backend",
            "version": VERSION}


@health_router.get("/health/ready")
async def ready():
    """Readiness: dependencies and corpus state. 200 when the API can serve requests (degraded modes included)."""
    _, status = local_index()
    store = await get_repository().health()
    checks = {
        "case_store": store,
        "legal_index": {"chunks": status.chunks, "documents": status.documents, "embeddings": status.embeddings,
                        "embedding_dim": status.embedding_dim, "problem": status.problem or None},
        "llm": {"configured": settings.llm_configured, "fallback": "deterministic" if not settings.llm_configured else None},
        "auth_mode": settings.auth_mode,
        "supabase_retrieval": bool(settings.supabase_url and settings.supabase_secret_key),
        "config_problems": settings.production_problems(),
    }
    ok = store.get("ok", False) and not checks["config_problems"]
    from fastapi.responses import JSONResponse

    return JSONResponse(status_code=200 if ok else 503, content={"status": "ready" if ok else "degraded",
                                                                 "version": VERSION, "checks": checks})


@auth_router.post("/anonymous", dependencies=[Depends(rate_limit("auth"))])
def anonymous_session():
    """AUTH_MODE=local only: issue a signed anonymous session (mirrors Supabase anonymous sign-in)."""
    return issue_local_token()


@auth_router.get("/me")
async def me(user: CurrentUser = Depends(get_current_user)):
    return {"id": user.id, "auth_mode": user.mode, "is_anonymous": user.is_anonymous}
