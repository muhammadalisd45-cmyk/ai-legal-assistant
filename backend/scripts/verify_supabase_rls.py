"""Live RLS / access-control verification against a real Supabase project, using only the public anon key.

Creates two anonymous users (A, B) and one clearly-labelled test case owned by A, then checks that B and
unauthenticated callers cannot read or change it, and that corpus tables are closed to browser roles.

Usage:
  python scripts/verify_supabase_rls.py                       # reads SUPABASE_URL / SUPABASE_ANON_KEY (env or backend/.env)
  python scripts/verify_supabase_rls.py --env-file ../frontend/.env   # or NEXT_PUBLIC_* names from the frontend env

Test rows have public_case_id "RLS-TEST-…" and can be removed with:
  delete from public.cases where public_case_id like 'RLS-TEST-%';
"""
from __future__ import annotations

import argparse
import os
import re
import secrets
import sys
from pathlib import Path

import httpx

RESULTS: list[tuple[str, str, str]] = []


def record(name: str, status: str, detail: str = "") -> None:
    RESULTS.append((name, status, detail))
    print(f"{status:8} {name}" + (f"  — {detail}" if detail else ""))


def load_env(path: str | None) -> tuple[str, str]:
    values = dict(os.environ)
    if path and Path(path).exists():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*([A-Z0-9_]+)\s*=\s*(.*)$", line)
            if m:
                values.setdefault(m.group(1), m.group(2).strip().strip('"'))
    url = values.get("SUPABASE_URL") or values.get("NEXT_PUBLIC_SUPABASE_URL") or ""
    key = values.get("SUPABASE_ANON_KEY") or values.get("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
    if not url or not key:
        raise SystemExit("SUPABASE_URL and SUPABASE_ANON_KEY (or NEXT_PUBLIC_* equivalents) are required.")
    return url.rstrip("/"), key


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=str(Path(__file__).resolve().parents[1] / ".env"))
    args = parser.parse_args()
    url, key = load_env(args.env_file)
    c = httpx.Client(timeout=20)

    def signup() -> dict:
        r = c.post(f"{url}/auth/v1/signup", headers={"apikey": key, "content-type": "application/json"},
                   json={"data": {"app": "pjn-rls-verification"}})
        r.raise_for_status()
        return r.json()

    def h(token: str | None, prefer: str | None = None) -> dict:
        out = {"apikey": key, "Authorization": f"Bearer {token or key}", "content-type": "application/json"}
        if prefer:
            out["Prefer"] = prefer
        return out

    a, b = signup(), signup()
    ta, tb = a["access_token"], b["access_token"]
    ua, ub = a["user"]["id"], b["user"]["id"]
    record("anonymous sign-in", "PASS", "two independent anonymous users created")

    public_id = "RLS-TEST-" + secrets.token_hex(4).upper()
    r = c.post(f"{url}/rest/v1/cases?select=id", headers=h(ta, "return=representation"), json={
        "user_id": ua, "public_case_id": public_id, "language": "en", "status": "intake",
        "raw_description": "Automated RLS verification case — safe to delete.", "structured_payload": {"test": True}})
    if r.status_code >= 400:
        record("owner can create case", "FAIL", f"{r.status_code} {r.text[:120]}")
        return 1
    case_id = r.json()[0]["id"]
    record("owner can create case", "PASS")

    r = c.get(f"{url}/rest/v1/cases?select=id&id=eq.{case_id}", headers=h(ta))
    record("owner can read own case", "PASS" if r.status_code == 200 and len(r.json()) == 1 else "FAIL", str(r.status_code))

    r = c.get(f"{url}/rest/v1/cases?select=id&id=eq.{case_id}", headers=h(tb))
    record("other user cannot read case", "PASS" if r.status_code == 200 and r.json() == [] else "FAIL", f"rows={len(r.json()) if r.status_code == 200 else r.status_code}")

    r = c.get(f"{url}/rest/v1/cases?select=id&id=eq.{case_id}", headers=h(None))
    record("unauthenticated (anon) cannot read case", "PASS" if r.status_code in (200, 401) and (r.status_code == 401 or r.json() == []) else "FAIL")

    r = c.patch(f"{url}/rest/v1/cases?id=eq.{case_id}&select=id", headers=h(tb, "return=representation"), json={"status": "closed"})
    record("other user cannot update case", "PASS" if r.status_code in (200, 403, 404) and (r.status_code != 200 or r.json() == []) else "FAIL", str(r.status_code))

    r = c.patch(f"{url}/rest/v1/cases?id=eq.{case_id}&select=id", headers=h(ta, "return=representation"), json={"user_id": ub})
    record("owner cannot transfer ownership", "PASS" if r.status_code >= 400 else "FAIL", str(r.status_code))

    r = c.post(f"{url}/rest/v1/cases", headers=h(tb), json={"user_id": ua, "public_case_id": public_id + "-X",
                                                            "raw_description": "forged owner"})
    record("cannot create a case owned by someone else", "PASS" if r.status_code >= 400 else "FAIL", str(r.status_code))

    r = c.post(f"{url}/rest/v1/case_messages", headers=h(tb), json={"case_id": case_id, "role": "citizen", "content": "x"})
    record("other user cannot add message", "PASS" if r.status_code >= 400 else "FAIL", str(r.status_code))

    r = c.post(f"{url}/rest/v1/case_messages", headers=h(ta), json={"case_id": case_id, "role": "citizen", "content": "test"})
    record("owner can add citizen message", "PASS" if r.status_code < 300 else "FAIL", str(r.status_code))

    r = c.post(f"{url}/rest/v1/case_messages", headers=h(ta), json={"case_id": case_id, "role": "system", "content": "forged"})
    record("owner cannot forge 'system' message", "PASS" if r.status_code >= 400 else "PENDING",
           "" if r.status_code >= 400 else "allowed — apply migration 005")

    r = c.get(f"{url}/rest/v1/case_messages?select=id&case_id=eq.{case_id}", headers=h(tb))
    record("other user cannot read messages", "PASS" if r.status_code == 200 and r.json() == [] else "FAIL")

    r = c.delete(f"{url}/rest/v1/cases?id=eq.{case_id}", headers=h(ta, "return=representation"))
    deleted = r.status_code < 300 and r.json() != []
    record("citizens cannot delete case records", "FAIL" if deleted else "PASS", str(r.status_code))

    for table in ("legal_chunks",):
        r = c.get(f"{url}/rest/v1/{table}?select=chunk_id&limit=1", headers=h(ta))
        record(f"{table} closed to browser roles", "PASS" if r.status_code in (401, 403) else "FAIL", str(r.status_code))
    r = c.post(f"{url}/rest/v1/legal_documents", headers=h(ta), json={"document_id": "HACK-1", "title": "x", "document_type": "x",
                                                                     "jurisdiction": "x", "authority": "x", "source_url": "x"})
    record("legal_documents not writable by users", "PASS" if r.status_code >= 400 else "FAIL", str(r.status_code))
    r = c.post(f"{url}/rest/v1/rpc/match_legal_chunks", headers=h(ta), json={"query_embedding": "[" + ",".join(["0"] * 384) + "]"})
    record("retrieval RPC not callable by users", "PASS" if r.status_code in (401, 403, 404) else "FAIL", str(r.status_code))

    r = c.get(f"{url}/storage/v1/bucket/case-documents", headers=h(ta))
    if r.status_code in (400, 404) and "not found" in r.text.lower():
        record("storage bucket case-documents", "PENDING", "bucket missing — apply migration 005")
    else:
        path = f"{ua}/{case_id}/{secrets.token_hex(4)}.pdf"
        r = c.post(f"{url}/storage/v1/object/case-documents/{path}", headers={**h(ta), "content-type": "application/pdf"},
                   content=b"%PDF-1.4\n%%EOF\n")
        record("owner can upload to own folder", "PASS" if r.status_code < 300 else "FAIL", str(r.status_code))
        r = c.get(f"{url}/storage/v1/object/authenticated/case-documents/{path}", headers=h(tb))
        record("other user cannot download", "PASS" if r.status_code >= 400 else "FAIL", str(r.status_code))
        r = c.post(f"{url}/storage/v1/object/case-documents/{ub}/{case_id}/x.pdf", headers={**h(ta), "content-type": "application/pdf"},
                   content=b"%PDF-1.4\n%%EOF\n")
        record("cannot upload into another user's folder", "PASS" if r.status_code >= 400 else "FAIL", str(r.status_code))

    fails = [n for n, s, _ in RESULTS if s == "FAIL"]
    pending = [n for n, s, _ in RESULTS if s == "PENDING"]
    print(f"\n{len(RESULTS) - len(fails) - len(pending)} passed, {len(fails)} failed, {len(pending)} pending migration 005")
    print(f"Test case: {public_id} (delete with: delete from public.cases where public_case_id like 'RLS-TEST-%';)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
