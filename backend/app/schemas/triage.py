from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.text import sanitize_text


class Language(str, Enum):
    english = "english"
    urdu = "urdu"
    roman_urdu = "roman_urdu"
    auto = "auto"


class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"
    unknown = "unknown"


URGENCY_RANK = {Urgency.unknown: 0, Urgency.low: 1, Urgency.medium: 2, Urgency.high: 3, Urgency.critical: 4}


class FollowUpQuestion(BaseModel):
    id: str
    question: str
    reason: str = ""
    priority: Literal["high", "medium", "low"] = "medium"


class LegalIssue(BaseModel):
    issue: str
    explanation: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class Pathway(BaseModel):
    title: str
    description: str
    prerequisites: list[str] = Field(default_factory=list)
    caution: str = ""


class Warning(BaseModel):
    code: str
    message: str
    severity: Literal["info", "warning", "urgent"] = "warning"


class UrgencyIndicator(BaseModel):
    code: str
    label: str
    level: Urgency
    matched: str = ""


class ClarificationAnswer(BaseModel):
    """The citizen's answer to a follow-up question from an earlier triage round."""
    model_config = ConfigDict(extra="forbid")
    question_id: str = Field(min_length=1, max_length=80)
    question: str = Field(default="", max_length=500)
    answer: str = Field(min_length=1, max_length=2000)

    @field_validator("question", "answer")
    @classmethod
    def _clean(cls, value: str) -> str:
        return sanitize_text(value)

    def as_fact(self) -> str:
        return f"{self.question or self.question_id} — {self.answer}"


class TriageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str = Field(min_length=1, max_length=12000)
    language: Language = Language.english
    answers: list[ClarificationAnswer] = Field(default_factory=list, max_length=20)
    known_facts: list[str] = Field(default_factory=list, max_length=50)
    documents: list[dict] = Field(default_factory=list, max_length=30)
    timeline: list[dict] = Field(default_factory=list, max_length=100)
    legal_sources: list[dict] = Field(default_factory=list, max_length=50)

    @field_validator("message")
    @classmethod
    def _clean_message(cls, value: str) -> str:
        clean = sanitize_text(value)
        if not clean:
            raise ValueError("message must contain visible text")
        return clean

    @field_validator("known_facts")
    @classmethod
    def _clean_facts(cls, value: list[str]) -> list[str]:
        return [sanitize_text(item, 1000) for item in value if sanitize_text(item)]


class TriageLLMOutput(BaseModel):
    """The part of the result the language model is asked to produce."""
    model_config = ConfigDict(extra="forbid")
    category: str
    subcategory: str = ""
    summary: str
    issues: list[LegalIssue] = Field(default_factory=list)
    urgency: Urgency
    facts: list[str] = Field(default_factory=list)
    missing_facts: list[str] = Field(default_factory=list)
    follow_up_questions: list[FollowUpQuestion] = Field(default_factory=list)
    possible_pathways: list[Pathway] = Field(default_factory=list)
    warnings: list[Warning] = Field(default_factory=list)
    source_ids_used: list[str] = Field(default_factory=list)


DISCLAIMER = (
    "This is an AI-generated intake/triage summary, not a legal opinion. "
    "Verify important facts, deadlines and legal sources with a qualified "
    "lawyer or the relevant authority."
)


class TriageResult(TriageLLMOutput):
    model_config = ConfigDict(extra="forbid")
    mode: Literal["live", "deterministic_fallback"] = "live"
    detected_language: Literal["english", "urdu", "roman_urdu"] = "english"
    response_language: Literal["english", "urdu", "roman_urdu"] = "english"
    urgency_indicators: list[UrgencyIndicator] = Field(default_factory=list)
    urgency_note: str = (
        "Urgency is an intake priority based on apparent time-sensitivity or risk. "
        "It is not a legal assessment."
    )
    fallback_reason: str = ""
    request_id: str = ""
    disclaimer: str = DISCLAIMER
