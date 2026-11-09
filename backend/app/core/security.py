"""Authentication.

* AUTH_MODE=local    — the backend issues signed (HS256) anonymous user tokens via POST /api/v1/auth/anonymous.
                       Suitable for local development and single-tenant self-hosting.
* AUTH_MODE=supabase — the client sends its Supabase Auth access token; the backend verifies it with the
                       Supabase Auth server (works for both legacy HS256 and asymmetric signing keys). The same
                       token is forwarded to PostgREST so database RLS also applies.
"""
from __future__ import annotations

import hashlib
import threading
import time
import uuid
from dataclasses import dataclass

import httpx
import jwt
from fastapi import Request

from app.core.config import settings
from app.core.errors import AppError

LOCAL_ISSUER = "pjn-backend"
LOCAL_AUDIENCE = "pjn-api"


@dataclass(frozen=True)
class CurrentUser:
    id: str
    token: str
    mode: str
    is_anonymous: bool = True


def issue_local_token(user_id: str | None = None) -> dict:
    if settings.auth_mode != "local":
        raise AppError(404, "Anonymous local sessions are disabled; use Supabase Auth.")
    uid = user_id or str(uuid.uuid4())
    now = int(time.time())
    exp = now + settings.local_token_ttl_seconds
    token = jwt.encode(
        {"sub": uid, "iss": LOCAL_ISSUER, "aud": LOCAL_AUDIENCE, "iat": now, "exp": exp,
         "role": "authenticated", "is_anonymous": True},
        settings.local_jwt_secret, algorithm="HS256",
    )
    return {"access_token": token, "token_type": "bearer", "expires_at": exp, "user": {"id": uid}}


def _verify_local(token: str) -> CurrentUser:
    try:
        claims = jwt.decode(token, settings.local_jwt_secret, algorithms=["HS256"],
                            audience=LOCAL_AUDIENCE, issuer=LOCAL_ISSUER, options={"require": ["exp", "sub"]})
    except jwt.ExpiredSignatureError as exc:
        raise AppError(401, "Session expired. Please sign in again.", "token_expired") from exc
    except jwt.PyJWTError as exc:
        raise AppError(401, "Invalid authentication token.", "invalid_token") from exc
    try:
        uid = str(uuid.UUID(claims["sub"]))
    except ValueError as exc:
        raise AppError(401, "Invalid authentication token.", "invalid_token") from exc
    return CurrentUser(id=uid, token=token, mode="local", is_anonymous=bool(claims.get("is_anonymous", True)))


class _TTLCache:
    def __init__(self, ttl: float = 60.0, max_items: int = 5000):
        self.ttl, self.max_items = ttl, max_items
        self._data: dict[str, tuple[float, CurrentUser]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> CurrentUser | None:
        with self._lock:
            item = self._data.get(key)
            if item and item[0] > time.monotonic():
                return item[1]
            self._data.pop(key, None)
            return None

    def put(self, key: str, value: CurrentUser) -> None:
        with self._lock:
            if len(self._data) >= self.max_items:
                self._data.clear()
            self._data[key] = (time.monotonic() + self.ttl, value)


_supabase_cache = _TTLCache()


async def _verify_supabase(token: str, transport: httpx.AsyncBaseTransport | None = None) -> CurrentUser:
    if not settings.supabase_configured:
        raise AppError(503, "Authentication service is not configured.", "auth_not_configured")
    key = hashlib.sha256(token.encode()).hexdigest()
    cached = _supabase_cache.get(key)
    if cached:
        return cached
    try:
        async with httpx.AsyncClient(timeout=8, transport=transport) as client:
            response = await client.get(
                f"{settings.supabase_url.rstrip('/')}/auth/v1/user",
                headers={"apikey": settings.supabase_anon_key, "Authorization": f"Bearer {token}"},
            )
    except httpx.HTTPError as exc:
        raise AppError(503, "Authentication service is unavailable. Please retry.", "auth_unavailable") from exc
    if response.status_code in (401, 403):
        raise AppError(401, "Invalid or expired session.", "invalid_token")
    if response.status_code >= 400:
        raise AppError(503, "Authentication service is unavailable. Please retry.", "auth_unavailable")
    body = response.json()
    if not body.get("id"):
        raise AppError(401, "Invalid or expired session.", "invalid_token")
    user = CurrentUser(id=body["id"], token=token, mode="supabase", is_anonymous=bool(body.get("is_anonymous", False)))
    _supabase_cache.put(key, user)
    return user


def _bearer(request: Request) -> str | None:
    header = request.headers.get("authorization", "")
    scheme, _, value = header.partition(" ")
    if scheme.lower() == "bearer" and value.strip():
        return value.strip()
    return None


async def get_current_user(request: Request) -> CurrentUser:
    token = _bearer(request)
    if not token:
        raise AppError(401, "Authentication required.", "auth_required", headers={"WWW-Authenticate": "Bearer"})
    if len(token) > 4096:
        raise AppError(401, "Invalid authentication token.", "invalid_token")
    if settings.auth_mode == "local":
        return _verify_local(token)
    return await _verify_supabase(token)


async def get_optional_user(request: Request) -> CurrentUser | None:
    if not _bearer(request):
        return None
    return await get_current_user(request)
