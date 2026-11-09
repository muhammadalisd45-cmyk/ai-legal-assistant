"""Post-deployment smoke test against a running backend.

Usage:  python scripts/smoke_test.py [--base http://127.0.0.1:8000] [--token <supabase access token>]
With AUTH_MODE=local the script creates an anonymous session itself. Exits non-zero on the first failure.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tests"))

from helpers import make_pdf  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(condition), detail))
    print(f"{'PASS' if condition else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))
    if not condition:
        raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:8000")
    parser.add_argument("--token", default="")
    parser.add_argument("--skip-documents", action="store_true", help="skip upload checks (e.g. before migration 005)")
    args = parser.parse_args()
    c = httpx.Client(base_url=args.base, timeout=60)

    import os

    def new_session() -> str:
        """Local mode: backend anonymous session. Supabase mode: Supabase anonymous sign-in."""
        local = c.post("/api/v1/auth/anonymous")
        if local.status_code == 200:
            return local.json()["access_token"]
        url, key = os.getenv("SUPABASE_URL", "").rstrip("/"), os.getenv("SUPABASE_ANON_KEY", "")
        if not url or not key:
            raise SystemExit("AUTH_MODE=supabase: set SUPABASE_URL and SUPABASE_ANON_KEY (or pass --token).")
        r = httpx.post(f"{url}/auth/v1/signup", headers={"apikey": key}, json={"data": {"app": "pjn-smoke-test"}}, timeout=20)
        r.raise_for_status()
        return r.json()["access_token"]

    for _ in range(60):
        try:
            if c.get("/health").status_code == 200:
                break
        except httpx.HTTPError:
            pass
        time.sleep(1)
    health = c.get("/health")
    check("GET /health", health.status_code == 200 and health.json()["status"] == "ok")
    ready = c.get("/health/ready").json()
    idx = ready["checks"]["legal_index"]
    check("GET /health/ready", ready["status"] in {"ready", "degraded"},
          f"status={ready['status']} chunks={idx['chunks']} embeddings={idx['embeddings']} llm={ready['checks']['llm']['configured']}")

    t = c.post("/api/v1/triage", json={"message": "Police ne mere bhai ko kal raat giraftar kar liya, FIR nahi dikhayi",
                                       "language": "roman_urdu"}).json()
    check("POST /api/v1/triage (Roman Urdu)", t["category"] == "Criminal / Police" or t["mode"] == "live",
          f"category={t['category']} urgency={t['urgency']} mode={t['mode']}")
    check("triage urgency floor", t["urgency"] == "critical")

    s = c.post("/v1/search", json={"query": "When can bail be granted for a non-bailable offence?", "limit": 5}).json()
    top = s["results"][0] if s["results"] else {}
    check("POST /v1/search (English)", s["mode"] != "metadata-only" and top.get("evidence_level") == "chunk",
          f"mode={s['mode']} top={top.get('document_id')} {top.get('section_or_article')} {top.get('page_reference')}")
    s_ur = c.post("/v1/search", json={"query": "ضمانت کب ملتی ہے"}).json()
    top_ur = s_ur["results"][0] if s_ur["results"] else {}
    check("POST /v1/search (Urdu)", top_ur.get("document_id") == "PK-003",
          f"top={top_ur.get('document_id')} {top_ur.get('section_or_article')}")
    s_ru = c.post("/v1/search", json={"query": "chacha ne zameen par qabza kar liya"}).json()
    top_ru = s_ru["results"][0] if s_ru["results"] else {}
    check("POST /v1/search (Roman Urdu)", top_ru.get("document_id") == "PK-007",
          f"top={top_ru.get('document_id')} {top_ru.get('section_or_article')}")

    a = c.post("/api/v1/answer", json={"question": "What are my rights if I am arrested?", "language": "english"}).json()
    check("POST /api/v1/answer", a["grounded"] and a["citations"], f"mode={a['mode']} citations={len(a['citations'])}")
    none = c.post("/api/v1/answer", json={"question": "What is the income tax rate on crypto profits?"}).json()
    check("answer without evidence is honest", none["mode"] in {"no_evidence", "extractive_fallback", "live"},
          f"mode={none['mode']} grounded={none['grounded']}")

    token = args.token or new_session()
    h = {"Authorization": f"Bearer {token}"}
    check("GET /api/v1/auth/me", c.get("/api/v1/auth/me", headers=h).status_code == 200,
          c.get("/api/v1/auth/me", headers=h).json().get("auth_mode", ""))
    check("cases require auth", c.get("/api/v1/cases").status_code == 401)
    import secrets

    # Identifiable test rows: delete with  delete from public.cases where public_case_id like 'SMOKE-TEST-%';
    case = c.post("/api/v1/cases", headers=h, json={"description": "Landlord ne 3 din mein ghar khali karne ka kaha hai",
                                                     "language": "roman-ur", "run_triage": True,
                                                     "public_case_id": "SMOKE-TEST-" + secrets.token_hex(4).upper()})
    check("POST /api/v1/cases", case.status_code == 201, f"status={case.status_code}")
    case = case.json()
    check("GET /api/v1/cases", any(x["id"] == case["id"] for x in c.get("/api/v1/cases", headers=h).json()["items"]))
    check("GET /api/v1/cases/{id}", c.get(f"/api/v1/cases/{case['public_case_id']}", headers=h).status_code == 200)
    msg = c.post(f"/api/v1/cases/{case['id']}/messages", headers=h, json={"content": "Notice mila hai", "language": "roman-ur"})
    check("POST /api/v1/cases/{id}/messages", msg.status_code == 201)
    check("GET /api/v1/cases/{id}/messages", len(c.get(f"/api/v1/cases/{case['id']}/messages", headers=h).json()) == 1)
    other = {"Authorization": f"Bearer {new_session()}"} if not args.token else None
    if other:
        check("other users get 404", c.get(f"/api/v1/cases/{case['id']}", headers=other).status_code == 404)
    if args.skip_documents:
        print(f"\nSKIP  document upload checks\n{sum(ok for _, ok, _ in RESULTS)}/{len(RESULTS)} checks passed")
        return 0
    up = c.post(f"/api/v1/cases/{case['id']}/documents", headers=h,
                files={"file": ("notice.pdf", make_pdf(["EVICTION NOTICE", "Vacate within 3 days."]), "application/pdf")})
    check("POST /api/v1/cases/{id}/documents", up.status_code == 202, f"status={up.status_code}")
    doc = up.json()
    for _ in range(20):
        detail = c.get(f"/api/v1/cases/{case['id']}/documents/{doc['id']}", headers=h).json()
        if detail["status"] in {"analyzed", "failed"}:
            break
        time.sleep(0.5)
    check("document processed", detail["status"] == "analyzed", f"status={detail['status']}")
    download = c.get(f"/api/v1/cases/{case['id']}/documents/{doc['id']}/content", headers=h)
    check("document download (owner)", download.status_code == 200 and download.content.startswith(b"%PDF"))
    if other:
        check("document download (other user) is 404",
              c.get(f"/api/v1/cases/{case['id']}/documents/{doc['id']}/content", headers=other).status_code == 404)

    print(f"\n{sum(ok for _, ok, _ in RESULTS)}/{len(RESULTS)} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
