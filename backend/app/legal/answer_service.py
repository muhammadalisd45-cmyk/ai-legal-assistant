"""Grounded legal answers: retrieve → (LLM | extractive) → citation guard → uncertainty messaging."""
from __future__ import annotations

import logging

from pydantic import ValidationError

from app.core.text import detect_language, detect_prompt_injection
from app.legal.citation_guard import guard_answer, verify_quote
from app.legal.search_service import search
from app.prompts.answer_prompt import ANSWER_SYSTEM_PROMPT, ANSWER_USER_TEMPLATE
from app.prompts.triage_prompt import LANGUAGE_NAMES
from app.schemas.answer import AnswerLLMOutput, AnswerRequest, AnswerResponse, Citation
from app.schemas.search import SearchRequest, SearchResult
from app.schemas.triage import Language, Warning
from app.services.llm_client import LLMClient, LLMError

logger = logging.getLogger("pjn.answer")

TEXT = {
    "no_evidence": {
        "english": "I could not find official legal text in the current corpus that addresses this question, so I will "
                   "not guess. Please consult a qualified lawyer or your district legal-aid authority.",
        "roman_urdu": "Mojooda corpus mein is sawal se mutaliq koi sarkari qanooni matan nahi mila, is liye main andaza "
                      "nahi lagaunga. Barah-e-karam kisi mustanad wakeel ya zila legal aid authority se rabta karein.",
        "urdu": "موجودہ ذخیرے میں اس سوال سے متعلق کوئی سرکاری قانونی متن نہیں ملا، اس لیے میں اندازہ نہیں لگاؤں گا۔ "
                "براہ کرم کسی مستند وکیل یا ضلعی لیگل ایڈ اتھارٹی سے رابطہ کریں۔",
    },
    "no_evidence_uncertainty": {
        "english": "No retrieved official provision supports an answer. Documents listed (if any) are metadata-only "
                   "pointers and have not been checked for an exact provision.",
        "roman_urdu": "Koi hasil shuda sarkari shiq jawab ki tasdeeq nahi karti. Darj documents (agar hain) sirf metadata "
                      "hain, un mein kisi makhsoos shiq ki tasdeeq nahi hui.",
        "urdu": "کوئی حاصل شدہ سرکاری شق جواب کی تصدیق نہیں کرتی۔ درج دستاویزات (اگر ہیں) صرف میٹا ڈیٹا ہیں۔",
    },
    "extractive_intro": {
        "english": "These official provisions were retrieved for your question. They are quoted, not interpreted:",
        "roman_urdu": "Aap ke sawal ke liye yeh sarkari qanooni shiqein mili hain. Inhein naql kiya gaya hai, in ki tashreeh nahi ki gayi:",
        "urdu": "آپ کے سوال کے لیے یہ سرکاری قانونی شقیں ملی ہیں۔ انہیں نقل کیا گیا ہے، ان کی تشریح نہیں کی گئی:",
    },
    "extractive_uncertainty": {
        "english": "AI explanation is unavailable right now, so only retrieved text is shown. Whether these provisions "
                   "apply to your situation needs review by a qualified lawyer.",
        "roman_urdu": "AI wazahat is waqt dastiyab nahi, is liye sirf hasil shuda matan dikhaya gaya hai. Kya yeh shiqein "
                      "aap ke maamle par lagu hoti hain, iska faisla mustanad wakeel karega.",
        "urdu": "اے آئی وضاحت اس وقت دستیاب نہیں، اس لیے صرف حاصل شدہ متن دکھایا گیا ہے۔ یہ شقیں آپ کے معاملے پر لاگو ہوتی ہیں یا نہیں، اس کا جائزہ مستند وکیل لے گا۔",
    },
    "guard_removed": {
        "english": "Some generated statements were removed because they cited law not found in the retrieved official text.",
        "roman_urdu": "Kuch jumlay hata diye gaye kyun ke un mein aisa qanoon bataya gaya jo hasil shuda sarkari matan mein nahi tha.",
        "urdu": "کچھ جملے ہٹا دیے گئے کیونکہ ان میں ایسے قانون کا حوالہ تھا جو حاصل شدہ سرکاری متن میں موجود نہیں تھا۔",
    },
}


def _escape(text: str) -> str:
    return (text or "").replace("<", "‹").replace(">", "›")


def _evidence_blocks(evidence: dict[str, SearchResult], contents: dict[str, str]) -> str:
    blocks = []
    for eid, item in evidence.items():
        header = f'id="{eid}" document="{_escape(item.title)}" provision="{_escape(item.section_or_article or "unlabelled")}" pages="{item.page_reference}"'
        blocks.append(f"<evidence {header}>\n{_escape(contents[eid])}\n</evidence>")
    return "\n\n".join(blocks)


def _citation(eid: str, item: SearchResult, quote: str = "", verified: bool = False) -> Citation:
    return Citation(evidence_id=eid, chunk_id=item.chunk_id, document_id=item.document_id, title=item.title,
                    section_or_article=item.section_or_article, page_reference=item.page_reference,
                    page_url=item.provenance.page_url if item.provenance else "", source_url=item.source_url,
                    quote=quote, quote_verified=verified)


