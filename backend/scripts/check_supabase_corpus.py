"""Local end-to-end check of the Supabase legal corpus, before relying on the GitHub workflows.

    python scripts/check_supabase_corpus.py              # read-only: config, tables, search functions, publish plan
    python scripts/check_supabase_corpus.py --publish    # ...then publish, re-check (expect 0 changes), and run
                                                         #    real searches through Supabase exactly as production does

Reads SUPABASE_URL / SUPABASE_SECRET_KEY from backend/.env. Never prints key values.
Exit code 0 = all checks passed.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import subprocess
import sys
from pathlib import Path

import httpx
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.legal.index import LocalIndex  # noqa: E402
from app.legal.manifest import load_manifest  # noqa: E402
from app.legal.supabase_sync import COMPARE_COLUMNS, SupabaseRest, plan_publish  # noqa: E402

BACKEND = Path(__file__).resolve().parents[1]
# (question as a user would type it, document ids that should appear in the top results)
SEARCH_CASES = [
    ("khula ke liye family court mein case kaise karein", {"PK-023", "PK-024"}),
    ("Punjab consumer court complaint about a defective product", {"PB-001"}),
    ("landlord evicting tenant in Karachi rent", {"SD-003"}),
    ("civil court pecuniary jurisdiction suit value Sindh", {"SD-001"}),
    ("minimum wage for a factory worker", {"PK-029", "PK-027"}),
]
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    results.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" - {detail}" if detail else ""))
    return ok


def key_kind(secret: str) -> str:
    if secret.startswith("sb_secret_"):
        return "secret"
    if secret.startswith("sb_publishable_"):
        return "publishable"
    parts = secret.split(".")
    if len(parts) == 3:  # legacy JWT key: read the role claim (no verification needed for this check)
        try:
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
            return "secret" if payload.get("role") == "service_role" else f"jwt role={payload.get('role')}"
        except ValueError:
            return "unknown"
    return "unknown"


def current_plan(api: SupabaseRest, chunks: list[dict]):
    remote = {r["chunk_id"]: r for r in api.select_all("legal_chunks", COMPARE_COLUMNS, "chunk_id")}
    remote_docs = {r["document_id"] for r in api.select_all("legal_documents", ["document_id"], "document_id")}
    manifest_ids = {r.document_id for r in load_manifest(settings.manifest_path)}
    return remote, plan_publish(chunks, remote, manifest_ids, remote_docs)


async def run_searches() -> None:
    from app.legal.search_service import search
    from app.schemas.search import SearchRequest

    settings.retrieval_backend = "supabase"  # production path only; no silent fallback to the local index
    for question, expected in SEARCH_CASES:
        response = await search(SearchRequest(query=question, limit=5, include_metadata_fallback=False))
        top = [r.document_id for r in response.results]
        check(f"search via Supabase: '{question[:45]}'",
              response.mode == "supabase-hybrid" and bool(expected & set(top)),
              f"mode={response.mode}, top={top}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--publish", action="store_true", help="publish to Supabase, then verify")
    args = parser.parse_args()

    url, secret = settings.supabase_url.rstrip("/"), settings.supabase_secret_key
    if not check("SUPABASE_URL set in backend/.env", bool(url)) or \
            not check("SUPABASE_SECRET_KEY set in backend/.env", bool(secret),
                      "add the service-role key (Dashboard > Project Settings > API keys)"):
        return 1
    kind = key_kind(secret)
    if not check("SUPABASE_SECRET_KEY is a server-side (service-role) key", kind == "secret", f"detected: {kind}"):
        return 1
    check("RETRIEVAL_BACKEND lets the backend use Supabase", settings.retrieval_backend in {"auto", "supabase"},
          f"RETRIEVAL_BACKEND={settings.retrieval_backend}")

    api = SupabaseRest(url, secret)
    headers = api.headers
    try:
        for table in ("legal_documents", "legal_chunks"):
            response = api.client.get(f"{api.base}/{table}", headers=headers | {"Prefer": "count=exact"},
                                      params={"select": "document_id", "limit": 1})
            total = response.headers.get("content-range", "?").split("/")[-1]
            check(f"table {table} reachable", response.status_code == 200, f"HTTP {response.status_code}, rows={total}")
        lexical = api.client.post(f"{api.base}/rpc/search_legal_chunks_lexical", headers=headers,
                                  json={"query_text": "bail", "match_count": 1})
        check("function search_legal_chunks_lexical (migration 005)", lexical.status_code == 200,
              f"HTTP {lexical.status_code} {lexical.text[:120] if lexical.status_code != 200 else ''}")
        probe = np.random.default_rng(0).normal(size=384)
        probe = probe / np.linalg.norm(probe)
        semantic = api.client.post(f"{api.base}/rpc/match_legal_chunks", headers=headers, json={
            "query_embedding": "[" + ",".join(f"{v:.6f}" for v in probe) + "]", "match_threshold": 0.0, "match_count": 1})
        check("function match_legal_chunks (pgvector, migration 003)", semantic.status_code == 200,
              f"HTTP {semantic.status_code} {semantic.text[:120] if semantic.status_code != 200 else ''}")

        index, _ = LocalIndex.load(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path)
        check("local index loaded with aligned embeddings", index.size > 0 and index.embeddings is not None,
              f"{index.size} chunks")
        remote, plan = current_plan(api, index.chunks)
        print("publish plan:", json.dumps({"remote_chunks": len(remote), **plan.summary()}))

        if args.publish:
            code = subprocess.call([sys.executable, "scripts/push_to_supabase.py"], cwd=BACKEND)
            check("push_to_supabase.py completed", code == 0, f"exit {code}")
            remote, plan = current_plan(api, index.chunks)
            check("Supabase matches the local index (second plan is empty)",
                  not plan.upsert and not plan.delete_chunks and not plan.drop_documents,
                  json.dumps(plan.summary()))
            check("remote chunk count equals local", len(remote) == index.size, f"{len(remote)} vs {index.size}")
            fresh = api.client.get(f"{api.base}/legal_documents", headers=headers | {"Prefer": "count=exact"},
                                   params={"select": "document_id", "metadata->>source_last_checked": "not.is.null",
                                           "limit": 1})
            check("documents carry an 'official source last checked' date",
                  fresh.status_code == 200, f"{fresh.headers.get('content-range', '?').split('/')[-1]} documents")
            asyncio.run(run_searches())
        elif remote:
            asyncio.run(run_searches())
    except httpx.HTTPError as exc:
        check("Supabase request", False, f"{type(exc).__name__}: {exc}")
    finally:
        api.close()

    failed = [name for name, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed" + (f"; failed: {failed}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
