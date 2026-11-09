"""Post-generation citation guard.

Rules enforced on every model answer:
1. Inline evidence markers must reference evidence actually supplied ([E1]..[En]); others are stripped.
2. Any statutory reference (Section/Article/Rule/Order N) must be supported by the cited evidence (or, for
   sentences without markers, by any supplied evidence). Unsupported sentences are removed.
3. Case-law citations (PLD/SCMR/CLC/YLR/MLD/PCrLJ/PLJ/… or "X v. Y") are removed unless the exact citation text
   appears in the supplied evidence — the corpus currently contains no verified judgments.
4. Quotes attached to citations must appear verbatim (whitespace/case-normalised) in the cited evidence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

_MARKER = re.compile(r"\[\s*E(\d{1,2})\s*\]")
_SENTENCE = re.compile(r"(?<=[.!?۔؟])\s+|\n+")
_STATUTE_REF = re.compile(
    r"\b(?P<kind>sections?|secs?\.?|s\.|articles?|arts?\.?|rules?|orders?|dafa|دفعہ|آرٹیکل)\s*"
    r"(?P<num>\d{1,4}(?:-?(?-i:[A-Z]{1,2})\b)?|(?-i:[IVXLC]{1,7})\b)(?:\s*\((?P<sub>[0-9a-z]{1,3})\))?",
    re.IGNORECASE,
)
_CASE_CITATION = re.compile(
    r"\b(?:PLD|SCMR|CLC|YLR|MLD|PCr\.?LJ|PLJ|PTD|CLD|PLC|NLR|KLR|SBLR|GBLR)\s*\(?\d{4}\)?|"
    r"\b\d{4}\s+(?:PLD|SCMR|CLC|YLR|MLD|PCr\.?LJ|PLJ|PTD|CLD|PLC)\b|"
    r"\b[A-Z][a-zA-Z.&]+(?:\s+[A-Z][a-zA-Z.&]+){0,4}\s+(?:v\.|vs\.?|versus)\s+[A-Z][a-zA-Z.&]+",
)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


def _num_norm(num: str) -> str:
    return re.sub(r"[\s-]", "", num).lower()


@dataclass
class GuardResult:
    answer: str
    cited_ids: list[str]
    removed: list[str] = field(default_factory=list)
    invalid_markers: list[str] = field(default_factory=list)


def ref_supported(kind: str, num: str, evidence: list[dict]) -> bool:
    n = _num_norm(num)
    kind = kind.lower()
    for item in evidence:
        label = _norm(item.get("section_or_article", ""))
        label_num = re.search(r"(?:section|article|rule)\s+([0-9a-z]+)$", label)
        if label_num and label_num.group(1) == n:
            return True
        content = _norm(item.get("content", ""))
        # The provision number appears in the evidence text (e.g. a cross-reference "section 497" or heading "497.").
        if re.search(rf"(?:section|sections|article|rule|order|s\.)\s*{re.escape(n)}\b", content):
            return True
        if re.search(rf"(?:^|\s){re.escape(n)}\.\s", content[:200]):
            return True
        if kind.startswith("order") and f"order {n}" in label:
            return True
    return False


_ABBREVIATIONS = re.compile(r"\b(v|vs|no|nos|s|ss|sec|secs|art|arts|cl|sub|para|e\.g|i\.e|etc|mr|mrs|ms|dr|st|ord|govt)\.",
                            re.IGNORECASE)
_DOT = "․"  # one-dot leader: placeholder so abbreviations do not end a sentence


def split_sentences(text: str) -> list[str]:
    protected = _ABBREVIATIONS.sub(lambda m: m.group(0)[:-1] + _DOT, text or "")
    return [s.replace(_DOT, ".") for s in _SENTENCE.split(protected) if s and s.strip()]


def guard_answer(answer: str, evidence: dict[str, dict]) -> GuardResult:
    """`evidence` maps "E1" → chunk dict (content, section_or_article, …)."""
    result = GuardResult(answer="", cited_ids=[])
    kept: list[str] = []
    for sentence in split_sentences(answer):
        markers = [f"E{m}" for m in _MARKER.findall(sentence)]
        valid = [m for m in markers if m in evidence]
        result.invalid_markers.extend(m for m in markers if m not in evidence)
        clean = _MARKER.sub(lambda m: m.group(0) if f"E{m.group(1)}" in evidence else "", sentence)
        scope = [evidence[m] for m in valid] if valid else list(evidence.values())
        unsupported = False
        for ref in _STATUTE_REF.finditer(clean):
            if not ref_supported(ref.group("kind"), ref.group("num"), scope):
                unsupported = True
                break
        if not unsupported:
            all_text = " ".join(_norm(e.get("content", "")) for e in evidence.values())
            for case in _CASE_CITATION.finditer(clean):
                if _norm(case.group(0)) not in all_text:
                    unsupported = True
                    break
        if unsupported:
            result.removed.append(sentence.strip()[:300])
            continue
        kept.append(re.sub(r"\s{2,}", " ", clean).strip())
        for m in valid:
            if m not in result.cited_ids:
                result.cited_ids.append(m)
    result.answer = " ".join(kept).strip()
    return result


def verify_quote(quote: str, content: str) -> bool:
    q = _norm(quote).strip(" \"'“”…")
    return bool(q) and len(q) >= 12 and q in _norm(content)
