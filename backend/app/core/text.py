"""Multilingual text utilities: language detection, Roman-Urdu normalisation, legal-term bridging,
control-character sanitisation and prompt-injection heuristics."""
from __future__ import annotations

import re
import unicodedata

# Arabic-script blocks used for Urdu.
_URDU_CHAR = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")
_LATIN_CHAR = re.compile(r"[A-Za-z]")
_WORD = re.compile(r"[a-z]+")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f​-‏‪-‮⁦-⁩]")

# High-frequency Roman-Urdu function words that are rare in English text.
_ROMAN_URDU_MARKERS = {
    "hai", "hain", "hy", "he", "ka", "ki", "ke", "ko", "ne", "se", "mein", "main", "mai", "mera", "meri",
    "mere", "hum", "hamara", "hamari", "hamare", "aap", "ap", "kya", "kyun", "nahi", "nahin", "ye", "yeh",
    "wo", "woh", "tha", "thi", "the", "raha", "rahi", "rahe", "gaya", "gayi", "kar", "kiya", "kiye", "diya",
    "liya", "lia", "par", "pe", "bhi", "aur", "magar", "lekin", "abhi", "kal", "chahiye", "sakta", "sakti",
    "karna", "karta", "karti", "wala", "wali", "unhon", "unho", "usne", "mujhe", "humein", "hamein", "apna",
    "apni", "ghar", "bhai", "behan", "chacha", "walid", "shohar", "biwi",
}
# "the", "he", "main" also occur in English; they need company to count.
_AMBIGUOUS = {"the", "he", "main", "par", "ye", "wo"}

# Roman-Urdu spelling variants → canonical form (applied token-wise).
ROMAN_URDU_CANON = {
    "kabza": "qabza", "qabzah": "qabza", "kabzah": "qabza", "qbza": "qabza",
    "zamin": "zameen", "zamen": "zameen", "zmeen": "zameen",
    "talak": "talaq", "tlaq": "talaq", "talaaq": "talaq",
    "khulla": "khula", "khulaa": "khula",
    "kiraya": "kiraya", "kiraaya": "kiraya", "kirayah": "kiraya", "krayah": "kiraya",
    "kirayedar": "kirayedar", "kirayadar": "kirayedar", "kiraydar": "kirayedar",
    "wirasat": "virasat", "warasat": "virasat", "virasut": "virasat", "wirasut": "virasat",
    "giraftar": "giraftar", "griftar": "giraftar", "giraftaar": "giraftar",
    "giraftari": "giraftari", "griftari": "giraftari", "giraftaari": "giraftari",
    "zamanat": "zamanat", "zmanat": "zamanat", "zamaanat": "zamanat",
    "thana": "thana", "thaana": "thana", "thane": "thana",
    "tankhwah": "tankhwa", "tankhwa": "tankhwa", "tankhah": "tankhwa", "tankha": "tankhwa",
    "naukri": "naukri", "nokri": "naukri", "noukri": "naukri",
    "dhamki": "dhamki", "dhamkee": "dhamki", "dhamkiyan": "dhamki", "dhamkiyaan": "dhamki",
    "maar": "maar", "mar": "maar", "maarpeet": "maarpeet", "marpeet": "maarpeet", "maar-peet": "maarpeet",
    "harrasment": "harassment", "harasment": "harassment", "harrassment": "harassment",
    "nafqa": "nafqa", "nafaqa": "nafqa", "nafka": "nafqa",
    "jaidad": "jaidad", "jaydad": "jaidad", "jayedad": "jaidad",
    "adalat": "adalat", "adaalat": "adalat", "court": "court",
    "wakeel": "wakeel", "vakeel": "wakeel", "wakil": "wakeel", "vakil": "wakeel",
    "nikah": "nikah", "nikkah": "nikah", "nikaah": "nikah",
    "bachon": "bachay", "bachay": "bachay", "bache": "bachay", "bachche": "bachay",
    "hirasat": "hirasat", "hiraasat": "hirasat",
}

