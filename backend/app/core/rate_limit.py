"""In-process sliding-window rate limiter.

Suitable for a single instance. For multiple replicas, enforce limits at the edge/proxy or swap
`RateLimiter` for a Redis-backed implementation with the same `check()` signature.
"""
from __future__ import annotations

import threading
import time
from collections import defaultdict, deque

from fastapi import Request

from app.core.config import settings
from app.core.errors import AppError


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str, limit: int, window_seconds: float = 60.0) -> None:
        now = time.monotonic()
        with self._lock:
            bucket = self._hits[key]
            while bucket and now - bucket[0] >= window_seconds:
                bucket.popleft()
            if len(bucket) >= limit:
                retry_after = max(1, int(window_seconds - (now - bucket[0])) + 1)
                raise AppError(429, "Too many requests. Please wait and try again.",
                               headers={"Retry-After": str(retry_after)})
            bucket.append(now)
            if len(self._hits) > 50_000:  # bound memory under key-spraying
                for stale in [k for k, v in self._hits.items() if not v or now - v[-1] >= window_seconds][:10_000]:
                    self._hits.pop(stale, None)

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


limiter = RateLimiter()


def client_ip(request: Request) -> str:
    if settings.trust_proxy_headers:
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit(scope: str, ai: bool = False):
    """FastAPI dependency factory."""

    async def dependency(request: Request) -> None:
        if not settings.rate_limit_enabled:
            return
        limit = settings.rate_limit_ai_per_minute if ai else settings.rate_limit_per_minute
        limiter.check(f"{scope}:{client_ip(request)}", limit)

    return dependency
