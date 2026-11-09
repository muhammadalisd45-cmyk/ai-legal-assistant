from __future__ import annotations

import json
import logging

from pydantic import ValidationError

from app.core.text import detect_language, detect_prompt_injection
from app.prompts.triage_prompt import LANGUAGE_NAMES, SYSTEM_PROMPT, USER_TEMPLATE
from app.schemas.triage import (
    DISCLAIMER, Language, TriageLLMOutput, TriageRequest, TriageResult, Urgency, Warning,
)
from app.services.fallback import deterministic_fallback
from app.services.llm_client import LLMClient, LLMError
from app.services.urgency import EMERGENCY_GUIDANCE, apply_floor, detect_urgency_indicators

logger = logging.getLogger("pjn.triage")


def _escape_tags(text: str) -> str:
    # Prevent user text from closing our delimiting tags.
    return text.replace("<", "‹").replace(">", "›")


class TriageService:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    @staticmethod
    def resolve_languages(request: TriageRequest) -> tuple[str, str]:
        detected = detect_language(request.message)
        response = detected if request.language == Language.auto else request.language.value
        return detected, response

    async def analyze(self, request: TriageRequest, request_id: str = "") -> TriageResult:
        detected, response_lang = self.resolve_languages(request)
        answers = [a.answer for a in request.answers]
        injection = detect_prompt_injection(" ".join([request.message, *answers]))
        indicators = detect_urgency_indicators(" ".join([request.message, *request.known_facts, *answers]))
        # Clarification answers reach the model as citizen-supplied facts (question — answer).
        known_facts = [*request.known_facts, *(a.as_fact() for a in request.answers)]

        prompt = USER_TEMPLATE.format(
            language_name=LANGUAGE_NAMES[response_lang],
            detected_language=detected,
            message=_escape_tags(request.message),
            known_facts=_escape_tags(json.dumps(known_facts, ensure_ascii=False)),
            documents=_escape_tags(json.dumps(request.documents, ensure_ascii=False)[:8000]),
            timeline=_escape_tags(json.dumps(request.timeline, ensure_ascii=False)[:4000]),
            legal_sources=_escape_tags(json.dumps(request.legal_sources, ensure_ascii=False)[:12000]),
        )

        try:
            raw = await self.llm.complete_json(SYSTEM_PROMPT, prompt, TriageLLMOutput.model_json_schema())
            llm_output = TriageLLMOutput.model_validate(raw)
            result = TriageResult(**llm_output.model_dump(), mode="live")
        except LLMError as exc:
            if exc.reason != "not_configured":
                logger.warning("triage_llm_failed", extra={"reason": exc.reason, "request_id": request_id})
            result = deterministic_fallback(request, response_lang, detected, reason=exc.reason)
        except (ValidationError, ValueError, KeyError, TypeError):
            logger.warning("triage_llm_invalid_output", extra={"request_id": request_id})
            result = deterministic_fallback(request, response_lang, detected, reason="invalid_model_output")
        except Exception:  # noqa: BLE001 — availability: any LLM-path failure degrades to the fallback
            logger.exception("triage_llm_unexpected_error", extra={"request_id": request_id})
            result = deterministic_fallback(request, response_lang, detected, reason="unexpected_error")

        result.detected_language = detected  # type: ignore[assignment]
        result.response_language = response_lang  # type: ignore[assignment]
        result.request_id = request_id
        self._enforce_source_boundary(result, request)
        self._apply_urgency_floor(result, indicators, response_lang)
        if injection and not any(w.code == "instructions_ignored" for w in result.warnings):
            result.warnings.append(Warning(
                code="instructions_ignored",
                message="Parts of the message looked like instructions to the AI system. They were treated as case text only.",
                severity="info",
            ))
        result.disclaimer = DISCLAIMER
        return result

    @staticmethod
    def _enforce_source_boundary(result: TriageResult, request: TriageRequest) -> None:
        allowed = {str(source.get("id")) for source in request.legal_sources if source.get("id") is not None}
        result.source_ids_used = [sid for sid in dict.fromkeys(result.source_ids_used) if sid in allowed]

    @staticmethod
    def _apply_urgency_floor(result: TriageResult, indicators, response_lang: str) -> None:
        merged = {ind.code: ind for ind in result.urgency_indicators}
        for ind in indicators:
            merged.setdefault(ind.code, ind)
        result.urgency_indicators = list(merged.values())
        result.urgency = apply_floor(result.urgency, result.urgency_indicators)
        if result.urgency == Urgency.critical and not any(w.code == "emergency_contacts" for w in result.warnings):
            result.warnings.insert(0, Warning(code="emergency_contacts", message=EMERGENCY_GUIDANCE[response_lang],
                                              severity="urgent"))