# Roman-Urdu / Urdu → English legal vocabulary for lexical retrieval over the English corpus.
LEGAL_BRIDGE = {
    # property / inheritance
    "qabza": ["possession", "dispossessed", "immovable", "property", "specific relief"],
    "zameen": ["land", "immovable", "property"], "jaidad": ["property", "immovable"],
    "ghar": ["house", "premises", "property"], "makaan": ["house", "premises"],
    "virasat": ["inheritance", "succession", "heirs", "property"], "waris": ["heirs", "inheritance", "succession"],
    "registry": ["registration", "registered", "document"], "intiqal": ["mutation", "transfer", "property"],
    # tenancy
    "kiraya": ["rent", "tenant", "premises", "lease"], "kirayedar": ["tenant", "rent", "lease", "premises"],
    "khali": ["eviction", "ejectment", "vacate"], "beydakhli": ["eviction", "ejectment", "dispossessed"],
    # criminal
    "fir": ["first information", "police", "cognizable", "information"],
    "giraftar": ["arrest", "custody", "detention"], "giraftari": ["arrest", "custody", "detention"],
    "zamanat": ["bail", "bond", "surety"], "thana": ["police station", "officer in charge", "police"],
    "police": ["police", "officer", "investigation"], "hirasat": ["custody", "detention", "arrest"],
    "chori": ["theft", "dishonestly", "movable property"], "dhoka": ["cheating", "fraud", "dishonestly"],
    "qatl": ["murder", "qatl", "homicide"], "maar": ["hurt", "assault", "force"], "maarpeet": ["hurt", "assault"],
    "dhamki": ["criminal intimidation", "threat", "intimidation"],
    "churaya": ["theft", "dishonestly", "movable property"], "cheena": ["robbery", "theft"],
    "chheena": ["robbery", "theft"], "dakaiti": ["dacoity", "robbery"], "daketi": ["dacoity", "robbery"],
    # Colloquial / misspelled English → the statute's vocabulary ("robbed my laptop" → robbery, theft).
    "stolen": ["theft", "dishonestly", "movable property"], "stole": ["theft", "dishonestly", "movable property"],
    "steal": ["theft", "dishonestly"], "thief": ["theft", "dishonestly"], "theif": ["theft", "dishonestly"],
    "thieves": ["theft", "dishonestly"], "robbed": ["robbery", "theft"], "rob": ["robbery", "theft"],
    "robber": ["robbery", "theft"], "snatched": ["robbery", "theft"], "snatching": ["robbery", "theft"],
    "mugged": ["robbery", "theft"], "pickpocket": ["theft"], "burglary": ["house-breaking", "theft"],
    # family
    "talaq": ["divorce", "talaq", "dissolution of marriage"], "khula": ["khula", "dissolution of marriage", "divorce"],
    "nikah": ["marriage", "nikah"], "nafqa": ["maintenance", "wife", "children"],
    "bachay": ["children", "minor", "custody", "guardian"], "shohar": ["husband", "wife", "marriage"],
    "jahez": ["dowry", "marriage"], "haq mehr": ["dower", "mehr"],
    # employment / workplace
    "naukri": ["employment", "employee", "employer", "service"], "tankhwa": ["wages", "salary", "payment"],
    "harassment": ["harassment", "workplace", "inquiry committee", "complaint"],
    # courts / general
    "adalat": ["court", "suit", "proceedings"], "wakeel": ["advocate", "legal practitioner", "counsel"],
    # Not "case": in English and Roman Urdu it is used for criminal matters too ("theft case"), and mapping it to
    # "suit" pulled civil-procedure rules into criminal searches.
    "muqadma": ["suit", "case", "proceedings"],
    "haq": ["right", "rights"], "huqooq": ["rights", "fundamental rights"], "insaf": ["justice", "fair trial"],
    "muft": ["free", "legal aid"], "qanooni madad": ["legal aid"],
    "saza": ["punishment", "punished", "imprisonment"], "jurm": ["offence", "offender"],
    "jurmana": ["fine"], "qaid": ["imprisonment"], "shikayat": ["complaint", "complainant"],
    "daftar": ["workplace", "office", "employer"], "aurat": ["women", "woman", "female"],
    "mehroom": ["deprive", "depriving"], "na-qabil-e-zamanat": ["non-bailable", "bail"],
    "qabil-e-zamanat": ["bailable", "bail"], "gawah": ["witness", "evidence"], "saboot": ["evidence", "proof"],
    "faisla": ["judgment", "decree", "order"], "appeal": ["appeal"], "apeel": ["appeal"],
    "nabaligh": ["minor", "juvenile", "child"], "bacha": ["child", "juvenile", "minor"],
    "maarne": ["kill", "death", "hurt"], "jaan": ["life", "death"], "darj": ["registered", "recorded", "lodged"],
    "mukhbir": ["informant", "information"], "hukm": ["order", "injunction"], "stay": ["injunction", "temporary injunction"],
    "muddat": ["period", "limitation", "time"], "miyad": ["limitation", "period"],
}

