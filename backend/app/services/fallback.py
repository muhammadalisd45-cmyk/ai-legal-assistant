from app.schemas.triage import (
    FollowUpQuestion, LegalIssue, Pathway, TriageRequest,
    TriageResult, Urgency, Warning,
)


def deterministic_fallback(request: TriageRequest) -> TriageResult:
    text = request.message.lower()
    category = "General legal matter"
    subcategory = "Needs clarification"
    issues = []
    questions = []

    tenancy_terms = [
        "landlord", "tenant", "rent", "rented", "rental",
        "evict", "eviction", "tenancy", "lease", "kiraya",
        "kirayedar", "makaan malik", "ghar khali",
    ]
    inheritance_terms = [
        "inherit", "inheritance", "inherited", "waris",
        "virasat", "وراثت",
    ]
    property_terms = [
        "property", "land", "plot", "house", "qabza", "possession",
        "zameen", "ghar", "jaidad",
    ]

    if any(term in text for term in tenancy_terms):
        category = "Landlord / Tenant"
        subcategory = "Possible rental, tenancy, or eviction dispute"
        issues.append(LegalIssue(
            issue="landlord/tenant dispute",
            explanation="The message appears to involve a rental, tenancy, or eviction issue.",
            confidence=0.55,
        ))
        questions.extend([
            FollowUpQuestion(
                id="tenancy_agreement",
                question="Do you have a written rental agreement, and when did the tenancy begin?",
                reason="The agreement and tenancy dates may affect the available options.",
                priority="high",
            ),
            FollowUpQuestion(
                id="eviction_notice",
                question="Have you received a written eviction notice or any court order?",
                reason="Notices, orders, and deadlines need to be checked carefully.",
                priority="high",
            ),
        ])
    elif any(term in text for term in inheritance_terms):
        category = "Property / Inheritance"
        subcategory = "Possible property, possession, or inheritance dispute"
        issues.append(LegalIssue(
            issue="property/possession/inheritance",
            explanation="The message appears to involve property-related rights or inheritance.",
            confidence=0.55,
        ))
        questions.extend([
            FollowUpQuestion(
                id="property_owner",
                question="Who is currently recorded as the owner of the property?",
                reason="Ownership records can materially change the legal analysis.",
                priority="high",
            ),
            FollowUpQuestion(
                id="property_documents",
                question="What property, inheritance, or ownership documents do you have?",
                reason="The available documents may affect the next step.",
                priority="high",
            ),
        ])
    elif any(term in text for term in property_terms):
        category = "Property / Inheritance"
        subcategory = "Possible property or possession dispute"
        issues.append(LegalIssue(
            issue="property/possession",
            explanation="The message appears to involve property rights or possession; the exact issue needs clarification.",
            confidence=0.45,
        ))
        questions.extend([
            FollowUpQuestion(
                id="property_owner",
                question="Who is currently recorded as the owner of the property?",
                reason="Ownership records can materially change the legal analysis.",
                priority="high",
            ),
            FollowUpQuestion(
                id="property_documents",
                question="What property or ownership documents do you have?",
                reason="The available documents may affect the next step.",
                priority="high",
            ),
        ])
    else:
        questions.append(FollowUpQuestion(
            id="desired_outcome",
            question="What outcome are you trying to achieve, and has any court, police, government office, or other authority already been contacted?",
            reason="This helps determine the relevant pathway and urgency.",
            priority="high",
        ))

    return TriageResult(
        category=category,
        subcategory=subcategory,
        summary="The issue needs further fact collection before a reliable legal pathway can be identified.",
        issues=issues,
        urgency=Urgency.unknown,
        facts=request.known_facts,
        missing_facts=[
            "Relevant dates and any stated deadlines",
            "Documents or notices already received",
            "Location/jurisdiction of the dispute",
            "What outcome the citizen wants",
        ],
        follow_up_questions=questions,
        possible_pathways=[
            Pathway(
                title="Collect and verify the relevant facts and documents",
                description="Gather ownership records, notices, agreements, orders, dates, and other relevant evidence before relying on a legal pathway.",
                prerequisites=["Relevant documents", "Key dates"],
                caution="Do not assume that a document or deadline is legally decisive until it is verified.",
            ),
            Pathway(
                title="Professional review",
                description="Consider review by a qualified lawyer or the relevant authority if rights, deadlines, or court proceedings may be involved.",
                prerequisites=[],
                caution="This AI triage is not a substitute for professional legal advice.",
            ),
        ],
        warnings=[Warning(
            code="triage_only",
            message="The available information is insufficient for a definitive legal conclusion.",
            severity="warning",
        )],
        mode="deterministic_fallback",
    )
