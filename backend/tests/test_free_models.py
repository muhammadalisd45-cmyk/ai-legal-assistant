"""Cost guard: only free LLM models may ever be called."""
import asyncio
import json

import httpx
import pytest

from app.core.config import is_free_model, settings
from app.services.llm_client import LLMClient, LLMError


def _client(seen: list):
    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(json.loads(request.content))
        body = {"model": seen[-1]["model"], "choices": [{"message": {"content": '{"ok": true}'}}]}
        return httpx.Response(200, json=body)
    return LLMClient(transport=httpx.MockTransport(handler))


def _configure(monkeypatch, model, fallbacks="", base="https://openrouter.ai/api/v1"):
    monkeypatch.setattr(settings, "llm_api_key", "k")
    monkeypatch.setattr(settings, "llm_model", model)
    monkeypatch.setattr(settings, "llm_fallback_models", fallbacks)
    monkeypatch.setattr(settings, "llm_base_url", base)
    monkeypatch.setattr(settings, "llm_response_format", "json_object")


def _call(client):
    return asyncio.run(client.complete_json("sys", "user", {"type": "object", "properties": {}}))


@pytest.mark.parametrize("model,free", [
    ("google/gemma-4-31b-it:free", True), ("openrouter/free", True),
    ("openai/gpt-5", False), ("anthropic/claude-opus-5-5", False), ("free/model", False),
])
def test_is_free_model(model, free):
    assert is_free_model(model) is free


@pytest.mark.parametrize("model,fallbacks", [("openai/gpt-5", ""), ("a/b:free", "openai/gpt-5")])
def test_paid_model_is_blocked_before_any_request(monkeypatch, model, fallbacks):
    _configure(monkeypatch, model, fallbacks)
    seen: list = []
    with pytest.raises(LLMError) as err:
        _call(_client(seen))
    assert err.value.reason == "paid_model_blocked"
    assert seen == []


def test_openrouter_request_caps_price_and_sends_fallbacks(monkeypatch):
    _configure(monkeypatch, "a/one:free", "b/two:free, a/one:free")
    seen: list = []
    assert _call(_client(seen)) == {"ok": True}
    assert seen[0]["provider"] == {"max_price": {"prompt": 0, "completion": 0}}
    assert seen[0]["models"] == ["a/one:free", "b/two:free"]


def test_response_from_non_free_model_is_rejected(monkeypatch):
    _configure(monkeypatch, "openrouter/free")

    def handler(request):
        return httpx.Response(200, json={"model": "openai/gpt-5", "choices": [{"message": {"content": "{}"}}]})

    with pytest.raises(LLMError) as err:
        _call(LLMClient(transport=httpx.MockTransport(handler)))
    assert err.value.reason == "paid_model_blocked"


def test_openrouter_fallback_list_is_capped_at_three(monkeypatch):
    _configure(monkeypatch, "a/1:free", "b/2:free,c/3:free,d/4:free")
    seen: list = []
    _call(_client(seen))
    assert seen[0]["models"] == ["a/1:free", "b/2:free", "c/3:free"]
    assert seen[0]["reasoning"] == {"enabled": False}


def test_error_inside_http_200_body_is_retried_then_raised(monkeypatch):
    _configure(monkeypatch, "a/1:free")
    monkeypatch.setattr(settings, "llm_max_retries", 1)
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(200, json={"error": {"code": 429, "message": "temporarily rate-limited upstream"}})

    with pytest.raises(LLMError) as err:
        _call(LLMClient(transport=httpx.MockTransport(handler)))
    assert err.value.reason == "rate_limited"
    assert len(calls) == 2