class AnswerService:
    def __init__(self, llm: LLMClient | None = None):
        self.llm = llm or LLMClient()

    async def answer(self, request: AnswerRequest, request_id: str = "") -> AnswerResponse:
        detected = detect_language(request.question)
        lang = detected if request.language == Language.auto else request.language.value
        warnings: list[Warning] = []
        if detect_prompt_injection(request.question):
            warnings.append(Warning(code="instructions_ignored", severity="info",
                                    message="Parts of the question looked like instructions to the AI system. They were treated as question text only."))

        found = await search(SearchRequest(query=request.question, limit=request.limit, filters=request.filters),
                             request_id)
        # Only strong matches count as evidence; weak lexical overlaps (e.g. "income" in a tax article for a crypto
        # question) must not be presented as the applicable law.
        chunks = [r for r in found.results
                  if r.evidence_level == "chunk" and r.relevance is not None and r.relevance.strong_match]
        if not chunks:
            weak = any(r.evidence_level == "chunk" for r in found.results)
            return AnswerResponse(
                answer=TEXT["no_evidence"][lang], mode="no_evidence", grounded=False, language=lang,
                detected_language=detected, uncertainty=TEXT["no_evidence_uncertainty"][lang], needs_lawyer=True,
                warnings=warnings + [Warning(code="no_evidence", severity="warning",
                                             message=("Only weak, possibly unrelated provisions were found; they are listed "
                                                      "as leads, not as the answer.") if weak else
                                             "No official legal text was retrieved for this question.")],
                evidence=found.results, search_mode=found.mode,
                fallback_reason="weak_matches_only" if weak else (found.fallback_reason or "no_evidence"),
                request_id=request_id)

        evidence = {f"E{i}": item for i, item in enumerate(chunks, start=1)}
        contents = self._full_contents(evidence)
        try:
            return await self._live(request, lang, detected, evidence, contents, warnings, found.mode, request_id)
        except LLMError as exc:
            reason = exc.reason
        except (ValidationError, ValueError, KeyError, TypeError):
            reason = "invalid_model_output"
        except Exception:  # noqa: BLE001
            logger.exception("answer_unexpected_error", extra={"request_id": request_id})
            reason = "unexpected_error"
        if reason != "not_configured":
            logger.warning("answer_llm_fallback", extra={"reason": reason, "request_id": request_id})
        return self._extractive(lang, detected, evidence, warnings, found.mode, reason, request_id)

    @staticmethod
    def _full_contents(evidence: dict[str, SearchResult]) -> dict[str, str]:
        from app.core.index_state import local_index

        index, _ = local_index()
        by_id = {c.get("chunk_id"): c for c in index.chunks} if index.size else {}
        return {eid: (by_id.get(item.chunk_id) or {}).get("content") or item.snippet for eid, item in evidence.items()}

    async def _live(self, request, lang, detected, evidence, contents, warnings, search_mode, request_id) -> AnswerResponse:
        prompt = ANSWER_USER_TEMPLATE.format(language_name=LANGUAGE_NAMES[lang], question=_escape(request.question),
                                             evidence_blocks=_evidence_blocks(evidence, contents))
        raw = await self.llm.complete_json(ANSWER_SYSTEM_PROMPT, prompt, AnswerLLMOutput.model_json_schema(),
                                           schema_name="grounded_legal_answer")
        out = AnswerLLMOutput.model_validate(raw)
        guard_input = {eid: {"content": contents[eid], "section_or_article": item.section_or_article}
                       for eid, item in evidence.items()}
        guarded = guard_answer(out.answer, guard_input)

        citations: list[Citation] = []
        seen: set[str] = set()
        for cit in out.citations:
            if cit.evidence_id in evidence and cit.evidence_id not in seen:
                verified = verify_quote(cit.quote, contents[cit.evidence_id])
                citations.append(_citation(cit.evidence_id, evidence[cit.evidence_id], cit.quote if verified else "", verified))
                seen.add(cit.evidence_id)
        for eid in guarded.cited_ids:
            if eid not in seen:
                citations.append(_citation(eid, evidence[eid]))
                seen.add(eid)

        if guarded.removed:
            warnings.append(Warning(code="unsupported_claims_removed", severity="warning", message=TEXT["guard_removed"][lang]))
        if not guarded.answer or not guarded.cited_ids:
            # Nothing grounded survived: never return an uncited explanation.
            response = self._extractive(lang, detected, evidence, warnings, search_mode, "ungrounded_model_answer", request_id)
            response.unsupported_claims_removed = guarded.removed
            return response
        uncertainty = out.uncertainty.strip()
        if out.insufficient_evidence and not uncertainty:
            uncertainty = TEXT["no_evidence_uncertainty"][lang]
        return AnswerResponse(
            answer=guarded.answer, mode="live", grounded=True, language=lang, detected_language=detected,
            citations=citations, uncertainty=uncertainty, needs_lawyer=out.needs_lawyer or out.insufficient_evidence,
            unsupported_claims_removed=guarded.removed, warnings=warnings, evidence=list(evidence.values()),
            search_mode=search_mode, request_id=request_id)

    @staticmethod
    def _extractive(lang, detected, evidence, warnings, search_mode, reason, request_id) -> AnswerResponse:
        lines = [TEXT["extractive_intro"][lang]]
        citations = []
        for eid, item in list(evidence.items())[:4]:
            label = ", ".join(part for part in (item.title, item.section_or_article, item.page_reference) if part)
            quote = item.snippet[:320].rstrip() + ("…" if len(item.snippet) > 320 else "")
            lines.append(f"• {label}: \"{quote}\" [{eid}]")
            citations.append(_citation(eid, item, item.snippet[:320], True))
        return AnswerResponse(
            answer="\n".join(lines), mode="extractive_fallback", grounded=True, language=lang, detected_language=detected,
            citations=citations, uncertainty=TEXT["extractive_uncertainty"][lang], needs_lawyer=True,
            warnings=warnings, evidence=list(evidence.values()), search_mode=search_mode, fallback_reason=reason,
            request_id=request_id)
