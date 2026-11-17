"""OpenAI-compatible chat-completions client with strict structured output, retries and timeouts."""
from __future__ import annotations

import asyncio
import copy
import json
import logging
from typing import Any

import httpx

from app.core.config import is_free_model, settings

logger = logging.getLogger("pjn.llm")

# Keywords strict structured-output mode does not accept.
_UNSUPPORTED_KEYS = {"default", "title", "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
                     "minLength", "maxLength", "minItems", "maxItems", "pattern", "format", "examples"}


# OpenRouter rejects a `models` fallback list longer than this.
OPENROUTER_MAX_MODELS = 3


class LLMError(RuntimeError):
    """Raised for any LLM failure (not configured, transport, timeout, HTTP, invalid JSON)."""

    def __init__(self, reason: str, message: str = ""):
        super().__init__(message or reason)
        self.reason = reason


def to_strict_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Convert a pydantic JSON schema to the strict structured-output dialect:
    every object closes `additionalProperties` and lists all properties as required."""
    root = copy.deepcopy(schema)

    def walk(node: Any) -> None:
        """`node` is always a schema object (never a name→schema mapping)."""
        if not isinstance(node, dict):
            return
        for key in list(node):
            if key in _UNSUPPORTED_KEYS:
                node.pop(key)
        if node.get("type") == "object" or "properties" in node:
            props = node.setdefault("properties", {})
            node["type"] = "object"
            node["additionalProperties"] = False
            node["required"] = list(props.keys())
            for child in props.values():
                walk(child)
        if isinstance(node.get("items"), dict):
            walk(node["items"])
        for combinator in ("anyOf", "oneOf", "allOf"):
            for child in node.get(combinator, []) or []:
                walk(child)
        for child in (node.get("$defs") or {}).values():
            walk(child)

    walk(root)
    # `$ref` siblings are not allowed: pydantic emits {"$ref": ..., "default": ...}; defaults already stripped.
    return root


def _extract_json(content: str) -> dict[str, Any]:
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):] if "{" in text else text
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise LLMError("invalid_json", "model did not return a JSON object")
    try:
        value = json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        raise LLMError("invalid_json", "model returned malformed JSON") from exc
    if not isinstance(value, dict):
        raise LLMError("invalid_json", "model JSON is not an object")
    return value


class LLMClient:
    def __init__(self, transport: httpx.AsyncBaseTransport | None = None):
        self._transport = transport

    async def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: dict[str, Any],
        schema_name: str = "legal_triage_result",
        models: list[str] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """`models` overrides the configured model order (e.g. to retry on the next model after bad output);
        `timeout` caps this call when the caller has less time left than `llm_timeout_seconds`."""
        if not settings.llm_configured:
            raise LLMError("not_configured", "LLM is not configured")

        # Cost guard: never send a request to a paid model.
        paid = settings.llm_paid_models()
        order = [m for m in (models or settings.llm_models) if m]
        if settings.llm_free_only and models:
            paid = paid + [m for m in order if not is_free_model(m) and m not in paid]
        if paid:
            logger.error("llm_paid_model_blocked", extra={"models": paid})
            raise LLMError("paid_model_blocked", f"Paid models are not allowed: {', '.join(paid)}")

        url = settings.llm_base_url.rstrip("/") + "/chat/completions"
        headers = {"Authorization": f"Bearer {settings.llm_api_key}", "Content-Type": "application/json"}
        payload: dict[str, Any] = {
            "model": order[0],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
        }
        if settings.llm_is_openrouter:
            headers["HTTP-Referer"] = "https://pakistan-justice-navigator.local"
            headers["X-Title"] = "Pakistan Justice Navigator"
            routed = order[:OPENROUTER_MAX_MODELS]
            if len(routed) > 1:
                # OpenRouter tries these in order when one is rate-limited or down.
                payload["models"] = routed
            if settings.llm_free_only:
                # Server-side cap: OpenRouter refuses any provider that would charge for this request.
                payload["provider"] = {"max_price": {"prompt": 0, "completion": 0}}
            # Free "thinking" models can spend 30s+ reasoning; the answer must fit the frontend's wait budget.
            payload["reasoning"] = {"enabled": False}
        if settings.llm_response_format == "json_schema":
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": schema_name, "strict": True, "schema": to_strict_schema(json_schema)},
            }
        else:
            payload["response_format"] = {"type": "json_object"}
            payload["messages"][0]["content"] += (
                "\n\nReturn a single JSON object that matches this JSON schema exactly:\n"
                + json.dumps(json_schema, ensure_ascii=False)
            )

        timeout = min(settings.llm_timeout_seconds, timeout) if timeout else settings.llm_timeout_seconds
        attempts = settings.llm_max_retries + 1
        last: LLMError | None = None
        for attempt in range(attempts):
            try:
                # Hard wall-clock cap in addition to httpx's per-phase timeouts.
                return await asyncio.wait_for(self._post(url, headers, payload, timeout), timeout=timeout + 2)
            except LLMError as exc:
                if exc.reason == "reasoning_required":
                    # openrouter/free (or a fallback) picked a model that cannot turn reasoning off; it answered
                    # instantly with a 400, so resend once with the provider's default.
                    payload.pop("reasoning", None)
                    try:
                        return await asyncio.wait_for(self._post(url, headers, payload, timeout), timeout=timeout + 2)
                    except asyncio.TimeoutError as timeout_exc:
                        raise LLMError("timeout", "LLM request timed out") from timeout_exc
                last = exc
                if exc.reason not in {"rate_limited", "upstream_5xx", "transport"}:
                    raise
            except asyncio.TimeoutError as exc:
                # The time budget is already spent; retrying would outlast the caller's own timeout.
                raise LLMError("timeout", "LLM request timed out") from exc
            logger.warning("llm_retry", extra={"attempt": attempt + 1, "reason": last.reason})
            if attempt + 1 < attempts:
                await asyncio.sleep(min(2.0, 0.5 * (2 ** attempt)))
        assert last is not None
        raise last

    async def _post(self, url: str, headers: dict, payload: dict, timeout: float) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=timeout, transport=self._transport) as client:
                response = await client.post(url, headers=headers, json=payload)
        except httpx.TimeoutException as exc:
            raise LLMError("timeout", "LLM request timed out") from exc
        except httpx.HTTPError as exc:
            raise LLMError("transport", "LLM provider unreachable") from exc

        if response.status_code == 429:
            raise LLMError("rate_limited", "LLM provider rate limited the request")
        if response.status_code >= 500:
            raise LLMError("upstream_5xx", f"LLM provider error {response.status_code}")
        if response.status_code >= 400:
            try:
                detail = str(response.json().get("error", {}).get("message", ""))[:200]
            except (ValueError, AttributeError):
                detail = ""
            logger.warning("llm_rejected", extra={"status": response.status_code, "detail": detail})
            if "reasoning" in payload and "reasoning is mandatory" in detail.lower():
                raise LLMError("reasoning_required", "model requires reasoning to stay enabled")
            raise LLMError("upstream_4xx", f"LLM provider rejected the request ({response.status_code})")
        try:
            data = response.json()
        except ValueError as exc:
            raise LLMError("invalid_response", "LLM response is not JSON") from exc
        # OpenRouter sometimes reports a provider failure inside an HTTP 200 body.
        if isinstance(data, dict) and isinstance(data.get("error"), dict):
            code = data["error"].get("code")
            logger.warning("llm_provider_error", extra={"code": code, "detail": str(data["error"].get("message", ""))[:200]})
            if code == 429:
                raise LLMError("rate_limited", "LLM provider rate limited the request")
            if isinstance(code, int) and code >= 500:
                raise LLMError("upstream_5xx", f"LLM provider error {code}")
            raise LLMError("upstream_4xx", f"LLM provider rejected the request ({code})")
        try:
            message = data["choices"][0]["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError("invalid_response", "LLM response missing choices") from exc
        served_by = str(data.get("model") or "")
        if (settings.llm_free_only and served_by and settings.llm_is_openrouter
                and not is_free_model(served_by) and served_by not in (payload.get("models") or [payload["model"]])):
            # The "openrouter/free" router reports the concrete free model it picked; anything else is unexpected.
            logger.error("llm_unexpected_model", extra={"model": served_by})
            raise LLMError("paid_model_blocked", f"Response came from a non-free model: {served_by}")
        if message.get("refusal"):
            raise LLMError("refusal", "model refused the request")
        return _extract_json(message.get("content") or "")