URDU_BRIDGE = {
    "قبضہ": ["possession", "dispossessed", "property"], "زمین": ["land", "immovable", "property"],
    "جائیداد": ["property", "immovable"], "مکان": ["house", "premises"], "گھر": ["house", "premises"],
    "وراثت": ["inheritance", "succession", "heirs"], "وارث": ["heirs", "inheritance"],
    "کرایہ": ["rent", "tenant", "premises"], "کرایہ دار": ["tenant", "rent", "lease"],
    "بے دخلی": ["eviction", "ejectment"], "خالی": ["vacate", "eviction"],
    "ایف آئی آر": ["first information", "police"], "پولیس": ["police", "officer"], "تھانہ": ["police station", "police"],
    "گرفتار": ["arrest", "custody"], "گرفتاری": ["arrest", "custody", "detention"], "ضمانت": ["bail", "bond", "surety"],
    "حراست": ["custody", "detention"], "چوری": ["theft", "dishonestly"], "دھوکہ": ["cheating", "fraud"],
    "چور": ["theft", "dishonestly"], "چھین": ["robbery", "theft"], "ڈکیتی": ["dacoity", "robbery"],
    "قتل": ["murder", "qatl"], "مار پیٹ": ["hurt", "assault"], "دھمکی": ["criminal intimidation", "threat"],
    "طلاق": ["divorce", "talaq"], "خلع": ["khula", "dissolution of marriage"], "نکاح": ["marriage", "nikah"],
    "نان نفقہ": ["maintenance"], "نفقہ": ["maintenance"], "بچوں": ["children", "custody", "guardian"],
    "شوہر": ["husband", "marriage"], "جہیز": ["dowry"], "حق مہر": ["dower", "mehr"],
    "نوکری": ["employment", "employee"], "تنخواہ": ["wages", "salary"], "ہراسانی": ["harassment", "workplace"],
    "ہراساں": ["harassment"], "عدالت": ["court", "suit"], "وکیل": ["advocate", "legal practitioner"],
    "مقدمہ": ["suit", "case", "proceedings"], "حقوق": ["rights", "fundamental rights"], "آئین": ["constitution"],
    "قانونی امداد": ["legal aid"], "معاہدہ": ["contract", "agreement"], "ملازمت": ["employment", "service"],
    "سزا": ["punishment", "punished", "imprisonment"], "جرم": ["offence"], "جرمانہ": ["fine"], "قید": ["imprisonment"],
    "شکایت": ["complaint", "complainant"], "دفتر": ["workplace", "office"], "عورت": ["women", "woman"],
    "خواتین": ["women"], "محروم": ["deprive", "depriving"], "ناجائز": ["unlawful", "without consent"],
    "مفت": ["free", "legal aid"], "گواہ": ["witness"], "ثبوت": ["evidence", "proof"], "فیصلہ": ["judgment", "decree"],
    "اپیل": ["appeal"], "مارنے": ["kill", "death"], "جان": ["life", "death"], "درج": ["registered", "recorded"],
    "حکم امتناعی": ["temporary injunction", "injunction"], "مدت": ["period", "limitation"],
}

