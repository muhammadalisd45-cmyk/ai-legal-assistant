"""Rule-based urgency indicators (English, Roman Urdu, Urdu).

These signal *intake priority* only — never a legal finding. The server applies the strongest
rule-based level as a floor so a model can never down-rank an apparent emergency.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.text import normalize_for_matching
from app.schemas.triage import URGENCY_RANK, Urgency, UrgencyIndicator


@dataclass(frozen=True)
class Rule:
    code: str
    label: str
    level: Urgency
    patterns: tuple[str, ...]


RULES: tuple[Rule, ...] = (
    Rule("self_harm_risk", "Possible risk to life or self-harm", Urgency.critical, (
        r"\bsuicid\w*", r"\bkill (myself|herself|himself)\b", r"\bend my life\b", r"\bkhudkushi\b",
        r"خودکشی", r"\bjaan (de|le) (dun|doon|lunga|lungi)\b",
    )),
    Rule("violence_or_threat_to_life", "Violence or threat to life or safety", Urgency.critical, (
        r"\b(threat\w* to kill|kill me|kill us|going to kill|murder\w*)\b", r"\bjaan se maar\w*",
        r"\bmaar (dalenge|dalega|denge|dega)\b", r"\bqatl\b", r"جان سے مار", r"قتل",
        r"\b(beat|beating|beaten|assault\w*|attack\w*|stabb\w*|shot|acid)\b", r"\bmaarpeet\b",
        r"\bmaar (raha|rahi|rahe|ta|ti|te)\b", r"مار پیٹ", r"تشدد", r"\btashaddud\b",
    )),
    Rule("domestic_violence", "Possible domestic violence", Urgency.critical, (
        r"\bdomestic (violence|abuse)\b", r"\b(husband|shohar|sasural|in-laws)\b.{0,40}\b(beat\w*|hit\w*|maar\w*|abuse\w*)",
        r"گھریلو تشدد",
    )),
    Rule("unlawful_detention", "Arrest, custody or detention", Urgency.critical, (
        r"\b(arrest\w*|detain\w*|custody|abduct\w*|kidnap\w*|missing person|picked up by)\b",
        r"\bgiraftar\w*", r"\bhirasat\b", r"\butha (liya|le gaye|kar le gaye)\b", r"\baghwa\b",
        r"گرفتار", r"حراست", r"اغوا", r"اٹھا کر لے گئے",
    )),
    Rule("child_at_risk", "A child may be at risk", Urgency.critical, (
        r"\bchild (marriage|abuse|labou?r)\b", r"\bunderage marriage\b", r"\bkam umar\w* (ki )?shadi\b",
        r"کم عمری کی شادی",
    )),
    Rule("imminent_hearing_or_deadline", "Hearing, deadline or action is imminent", Urgency.high, (
        r"\bwithin (24|48|72) hours\b",
        r"\b(hearing|peshi|deadline|last date|summons?|notice|court date|vacate)\b.{0,40}\b(tomorrow|tonight|today|kal|aaj|this week|\d+ (days?|din))\b",
        r"\b(tomorrow|tonight|today|this week)\b.{0,40}\b(hearing|court|deadline|evict\w*|vacate|summons?)\b",
        r"\b(kal|aaj|parson)\b.{0,30}\b(peshi|tareekh|sunwai|court|adalat|hearing)\b",
        r"\b\d+\s*(days?|din)\b.{0,30}\b(notice|mohlat|deadline|left|baqi|bache)\b",
        r"(آج|کل|پرسوں).{0,25}(پیشی|سماعت|عدالت|تاریخ)", r"(پیشی|سماعت).{0,25}(آج|کل)",
        r"\d+\s*دن.{0,20}مہلت", r"مہلت.{0,20}\d+\s*دن",
    )),
    Rule("eviction_or_dispossession", "Eviction or loss of possession under way", Urgency.high, (
        r"\b(evict\w*|thrown out|forcibly removed|lock\w* (me )?out|demolish\w*|bulldoz\w*)\b",
        r"\bghar (se )?(khali|nikal)\w*", r"\bnikal (diya|dia|rahe|denge)\b", r"\bqabza (kar|ho) (liya|raha|gaya)\b",
        r"بے دخل", r"گھر خالی", r"قبضہ کر لیا", r"مسمار",
    )),
    Rule("threat_or_intimidation", "Threats or intimidation reported", Urgency.high, (
        r"\b(threat\w*|intimidat\w*|blackmail\w*|extort\w*)\b", r"\bdhamki\b", r"\bblackmail\b",
        r"دھمکی", r"بلیک میل",
    )),
    Rule("harassment", "Harassment reported", Urgency.medium, (
        r"\bharass\w*\b", r"\bharassment\b", r"\bstalk\w*", r"ہراس", r"\bpareshan kar\w*",
    )),
    Rule("loss_of_income", "Loss of livelihood or unpaid wages", Urgency.medium, (
        r"\b(fired|terminated|dismissed|unpaid (salary|wages)|salary not paid)\b",
        r"\btankhwa\b.{0,20}\b(nahi|nahin|rok)\w*", r"\bnaukri se nikal\w*", r"تنخواہ", r"نوکری سے نکال",
    )),
)

_COMPILED = [(rule, [re.compile(p, re.IGNORECASE) for p in rule.patterns]) for rule in RULES]


def detect_urgency_indicators(text: str) -> list[UrgencyIndicator]:
    haystack = normalize_for_matching(text)
    found: list[UrgencyIndicator] = []
    for rule, patterns in _COMPILED:
        for pattern in patterns:
            match = pattern.search(haystack)
            if match:
                found.append(UrgencyIndicator(code=rule.code, label=rule.label, level=rule.level,
                                              matched=match.group(0)[:60]))
                break
    return found


def strongest(indicators: list[UrgencyIndicator]) -> Urgency:
    level = Urgency.unknown
    for indicator in indicators:
        if URGENCY_RANK[indicator.level] > URGENCY_RANK[level]:
            level = indicator.level
    return level


def apply_floor(current: Urgency, indicators: list[UrgencyIndicator]) -> Urgency:
    floor = strongest(indicators)
    return floor if URGENCY_RANK[floor] > URGENCY_RANK[current] else current


EMERGENCY_GUIDANCE = {
    "english": "If anyone is in immediate danger, contact Police 15 or Rescue 1122 now. "
               "This service cannot dispatch help.",
    "roman_urdu": "Agar kisi ki jaan ya hifazat ko foran khatra hai to abhi Police 15 ya Rescue 1122 par rabta karein. "
                  "Yeh service madad nahi bhej sakti.",
    "urdu": "اگر کسی کی جان یا حفاظت کو فوری خطرہ ہے تو ابھی پولیس 15 یا ریسکیو 1122 سے رابطہ کریں۔ "
            "یہ سروس مدد نہیں بھیج سکتی۔",
}
