import time

import jwt
import pytest

from app.core.config import settings
from conftest import auth_headers
from helpers import make_pdf

CASES = "/api/v1/cases"


def create_case(client, headers, **kw):
    payload = {"description": "My landlord is trying to evict me without notice.", "language": "en", **kw}
    response = client.post(CASES, json=payload, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()


# ---------------- authentication ----------------

@pytest.mark.parametrize("method,path", [
    ("get", CASES), ("post", CASES), ("get", f"{CASES}/PJN-AAAA1111"), ("get", "/api/v1/auth/me"),
])
def test_case_routes_require_auth(client, method, path):
    response = getattr(client, method)(path, **({"json": {"description": "x"}} if method == "post" else {}))
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "auth_required"


def test_invalid_expired_and_tampered_tokens_rejected(client):
    assert client.get(CASES, headers={"Authorization": "Bearer not-a-jwt"}).status_code == 401
    expired = jwt.encode({"sub": "6f0c3c1e-0000-4000-8000-000000000000", "iss": "pjn-backend", "aud": "pjn-api",
                          "exp": int(time.time()) - 10}, settings.local_jwt_secret, algorithm="HS256")
    response = client.get(CASES, headers={"Authorization": f"Bearer {expired}"})
    assert response.status_code == 401 and response.json()["error"]["code"] == "token_expired"
    forged = jwt.encode({"sub": "6f0c3c1e-0000-4000-8000-000000000000", "iss": "pjn-backend", "aud": "pjn-api",
                         "exp": int(time.time()) + 600}, "attacker-secret-attacker-secret-1234", algorithm="HS256")
    assert client.get(CASES, headers={"Authorization": f"Bearer {forged}"}).status_code == 401
    none_alg = jwt.encode({"sub": "6f0c3c1e-0000-4000-8000-000000000000"}, key=None, algorithm="none")
    assert client.get(CASES, headers={"Authorization": f"Bearer {none_alg}"}).status_code == 401


def test_anonymous_session_and_me(client):
    headers = auth_headers(client)
    me = client.get("/api/v1/auth/me", headers=headers).json()
    assert me["auth_mode"] == "local" and me["is_anonymous"] is True


# ---------------- cases CRUD + isolation ----------------

def test_case_lifecycle(client):
    headers = auth_headers(client)
    case = create_case(client, headers, public_case_id="PJN-TEST0001", category="Landlord / Tenant", urgency="high")
    assert case["public_case_id"] == "PJN-TEST0001" and case["status"] == "intake"
    by_public = client.get(f"{CASES}/PJN-TEST0001", headers=headers).json()
    by_uuid = client.get(f"{CASES}/{case['id']}", headers=headers).json()
    assert by_public["id"] == by_uuid["id"] == case["id"]
    patched = client.patch(f"{CASES}/{case['id']}", json={"status": "ready_for_lawyer"}, headers=headers).json()
    assert patched["status"] == "ready_for_lawyer"
    listing = client.get(CASES, headers=headers).json()
    assert [c["id"] for c in listing["items"]] == [case["id"]]
    assert client.post(CASES, json={"description": "dup", "public_case_id": "PJN-TEST0001"}, headers=headers).status_code == 409


def test_users_cannot_see_or_modify_each_others_cases(client):
    alice, mallory = auth_headers(client), auth_headers(client)
    case = create_case(client, alice)
    for path in (f"{CASES}/{case['id']}", f"{CASES}/{case['public_case_id']}", f"{CASES}/{case['id']}/messages",
                 f"{CASES}/{case['id']}/documents"):
        assert client.get(path, headers=mallory).status_code == 404, path
    assert client.patch(f"{CASES}/{case['id']}", json={"status": "closed"}, headers=mallory).status_code == 404
    assert client.post(f"{CASES}/{case['id']}/messages", json={"content": "hi"}, headers=mallory).status_code == 404
    assert client.get(CASES, headers=mallory).json()["items"] == []
    assert client.get(f"{CASES}/{case['id']}", headers=alice).json()["status"] == "intake"


def test_case_create_with_triage(client):
    headers = auth_headers(client)
    case = create_case(client, headers, description="Police ne bhai ko giraftar kar liya hai, FIR nahi dikhayi",
                       language="roman-ur", run_triage=True)
    assert case["category"] == "Criminal / Police" and case["urgency"] == "critical"
    assert case["status"] == "analysis"
    assert case["structured_payload"]["triage"]["mode"] == "deterministic_fallback"


def test_case_validation(client):
    headers = auth_headers(client)
    assert client.post(CASES, json={"description": "x", "public_case_id": "../../etc"}, headers=headers).status_code == 422
    assert client.post(CASES, json={"description": "x", "language": "fr"}, headers=headers).status_code == 422
    big = {"blob": "a" * (300 * 1024)}
    assert client.post(CASES, json={"description": "x", "structured_payload": big}, headers=headers).status_code == 422
    assert client.post(CASES, json={"description": "x", "user_id": "someone-else"}, headers=headers).status_code == 422


def test_messages(client):
    headers = auth_headers(client)
    case = create_case(client, headers)
    first = client.post(f"{CASES}/{case['id']}/messages", json={"content": "Notice received today", "language": "en"},
                        headers=headers)
    assert first.status_code == 201
    client.post(f"{CASES}/{case['id']}/messages", json={"role": "assistant", "content": "Noted."}, headers=headers)
    messages = client.get(f"{CASES}/{case['id']}/messages", headers=headers).json()
    assert [m["role"] for m in messages] == ["citizen", "assistant"]
    assert client.post(f"{CASES}/{case['id']}/messages", json={"role": "system", "content": "x"},
                       headers=headers).status_code == 422


# ---------------- documents ----------------

def upload(client, headers, case_id, name, content, mime="application/pdf"):
    return client.post(f"{CASES}/{case_id}/documents", files={"file": (name, content, mime)}, headers=headers)


def test_pdf_upload_processing_and_owner_only_download(client):
    alice, mallory = auth_headers(client), auth_headers(client)
    case = create_case(client, alice)
    pdf = make_pdf(["EVICTION NOTICE", "You must vacate the premises within 15 days."])
    response = upload(client, alice, case["id"], "notice.pdf", pdf)
    assert response.status_code == 202
    doc = response.json()
    assert doc["status"] == "queued" and doc["page_count"] == 2 and len(doc["sha256"]) == 64
    # TestClient runs background tasks before returning; the document is processed by now.
    detail = client.get(f"{CASES}/{case['id']}/documents/{doc['id']}", headers=alice).json()
    assert detail["status"] == "analyzed"
    assert "vacate the premises" in detail["analysis"]["text"]
    listing = client.get(f"{CASES}/{case['id']}/documents", headers=alice).json()
    assert "text" not in listing[0]["analysis"]
    content = client.get(f"{CASES}/{case['id']}/documents/{doc['id']}/content", headers=alice)
    assert content.status_code == 200 and content.content == pdf
    assert "attachment" in content.headers["content-disposition"]
    assert client.get(f"{CASES}/{case['id']}/documents/{doc['id']}/content", headers=mallory).status_code == 404
    stored = list((settings.upload_dir).rglob("*.pdf"))
    assert len(stored) == 1 and stored[0].name == f"{doc['id']}.pdf"  # random name, not "notice.pdf"


@pytest.mark.parametrize("name,content,code", [
    ("evil.pdf", b"MZ\x90\x00 this is an exe", "type_mismatch"),
    ("notes.txt", b"hello", "unsupported_type"),
    ("script.pdf", make_pdf(["hello"], javascript=True), "pdf_active_content"),
    ("empty.pdf", b"", "empty_file"),
    ("broken.pdf", b"%PDF-1.4 garbage without structure", "pdf_unreadable"),
    ("photo.png", b"\xff\xd8\xff\xe0 jpeg bytes", "type_mismatch"),
])
def test_upload_rejections(client, name, content, code):
    headers = auth_headers(client)
    case = create_case(client, headers)
    response = upload(client, headers, case["id"], name, content)
    assert response.status_code in (413, 415, 422)
    assert response.json()["error"]["code"] == code


def test_upload_size_limit(client, monkeypatch):
    monkeypatch.setattr(settings, "max_upload_bytes", 1024)
    headers = auth_headers(client)
    case = create_case(client, headers)
    response = upload(client, headers, case["id"], "big.pdf", make_pdf(["x " * 2000]))
    assert response.status_code == 413 and response.json()["error"]["code"] == "file_too_large"


def test_upload_filename_is_sanitised(client):
    headers = auth_headers(client)
    case = create_case(client, headers)
    doc = upload(client, headers, case["id"], "..\\..\\windows\\system32\\درخواست.pdf", make_pdf(["ok"])).json()
    assert doc["original_file_name"] == "درخواست.pdf"
    download = client.get(f"{CASES}/{case['id']}/documents/{doc['id']}/content", headers=headers)
    assert download.status_code == 200 and "filename*=UTF-8''" in download.headers["content-disposition"]


def test_png_upload_is_stored_with_ocr_note(client):
    headers = auth_headers(client)
    case = create_case(client, headers)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 64
    doc = upload(client, headers, case["id"], "photo.png", png, "image/png").json()
    detail = client.get(f"{CASES}/{case['id']}/documents/{doc['id']}", headers=headers).json()
    assert detail["status"] == "analyzed" and "OCR" in detail["analysis"]["note"]


def test_upload_to_someone_elses_case_is_404(client):
    alice, mallory = auth_headers(client), auth_headers(client)
    case = create_case(client, alice)
    assert upload(client, mallory, case["id"], "x.pdf", make_pdf(["x"])).status_code == 404


def test_legacy_document_extraction_endpoint(client):
    response = client.post("/api/v1/document", files={"file": ("a.pdf", make_pdf(["Hello legal text"]), "application/pdf")})
    assert response.status_code == 200 and "Hello legal text" in response.json()["text"]
    assert client.post("/api/v1/document", files={"file": ("a.pdf", b"nope", "application/pdf")}).status_code == 415
