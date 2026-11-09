"""Uniform error envelope: {"error": {"code", "message", "request_id"}, "detail": message}.

`detail` is kept for backward compatibility with FastAPI-style clients.
Internal exception text is never returned to the client.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("pjn.errors")

_STATUS_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    409: "conflict",
    413: "payload_too_large",
    415: "unsupported_media_type",
    422: "validation_error",
    429: "rate_limited",
    502: "upstream_unavailable",
    503: "service_unavailable",
    504: "upstream_timeout",
}


class AppError(Exception):
    def __init__(self, status_code: int, message: str, code: str | None = None, headers: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.code = code or _STATUS_CODES.get(status_code, "error")
        self.headers = headers


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "")


def error_response(request: Request, status_code: int, message: str, code: str | None = None,
                   headers: dict | None = None, extra: dict | None = None) -> JSONResponse:
    body = {
        "error": {
            "code": code or _STATUS_CODES.get(status_code, "error"),
            "message": message,
            "request_id": _request_id(request),
        },
        "detail": message,
    }
    if extra:
        body["error"].update(extra)
    return JSONResponse(status_code=status_code, content=body, headers=headers)


def _validation_summary(exc: RequestValidationError) -> tuple[str, list[dict]]:
    fields = []
    for err in exc.errors()[:10]:
        location = ".".join(str(part) for part in err.get("loc", []) if part != "body")
        # Never echo submitted input values back (they may contain private case facts).
        fields.append({"field": location or "body", "message": err.get("msg", "invalid")})
    first = fields[0] if fields else {"field": "body", "message": "invalid request"}
    return f"Invalid request: {first['field']} — {first['message']}", fields


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError):
        return error_response(request, exc.status_code, exc.message, exc.code, exc.headers)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException):
        message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return error_response(request, exc.status_code, message, headers=getattr(exc, "headers", None))

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError):
        message, fields = _validation_summary(exc)
        return error_response(request, 422, message, "validation_error", extra={"fields": fields})

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        logger.exception("unhandled_error", extra={"path": request.url.path})
        return error_response(request, 500, "An internal error occurred. Please retry later.", "internal_error")
