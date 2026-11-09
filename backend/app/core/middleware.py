from __future__ import annotations

import json
import logging
import re
import time
import uuid

from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = logging.getLogger("pjn.access")

_REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9._-]{8,64}$")

SECURITY_HEADERS = [
    (b"x-content-type-options", b"nosniff"),
    (b"x-frame-options", b"DENY"),
    (b"referrer-policy", b"no-referrer"),
    (b"cross-origin-opener-policy", b"same-origin"),
    (b"permissions-policy", b"camera=(), microphone=(), geolocation=()"),
    (b"cache-control", b"no-store"),
]
# Swagger UI needs inline scripts from a CDN; API responses get a locked-down CSP.
API_CSP = (b"content-security-policy", b"default-src 'none'; frame-ancestors 'none'")


class RequestContextMiddleware:
    """Request ID, security headers, request-body size limit, redacted access log."""

    def __init__(self, app: ASGIApp, max_body_bytes: int, hsts: bool = False):
        self.app = app
        self.max_body_bytes = max_body_bytes
        self.hsts = hsts

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])}
        incoming = headers.get("x-request-id", "")
        request_id = incoming if _REQUEST_ID_RE.match(incoming) else uuid.uuid4().hex
        scope.setdefault("state", {})["request_id"] = request_id
        path = scope.get("path", "")
        started = time.perf_counter()
        status_holder = {"status": 500}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                status_holder["status"] = message["status"]
                raw = list(message.get("headers", []))
                existing = {name.lower() for name, _ in raw}
                raw.append((b"x-request-id", request_id.encode()))
                for name, value in SECURITY_HEADERS:
                    if name not in existing:
                        raw.append((name, value))
                if not path.startswith(("/docs", "/redoc")) and b"content-security-policy" not in existing:
                    raw.append(API_CSP)
                if self.hsts:
                    raw.append((b"strict-transport-security", b"max-age=63072000; includeSubDomains"))
                message["headers"] = raw
            await send(message)

        declared = headers.get("content-length")
        if declared is not None:
            try:
                too_large = int(declared) > self.max_body_bytes
            except ValueError:
                too_large = True
            if too_large:
                await _reject_413(send_wrapper, request_id)
                self._log(scope, 413, started, request_id)
                return

        received = 0

        async def receive_wrapper() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_body_bytes:
                    raise _BodyTooLarge()
            return message

        try:
            await self.app(scope, receive_wrapper, send_wrapper)
        except _BodyTooLarge:
            await _reject_413(send_wrapper, request_id)
            status_holder["status"] = 413
        finally:
            self._log(scope, status_holder["status"], started, request_id)

    @staticmethod
    def _log(scope: Scope, status: int, started: float, request_id: str) -> None:
        # Path only — never query strings or bodies.
        logger.info(
            "request",
            extra={
                "method": scope.get("method"),
                "path": scope.get("path"),
                "status": status,
                "duration_ms": round((time.perf_counter() - started) * 1000, 1),
                "request_id": request_id,
            },
        )


class _BodyTooLarge(Exception):
    pass


async def _reject_413(send: Send, request_id: str) -> None:
    body = json.dumps({
        "error": {"code": "payload_too_large", "message": "Request body is too large.", "request_id": request_id},
        "detail": "Request body is too large.",
    }).encode()
    await send({"type": "http.response.start", "status": 413,
                "headers": [(b"content-type", b"application/json"), (b"content-length", str(len(body)).encode())]})
    await send({"type": "http.response.body", "body": body})
