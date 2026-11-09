"""Deterministic triage used when the LLM is unavailable, misconfigured, slow or returns invalid output.

It never asserts statutes, sections or deadlines — it classifies, asks questions, and flags urgency.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.core.text import normalize_for_matching
from app.schemas.triage import (
    FollowUpQuestion, LegalIssue, Pathway, TriageRequest, TriageResult, Urgency, Warning,
)
from app.services.urgency import EMERGENCY_GUIDANCE, apply_floor, detect_urgency_indicators

Lang = str  # "english" | "roman_urdu" | "urdu"


@dataclass(frozen=True)
class Q:
    id: str
    en: str
    ru: str
    ur: str
    reason: str
    priority: str = "high"

    def render(self, lang: Lang) -> FollowUpQuestion:
        text = {"english": self.en, "roman_urdu": self.ru, "urdu": self.ur}.get(lang, self.en)
        return FollowUpQuestion(id=self.id, question=text, reason=self.reason, priority=self.priority)


@dataclass(frozen=True)
class Category:
    name: str
    subcategory: str
    issue: str
    explanation: str
    terms: tuple[str, ...]
    questions: tuple[Q, ...]
    weight: float = 1.0
    pathways: tuple[Pathway, ...] = field(default_factory=tuple)
    # (missing fact, id of the follow-up question whose answer resolves it — or None)
    missing: tuple[tuple[str, str | None], ...] = field(default_factory=tuple)
    # Intake/workflow priority when no stronger urgency indicator is present — never a legal assessment.
    baseline: Urgency = Urgency.unknown


GENERIC_MISSING: tuple[tuple[str, str | None], ...] = (
    ("Relevant dates and any stated deadlines", None),
    ("Documents, notices or records already received", None),
    ("City/district where this happened", "location"),
    ("What outcome you want", "desired_outcome"),
)

GENERIC_PATHWAYS: tuple[Pathway, ...] = (
    Pathway(
        title="Collect and verify the relevant facts and documents",
        description="Gather documents, notices, agreements, orders, dates and other evidence connected to the matter "
                    "before relying on any legal pathway.",
        prerequisites=["Relevant documents", "Key dates"],
        caution="Do not assume that a document or deadline is legally decisive until it is verified.",
    ),
)

PROFESSIONAL_REVIEW = Pathway(
    title="Professional review",
    description="Consider review by a qualified lawyer, a district legal-aid committee, or the relevant authority if "
                "rights, deadlines, or court proceedings may be involved.",
    prerequisites=[],
    caution="This AI triage is not a substitute for professional legal advice.",
)

FIR_QUESTION = Q("fir_status", "Has an FIR been registered? If yes, do you have its number, police station and date?",
                 "Kya FIR darj hui hai? Agar haan, to FIR number, thana aur tareekh kya hai?",
                 "کیا ایف آئی آر درج ہوئی ہے؟ اگر ہاں تو نمبر، تھانہ اور تاریخ کیا ہے؟",
                 "FIR details determine the procedural stage.")

CATEGORIES: tuple[Category, ...] = (
    Category(
        "Theft / Robbery", "Possible theft, robbery or snatching", "theft/robbery — police report (FIR)",
        "The message appears to describe property being stolen, robbed or snatched. Such incidents are normally "
        "reported to the police, who record a First Information Report (FIR).",
        ("theft", "thief", "thieves", "theif", "theives", "thef", "steal", "stealing", "stole", "stolen", "stollen",
         "rob", "robbed", "robber", "robbers", "robbery", "robbing", "snatch", "snatched", "snatching", "snatcher",
         "mugged", "mugging", "pickpocket", "pickpocketed", "burglary", "burgled", "break-in", "broke into",
         # Not "chor" (also a spelling of "chhor" = leave), "cheen" (= China) or "لوٹ" (= return): too ambiguous.
         "looted", "loot", "dacoity", "dacoit", "dacoits", "chori", "churaya", "churai", "chura liya",
         "cheena", "cheen liya", "chheena", "chheen liya", "dakaiti", "daketi", "dakait",
         "loot liya", "lut liya", "چوری", "چور", "چھین", "ڈکیتی", "ڈاکو"),
        (FIR_QUESTION,
         Q("incident_details", "When did it happen, and what exactly was taken (with any serial number, IMEI or receipt)?",
           "Yeh kab hua, aur kya cheez li gayi (serial number, IMEI ya raseed ke saath)?",
           "یہ کب ہوا، اور کیا چیز لی گئی (سیریل نمبر، آئی ایم ای آئی یا رسید سمیت)؟",
           "The date, the items and their identifying details go into the police report."),
         Q("force_used", "Was any force, threat or weapon used, and was anyone hurt?",
           "Kya zabardasti, dhamki ya hathiyar istemal hua, aur kya koi zakhmi hua?",
           "کیا زبردستی، دھمکی یا ہتھیار استعمال ہوا، اور کیا کوئی زخمی ہوا؟",
           "Force, threats or injuries affect how the incident is recorded and how urgent it is."),
         Q("suspect_witnesses", "Do you know who took it, and were there witnesses or CCTV cameras nearby?",
           "Kya aap jaante hain kis ne liya, aur kya wahan koi gawah ya CCTV camera tha?",
           "کیا آپ جانتے ہیں کس نے لیا، اور کیا وہاں کوئی گواہ یا سی سی ٹی وی کیمرہ تھا؟",
           "Suspect details, witnesses and footage help the investigation.", "medium")),
        weight=1.4,
        pathways=(
            Pathway(
                title="Report it to the police",
                description="Go to the police station for the area where it happened and ask for an FIR to be "
                            "registered. Take your CNIC and any proof of ownership (receipt, box, serial number or "
                            "IMEI), and ask for a copy of the FIR with its number.",
                prerequisites=["CNIC", "Proof of ownership", "Date, time and place of the incident"],
                caution="If the police do not register the report, note the officer's name and the date and ask a "
                        "lawyer or legal-aid office about the remedies available.",
            ),
            Pathway(
                title="Limit further harm",
                description="If a phone, laptop, cards or ID were taken, change your account passwords, ask your bank "
                            "to block cards, and ask your mobile network to block the SIM and report the IMEI.",
                prerequisites=["Serial number / IMEI", "Account and card details"],
                caution="Keep records of every report you make; they may be needed later.",
            ),
        ),
        missing=(
            ("Date and time of the incident", "incident_details"),
            ("What was taken, its approximate value and identifying details (serial number / IMEI, receipt)",
             "incident_details"),
            ("Whether an FIR has been registered — number, police station and date", "fir_status"),
            ("Whether force, threats or a weapon were used, and any injuries", "force_used"),
            ("Suspect description, witnesses or CCTV footage", "suspect_witnesses"),
            ("City/district and police-station area where it happened", "location"),
        ),
        baseline=Urgency.medium,
    ),
    Category(
        "Criminal / Police", "Possible police, FIR, arrest or bail matter", "criminal/police matter",
        "The message appears to involve police action, an FIR, an arrest, bail, or a criminal complaint.",
        ("fir", "police", "arrest", "arrested", "bail", "giraftar", "giraftari", "zamanat", "thana", "hirasat",
         "custody", "detained", "theft", "chori", "robbery", "dacoity", "murder", "qatl", "assault", "cheating",
         "fraud", "dhoka", "kidnap", "aghwa", "complaint against", "پولیس", "ایف آئی آر", "گرفتار", "ضمانت",
         "تھانہ", "چوری", "قتل", "اغوا", "حراست"),
        (FIR_QUESTION,
         Q("custody_status", "Is anyone currently in police custody, and since when?",
           "Kya koi is waqt police hirasat mein hai, aur kab se?",
           "کیا کوئی اس وقت پولیس حراست میں ہے، اور کب سے؟",
           "Custody duration and status can be time-critical.")),
        weight=1.3,
        missing=(
            ("Whether an FIR has been registered — number, police station and date", "fir_status"),
            ("Whether anyone is in custody, and since when", "custody_status"),
            ("Documents or notices received from the police or a court", None),
            ("City/district and police-station area", "location"),
        ),
    ),
    Category(
        "Family", "Possible marriage, divorce, khula, maintenance or custody matter", "family law matter",
        "The message appears to involve marriage, divorce/khula, maintenance, dower or child custody.",
        ("divorce", "talaq", "khula", "nikah", "marriage", "husband", "wife", "shohar", "biwi", "maintenance",
         "nafqa", "custody of", "child custody", "bachay", "guardian", "dower", "mehr", "haq mehr", "dowry",
         "jahez", "sasural", "in-laws", "طلاق", "خلع", "نکاح", "شوہر", "بیوی", "نفقہ", "حق مہر", "جہیز", "بچوں"),
        (Q("marriage_docs", "Do you have the Nikahnama, and has any divorce/khula notice or family-court case been filed?",
           "Kya aap ke paas nikahnama hai, aur kya talaq/khula ka notice ya family court mein case dakhil hua hai?",
           "کیا آپ کے پاس نکاح نامہ ہے، اور کیا طلاق/خلع کا نوٹس یا فیملی کورٹ میں مقدمہ دائر ہوا ہے؟",
           "Marriage records and filed proceedings shape the available options."),
         Q("children", "Are children involved, and who are they currently living with?",
           "Kya bachay shamil hain, aur woh is waqt kis ke saath reh rahe hain?",
           "کیا بچے شامل ہیں، اور وہ اس وقت کس کے ساتھ رہ رہے ہیں؟",
           "Custody and maintenance questions depend on the children's situation.")),
        weight=1.2,
    ),
    Category(
        "Workplace harassment", "Possible harassment complaint", "harassment",
        "The message appears to involve harassment, possibly at a workplace.",
        ("harassment", "harass", "harassed", "stalking", "inappropriate", "ہراسانی", "ہراساں"),
        (Q("harassment_where", "Where did the harassment happen (workplace, online, public place) and who is involved?",
           "Harassment kahan hui (daftar, online, awami jagah) aur kaun shamil hai?",
           "ہراسانی کہاں ہوئی (دفتر، آن لائن، عوامی جگہ) اور کون ملوث ہے؟",
           "The setting determines which complaint forum may apply."),
         Q("harassment_evidence", "Do you have messages, witnesses or other records of the incidents, with dates?",
           "Kya aap ke paas messages, gawah ya waqiyat ka koi record tareekhon ke saath hai?",
           "کیا آپ کے پاس پیغامات، گواہ یا واقعات کا کوئی ریکارڈ تاریخوں کے ساتھ ہے؟",
           "Evidence and dates support any complaint.")),
        weight=1.2,
    ),
    Category(
        "Cybercrime", "Possible online harassment, blackmail or fraud", "online/cyber matter",
        "The message appears to involve online harassment, account misuse, blackmail or digital fraud.",
        ("hacked", "hack", "online", "facebook", "whatsapp", "instagram", "fake account", "fake id", "blackmail",
         "pictures", "photos", "video leaked", "cyber", "fia", "sim", "otp", "bank account", "jazzcash", "easypaisa",
         "بلیک میل", "آن لائن", "ہیک"),
        (Q("cyber_evidence", "Have you saved screenshots, links, account names and transaction IDs related to the incident?",
           "Kya aap ne screenshots, links, account names aur transaction IDs mehfooz kar liye hain?",
           "کیا آپ نے اسکرین شاٹس، لنکس، اکاؤنٹ کے نام اور ٹرانزیکشن آئی ڈیز محفوظ کر لیے ہیں؟",
           "Digital evidence can disappear; preservation matters."),),
        weight=1.0,
    ),
    Category(
        "Landlord / Tenant", "Possible rental, tenancy, or eviction dispute", "landlord/tenant dispute",
        "The message appears to involve a rental, tenancy, or eviction issue.",
        ("landlord", "tenant", "rent", "rented", "rental", "evict", "eviction", "tenancy", "lease", "kiraya",
         "kirayedar", "makaan malik", "ghar khali", "advance", "security deposit", "کرایہ", "کرایہ دار",
         "مالک مکان", "بے دخل"),
        (Q("tenancy_agreement", "Do you have a written rental agreement, and when did the tenancy begin?",
           "Kya aap ke paas likhit kiraya nama hai, aur kirayedari kab shuru hui?",
           "کیا آپ کے پاس تحریری کرایہ نامہ ہے، اور کرایہ داری کب شروع ہوئی؟",
           "The agreement and tenancy dates may affect the available options."),
         Q("eviction_notice", "Have you received a written eviction notice or any court order?",
           "Kya aap ko ghar khali karne ka likhit notice ya adalat ka koi hukum mila hai?",
           "کیا آپ کو مکان خالی کرنے کا تحریری نوٹس یا عدالت کا کوئی حکم ملا ہے؟",
           "Notices, orders, and deadlines need to be checked carefully.")),
        weight=1.25,
    ),
    Category(
        "Property / Inheritance", "Possible property, possession, or inheritance dispute", "property/possession/inheritance",
        "The message appears to involve property-related rights or inheritance.",
        ("inherit", "inheritance", "inherited", "waris", "virasat", "succession", "heirs", "share in property",
         "وراثت", "وارث", "ترکہ"),
        (Q("property_owner", "Who is currently recorded as the owner of the property?",
           "Record mein is waqt jaidad ka malik kaun darj hai?",
           "ریکارڈ میں اس وقت جائیداد کا مالک کون درج ہے؟",
           "Ownership records can materially change the legal analysis."),
         Q("property_documents", "What property, inheritance, or ownership documents do you have?",
           "Aap ke paas jaidad, virasat ya malkiyat ke kaun se kaghzat hain?",
           "آپ کے پاس جائیداد، وراثت یا ملکیت کے کون سے کاغذات ہیں؟",
           "The available documents may affect the next step.")),
        weight=1.15,
    ),
    Category(
        "Property / Inheritance", "Possible property or possession dispute", "property/possession",
        "The message appears to involve property rights or possession; the exact issue needs clarification.",
        ("property", "land", "plot", "house", "qabza", "possession", "zameen", "jaidad", "registry", "intiqal",
         "mutation", "fard", "encroach", "قبضہ", "زمین", "جائیداد", "پلاٹ", "رجسٹری", "انتقال"),
        (Q("property_owner", "Who is currently recorded as the owner of the property?",
           "Record mein is waqt jaidad ka malik kaun darj hai?",
           "ریکارڈ میں اس وقت جائیداد کا مالک کون درج ہے؟",
           "Ownership records can materially change the legal analysis."),
         Q("property_documents", "What property or ownership documents do you have?",
           "Aap ke paas jaidad ya malkiyat ke kaun se kaghzat hain?",
           "آپ کے پاس جائیداد یا ملکیت کے کون سے کاغذات ہیں؟",
           "The available documents may affect the next step.")),
        weight=0.9,
    ),
    Category(
        "Employment", "Possible employment, wages or termination dispute", "employment matter",
        "The message appears to involve employment, unpaid wages or termination.",
        ("salary", "wages", "employer", "employee", "fired", "terminated", "termination", "job", "naukri",
         "tankhwa", "company", "factory", "overtime", "gratuity", "eobi", "نوکری", "تنخواہ", "ملازمت"),
        (Q("employment_terms", "Do you have an appointment letter or contract, and how long have you worked there?",
           "Kya aap ke paas appointment letter ya contract hai, aur aap ne wahan kitna arsa kaam kiya?",
           "کیا آپ کے پاس تقرری نامہ یا معاہدہ ہے، اور آپ نے وہاں کتنا عرصہ کام کیا؟",
           "Terms and length of service affect entitlements."),
         Q("employment_dispute", "What exactly is unpaid or disputed, and since when?",
           "Kya cheez ada nahi hui ya mutnaza hai, aur kab se?",
           "کیا چیز ادا نہیں ہوئی یا متنازعہ ہے، اور کب سے؟",
           "Amounts and dates define the claim.")),
        weight=1.0,
    ),
    Category(
        "Consumer / Contract", "Possible consumer, contract or money dispute", "contract/consumer matter",
        "The message appears to involve an agreement, a purchase, a service, or money owed.",
        ("contract", "agreement", "refund", "defective", "consumer", "warranty", "loan", "qarz", "paisay", "money owed",
         "cheque", "dishonoured", "bounced", "payment", "معاہدہ", "قرض", "چیک"),
        (Q("contract_docs", "Is there a written agreement, receipt, cheque or message showing the deal or payment?",
           "Kya koi likhit muahida, raseed, cheque ya message hai jo deal ya payment dikhata ho?",
           "کیا کوئی تحریری معاہدہ، رسید، چیک یا پیغام ہے جو سودا یا ادائیگی ظاہر کرے؟",
           "Documentary proof is central to contract and consumer claims."),),
        weight=0.95,
    ),
)

GENERIC_QUESTION = Q(
    "desired_outcome",
    "What outcome are you trying to achieve, and has any court, police, government office, or other authority already been contacted?",
    "Aap kya nateeja chahte hain, aur kya kisi adalat, police, sarkari daftar ya kisi aur idare se rabta kiya gaya hai?",
    "آپ کیا نتیجہ چاہتے ہیں، اور کیا کسی عدالت، پولیس، سرکاری دفتر یا کسی اور ادارے سے رابطہ کیا گیا ہے؟",
    "This helps determine the relevant pathway and urgency.",
)
LOCATION_QUESTION = Q(
    "location", "In which city/district and province did this happen?",
    "Yeh maamla kis shehar/zila aur subay mein hai?",
    "یہ معاملہ کس شہر/ضلع اور صوبے میں ہے؟",
    "Jurisdiction and applicable provincial law depend on location.", "medium",
)


def _transpositions(term: str) -> set[str]:
    return {term[:i] + term[i + 1] + term[i] + term[i + 2:] for i in range(len(term) - 1)} - {term}


def _term_hits(text: str, term: str, tokens: set[str] | None = None) -> int:
    if re.fullmatch(r"[a-z0-9 \-]+", term):
        hits = len(re.findall(rf"\b{re.escape(term)}\b", text))
        # Tolerate the most common typing slip (two adjacent letters swapped, e.g. "theif", "salray") in longer
        # single words; short words are excluded because their swaps collide with real words.
        if not hits and tokens is not None and len(term) >= 5 and term.isalpha():
            hits = int(bool(_transpositions(term) & tokens))
        return hits
    return text.count(term)


def classify(text: str) -> list[tuple[float, Category]]:
    haystack = normalize_for_matching(text)
    tokens = set(re.findall(r"[a-z0-9]+", haystack))
    scored = []
    for category in CATEGORIES:
        hits = sum(min(2, _term_hits(haystack, term, tokens)) for term in category.terms)
        if hits:
            scored.append((hits * category.weight, category))
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored


def _summary(message: str, category: Category | None) -> str:
    first = re.split(r"(?<=[.!?۔؟])\s+", message.strip())
    excerpt = " ".join(first[:2]).strip().rstrip(".۔")
    if len(excerpt) > 280:
        excerpt = excerpt[:277].rstrip() + "…"
    lead = category.explanation if category else "The matter could not be classified from the description alone."
    return (f"{lead} Reported account: \"{excerpt}\". "
            "More details are needed before a reliable legal pathway can be identified.")


def deterministic_fallback(request: TriageRequest, response_language: Lang = "english",
                           detected_language: Lang | None = None, reason: str = "") -> TriageResult:
    lang = response_language if response_language in {"english", "roman_urdu", "urdu"} else "english"
    # Clarification answers are part of the citizen's account: they can reveal the category ("I want the thief
    # caught") and they resolve the questions/missing facts they answer. Question texts are NOT classified —
    # they contain our own category vocabulary ("Has an FIR been registered?").
    answered = {a.question_id for a in request.answers if a.answer.strip()}
    citizen_text = " ".join([request.message, *(a.answer for a in request.answers)])
    scored = classify(citizen_text)
    indicators = detect_urgency_indicators(citizen_text)

    issues: list[LegalIssue] = []
    questions: list[FollowUpQuestion] = []
    seen_q: set[str] = set()
    category_name = "General legal matter"
    subcategory = "Needs clarification"
    primary: Category | None = None
    active: list[Category] = []

    def ask(q: Q) -> None:
        if q.id not in seen_q:
            seen_q.add(q.id)
            if q.id not in answered:
                questions.append(q.render(lang))

    if scored:
        top_score = scored[0][0]
        primary = scored[0][1]
        category_name, subcategory = primary.name, primary.subcategory
        for score, category in scored[:2]:
            if category is not primary and score < top_score * 0.5:
                continue
            if any(issue.issue == category.issue for issue in issues):
                continue
            active.append(category)
            confidence = round(min(0.7, 0.35 + 0.08 * score), 2)
            issues.append(LegalIssue(issue=category.issue, explanation=category.explanation, confidence=confidence))
            for q in category.questions:
                ask(q)
    else:
        ask(GENERIC_QUESTION)
    ask(LOCATION_QUESTION)

    missing: list[str] = []
    for fact, resolved_by in (primary.missing if primary and primary.missing else GENERIC_MISSING):
        if (resolved_by is None or resolved_by not in answered) and fact not in missing:
            missing.append(fact)

    warnings = [Warning(code="triage_only",
                        message="The available information is insufficient for a definitive legal conclusion.",
                        severity="warning")]
    urgency = apply_floor(primary.baseline if primary else Urgency.unknown, indicators)
    if urgency == Urgency.critical:
        warnings.insert(0, Warning(code="emergency_contacts", message=EMERGENCY_GUIDANCE[lang], severity="urgent"))
    elif urgency == Urgency.high:
        warnings.insert(0, Warning(code="time_sensitive",
                                   message="The message suggests a time-sensitive situation. Seek prompt review by a qualified lawyer or the relevant authority.",
                                   severity="urgent"))

    pathways: list[Pathway] = []
    for category in active:
        pathways.extend(p for p in category.pathways if p not in pathways)
    if not pathways:
        pathways.extend(GENERIC_PATHWAYS)
    pathways.append(PROFESSIONAL_REVIEW)

    facts = list(request.known_facts)
    facts.extend(a.as_fact() for a in request.answers if a.answer.strip() and a.as_fact() not in facts)

    return TriageResult(
        category=category_name,
        subcategory=subcategory,
        summary=_summary(request.message, primary),
        issues=issues,
        urgency=urgency,
        facts=facts[:50],
        missing_facts=missing,
        follow_up_questions=questions,
        possible_pathways=pathways,
        warnings=warnings,
        source_ids_used=[],
        mode="deterministic_fallback",
        detected_language=detected_language or "english",
        response_language=lang,
        urgency_indicators=indicators,
        fallback_reason=reason,
    )
