"""Regression tests for a real intake that came out as an empty "General legal matter":
"there is theif case where a person robbed my laptop and now it is gone" (+ answers "I want to caught the theif",
"islamabad")."""
import pytest

from app.schemas.triage import ClarificationAnswer, TriageRequest
from app.services.fallback import classify, deterministic_fallback

REPORTED = "there is theif case where a person robbed my laptop and now it is gone"


@pytest.mark.parametrize("message", [
    REPORTED,
    "Someone stole my phone at the bus stop",
    "my bag was snatched yesterday",
    "I was mugged near the market and they took my wallet",
    "Mera laptop chori ho gaya hai",
    "Do larkon ne mera mobile cheen liya",
    "میرا موبائل چوری ہو گیا",
])
def test_theft_and_robbery_are_recognised(message):
    result = deterministic_fallback(TriageRequest(message=message))
    assert result.category == "Theft / Robbery"
    assert result.issues
    assert any(q.id == "fir_status" for q in result.follow_up_questions)
    assert result.urgency.value == "medium"  # workflow baseline — not a legal assessment
    assert any(p.title == "Report it to the police" for p in result.possible_pathways)
    assert not any("ownership records" in p.description for p in result.possible_pathways)


@pytest.mark.parametrize("message", [
    "My husband left me and does not pay maintenance — shohar ne chor diya hai",
    "I bought a phone made in cheen and it is defective, I want a refund",
    "I had a fight with my brother about the rent",
])
def test_ambiguous_words_do_not_trigger_theft(message):
    assert all(category.name != "Theft / Robbery" for _, category in classify(message))


def test_transposed_letters_are_tolerated_only_for_longer_words():
    assert classify("the theif ran away")[0][1].name == "Theft / Robbery"
    assert classify("My salray has not been paid by the employer")[0][1].name == "Employment"


def test_summary_is_plain_language_without_internal_labels():
    result = deterministic_fallback(TriageRequest(message=REPORTED))
    assert "Preliminary intake" not in result.summary and "unclassified" not in result.summary
    assert "robbed my laptop" in result.summary


def test_unclassified_summary_is_honest():
    result = deterministic_fallback(TriageRequest(message="I need some help with a problem I am facing at the moment"))
    assert result.category == "General legal matter"
    assert "could not be classified" in result.summary


def test_answers_resolve_questions_and_missing_facts():
    first = deterministic_fallback(TriageRequest(message=REPORTED))
    asked = {q.id: q.question for q in first.follow_up_questions}
    assert "location" in asked and "fir_status" in asked

    refined = deterministic_fallback(TriageRequest(message=REPORTED, answers=[
        ClarificationAnswer(question_id="fir_status", question=asked["fir_status"], answer="No, nobody informed the police"),
        ClarificationAnswer(question_id="location", question=asked["location"], answer="islamabad"),
    ]))
    remaining = {q.id for q in refined.follow_up_questions}
    assert "fir_status" not in remaining and "location" not in remaining
    assert "incident_details" in remaining
    assert not any("police-station area" in fact for fact in refined.missing_facts)
    assert not any("FIR has been registered" in fact for fact in refined.missing_facts)
    assert any("islamabad" in fact for fact in refined.facts)


def test_answers_can_classify_an_unclear_first_message():
    vague = "Something happened to me yesterday and I do not know what to do now"
    assert deterministic_fallback(TriageRequest(message=vague)).category == "General legal matter"
    refined = deterministic_fallback(TriageRequest(message=vague, answers=[
        ClarificationAnswer(question_id="desired_outcome", answer="I want the thief who stole my laptop caught")]))
    assert refined.category == "Theft / Robbery"


def test_question_text_is_not_classified():
    # Our own question mentions police/FIR; a neutral answer must not turn the case into a criminal matter.
    refined = deterministic_fallback(TriageRequest(message="My employer has not paid my salary for three months", answers=[
        ClarificationAnswer(question_id="desired_outcome",
                            question="Has any court, police, FIR or other authority been contacted?", answer="no")]))
    assert refined.category == "Employment"


def test_triage_api_accepts_answers(client):
    body = client.post("/api/v1/triage", json={
        "message": REPORTED, "language": "english",
        "answers": [{"question_id": "location", "question": "Which city?", "answer": "islamabad"}],
    }).json()
    assert body["category"] == "Theft / Robbery"
    assert all(q["id"] != "location" for q in body["follow_up_questions"])
    assert client.post("/api/v1/triage", json={
        "message": REPORTED, "answers": [{"question_id": "x", "answer": "y", "extra": 1}]}).status_code == 422


def test_colloquial_theft_query_is_bridged_to_statute_vocabulary():
    from app.legal.retrieval import analyze_query

    analysis = analyze_query(REPORTED)
    assert {"theft", "robbery"} <= set(analysis.bridged_terms)
    assert "suit" not in analysis.bridged_terms  # "case" no longer drags in civil procedure
    assert ("PK-002", "Section 390") in analysis.concept_hints and ("PK-003", "Section 154") in analysis.concept_hints
