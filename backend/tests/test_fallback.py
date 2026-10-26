import pytest
from app.schemas.triage import TriageRequest
from app.services.fallback import deterministic_fallback

def test_property_fallback():
    request = TriageRequest(
        message="Mere chacha ne hamari inherited property par qabza kar liya hai.",
        language="roman_urdu",
    )
    result = deterministic_fallback(request)
    assert result.category == "Property / Inheritance"
    assert result.issues
    assert result.follow_up_questions
    assert result.urgency.value == "unknown"

def test_empty_message_rejected():
    with pytest.raises(ValueError):
        TriageRequest(message="")

def test_landlord_eviction_is_not_misclassified_as_inheritance():
    request = TriageRequest(
        message="My landlord is trying to evict me from the house I rent.",
        language="english",
    )
    result = deterministic_fallback(request)
    assert result.category != "Property / Inheritance"
