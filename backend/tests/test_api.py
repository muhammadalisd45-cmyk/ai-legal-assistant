from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_triage_without_llm_uses_fallback():
    response = client.post(
        "/api/v1/triage",
        json={
            "message": "Mere chacha ne hamari inherited property par qabza kar liya hai.",
            "language": "roman_urdu",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "category" in body
    assert "follow_up_questions" in body
    assert "disclaimer" in body
