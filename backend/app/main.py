from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cases import router as cases_router
from app.api.legal import answer_router, search_router
from app.api.routes import router as triage_router
from app.api.system import VERSION, auth_router, health_router
from app.core.config import settings
from app.core.errors import install_error_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware

logger = logging.getLogger("pjn.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    problems = settings.production_problems()
    if problems:
        # Refuse to start an insecure production deployment.
        raise RuntimeError("Unsafe production configuration: " + "; ".join(problems))
    logger.info("startup", extra={"environment": settings.environment, "auth_mode": settings.auth_mode,
                                  "case_store": settings.case_store, "llm_configured": settings.llm_configured})
    if settings.environment != "test":
        await _warm_up()
    yield


async def _warm_up() -> None:
    """Load the corpus index and embedding model before serving, so the first search is not slow enough to
    trip the frontend's 12 s proxy timeout (which would silently degrade it to metadata-only)."""
    import asyncio
    import time

    from app.core.index_state import local_index
    from app.legal.embeddings import get_embedder

    def warm() -> dict:
        started = time.perf_counter()
        index, status = local_index()
        embedder = get_embedder()
        if embedder is not None and index.embeddings is not None:
            embedder.embed(["warm-up"])
        return {"chunks": status.chunks, "embeddings": status.embeddings,
                "seconds": round(time.perf_counter() - started, 1)}

    try:
        logger.info("warm_up_complete", extra=await asyncio.to_thread(warm))
    except Exception:  # noqa: BLE001 — never block startup; search degrades gracefully
        logger.exception("warm_up_failed")


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    app = FastAPI(
        title="Pakistan Justice Navigator — Backend API",
        version=VERSION,
        description=("Legal intake/triage, evidence-aware legal search, citation-backed answers and case management. "
                     "Legal information only — not a substitute for a lawyer or a court."),
        lifespan=lifespan,
        docs_url=None if settings.environment == "production" else "/docs",
        redoc_url=None,
    )
    install_error_handlers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=False,  # bearer tokens, no cookies
        allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID", "X-PJN-Client"],
        expose_headers=["X-Request-ID", "Retry-After"],
        max_age=600,
    )
    app.add_middleware(RequestContextMiddleware, max_body_bytes=settings.max_request_body_bytes,
                       hsts=settings.environment == "production")

    app.include_router(health_router)
    app.include_router(search_router)
    app.include_router(triage_router, prefix="/api/v1")
    app.include_router(answer_router, prefix="/api/v1")
    app.include_router(cases_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    return app


app = create_app()
