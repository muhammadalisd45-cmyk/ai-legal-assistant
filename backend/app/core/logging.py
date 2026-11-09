"""JSON logging with PII redaction.

Policy: request/response bodies (citizen case facts) are never logged. Free-text values that do
reach a log record are passed through `redact()` which masks emails, phone numbers, CNICs and
bearer tokens.
"""
from __future__ import annotations

import json
import logging
import re
import sys
from datetime import datetime, timezone

_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[email]"),
    (re.compile(r"\b\d{5}-?\d{7}-?\d\b"), "[cnic]"),  # Pakistani CNIC 12345-1234567-1
    (re.compile(r"(?:\+92|0092|\b0)3\d{2}[-\s]?\d{7}\b"), "[phone]"),
    (re.compile(r"\+?\d[\d\s-]{9,}\d"), "[number]"),
    (re.compile(r"(?i)bearer\s+[a-z0-9._\-]+"), "Bearer [token]"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+"), "[jwt]"),
]

_STANDARD_ATTRS = set(vars(logging.LogRecord("", 0, "", 0, "", None, None))) | {"message", "asctime"}


def redact(value: str) -> str:
    text = str(value)
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": redact(record.getMessage()),
        }
        for key, value in record.__dict__.items():
            if key in _STANDARD_ATTRS or key.startswith("_"):
                continue
            payload[key] = redact(value) if isinstance(value, str) else value
        if record.exc_info:
            # Exception type only; tracebacks can contain request data.
            payload["exc_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
            payload["exc"] = redact(str(record.exc_info[1]))[:500]
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    if any(getattr(handler, "_pjn", False) for handler in root.handlers):
        root.setLevel(level.upper())
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler._pjn = True  # type: ignore[attr-defined]
    root.addHandler(handler)
    root.setLevel(level.upper())
    # Access logs would include query strings; our middleware emits a redacted access line instead.
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("httpx").setLevel(logging.WARNING)