INJECTION_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"ignore\s+(all\s+|any\s+|the\s+)?(previous|prior|above|earlier)\s+(instructions|prompts?|rules)",
        r"disregard\s+(all\s+|the\s+)?(previous|prior|above|system)",
        r"forget\s+(all\s+|your\s+)?(previous\s+)?(instructions|rules)",
        r"(reveal|show|print|repeat|output)\s+(me\s+)?(your|the)\s+(system\s+)?(prompt|instructions|rules)",
        r"you\s+are\s+now\s+(a|an|in)\b",
        r"\b(developer|dan|jailbreak|god)\s+mode\b",
        r"act\s+as\s+(an?\s+)?(unrestricted|unfiltered|different)",
        r"<\s*/?\s*(system|assistant|instructions?)\s*>",
        r"^\s*(system|assistant)\s*:",
        r"\[\s*(system|inst)\s*\]",
        r"new\s+instructions?\s*:",
        r"override\s+(the\s+)?(rules|safety|guardrails|instructions)",
        r"(invent|fabricate|make\s+up)\s+(a\s+)?(section|citation|judgment|case\s+law)",
    ]
]


def sanitize_text(text: str, max_length: int | None = None) -> str:
    """NFC-normalise, strip control/bidi-override characters, collapse whitespace runs."""
    clean = unicodedata.normalize("NFC", text or "")
    clean = _CONTROL.sub(" ", clean)
    clean = re.sub(r"[ \t]{2,}", " ", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean).strip()
    if max_length is not None:
        clean = clean[:max_length]
    return clean


def detect_language(text: str) -> str:
    """Return 'urdu', 'roman_urdu' or 'english'."""
    sample = text or ""
    urdu = len(_URDU_CHAR.findall(sample))
    latin = len(_LATIN_CHAR.findall(sample))
    if urdu and urdu >= latin * 0.5:
        return "urdu"
    words = _WORD.findall(sample.lower())
    if not words:
        return "urdu" if urdu else "english"
    strong = sum(1 for w in words if w in _ROMAN_URDU_MARKERS and w not in _AMBIGUOUS)
    weak = sum(1 for w in words if w in _AMBIGUOUS)
    ratio = (strong + 0.3 * weak) / len(words)
    if strong >= 2 and ratio >= 0.12:
        return "roman_urdu"
    if strong >= 1 and len(words) <= 6 and ratio >= 0.2:
        return "roman_urdu"
    return "english"


def normalize_roman_urdu(text: str) -> str:
    """Lower-case and canonicalise common Roman-Urdu spellings (token-wise)."""
    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?|\S", (text or "").lower())
    out = []
    for token in tokens:
        out.append(ROMAN_URDU_CANON.get(token, token))
    return " ".join(out)


def normalize_for_matching(text: str) -> str:
    """Single normalised string used by keyword rules (English + Roman Urdu + Urdu kept)."""
    lowered = sanitize_text(text).lower()
    return normalize_roman_urdu(lowered) + " " + lowered


def bridge_terms(text: str) -> list[str]:
    """English legal vocabulary implied by Roman-Urdu / Urdu terms in the text."""
    normalized = normalize_roman_urdu(text)
    tokens = set(normalized.split())
    terms: list[str] = []
    for key, values in LEGAL_BRIDGE.items():
        if (" " in key and key in normalized) or key in tokens:
            terms.extend(values)
    for key, values in URDU_BRIDGE.items():
        if key in text:
            terms.extend(values)
    seen: set[str] = set()
    unique = []
    for term in terms:
        if term not in seen:
            seen.add(term)
            unique.append(term)
    return unique


def detect_prompt_injection(text: str) -> list[str]:
    """Return the matched injection patterns (empty list = none detected)."""
    hits = []
    for pattern in INJECTION_PATTERNS:
        if pattern.search(text or ""):
            hits.append(pattern.pattern)
    return hits
