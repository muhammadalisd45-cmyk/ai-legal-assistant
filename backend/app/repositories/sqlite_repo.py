"""SQLite case store for local development and single-node deployments.

Schema mirrors supabase/migrations (cases, case_messages, case_documents). Ownership is enforced in every
query (`user_id = ?`), the application-level equivalent of the Postgres RLS policies.
"""
from __future__ import annotations

import asyncio
import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.security import CurrentUser
from app.repositories.base import CaseRepository, ConflictError, new_public_case_id, parse_uuid

SCHEMA = """
pragma foreign_keys = on;
create table if not exists cases (
  id text primary key,
  user_id text not null,
  public_case_id text not null unique,
  language text not null default 'en' check (language in ('en','roman-ur','ur')),
  category text,
  summary text,
  urgency text check (urgency is null or urgency in ('low','medium','high','critical','unknown')),
  status text not null default 'intake' check (status in ('intake','analysis','ready_for_lawyer','closed')),
  raw_description text not null,
  structured_payload text not null default '{}',
  created_at text not null,
  updated_at text not null
);
create index if not exists idx_cases_user on cases(user_id, updated_at desc);
create table if not exists case_messages (
  id text primary key,
  case_id text not null references cases(id) on delete cascade,
  role text not null check (role in ('citizen','assistant','system')),
  language text not null default 'en',
  content text not null,
  metadata text not null default '{}',
  created_at text not null
);
create index if not exists idx_messages_case on case_messages(case_id, created_at);
create table if not exists case_documents (
  id text primary key,
  case_id text not null references cases(id) on delete cascade,
  storage_path text not null,
  original_file_name text not null,
  mime_type text,
  status text not null default 'uploaded' check (status in ('uploaded','queued','processing','analyzed','failed')),
  size_bytes integer,
  sha256 text,
  page_count integer,
  error text,
  analysis_payload text not null default '{}',
  created_at text not null,
  updated_at text not null
);
create index if not exists idx_documents_case on case_documents(case_id, created_at);
"""

CASE_COLUMNS = ("id", "public_case_id", "language", "category", "summary", "urgency", "status",
                "raw_description", "structured_payload", "created_at", "updated_at")
UPDATABLE_CASE = {"category", "summary", "urgency", "status", "structured_payload"}
UPDATABLE_DOC = {"status", "page_count", "error", "analysis_payload", "mime_type", "sha256", "size_bytes"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SQLiteCaseRepository(CaseRepository):
    name = "sqlite"

    def __init__(self, path: Path | str):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        with self._lock:
            self._conn.executescript(SCHEMA)
            if self.path != ":memory:":
                self._conn.execute("pragma journal_mode = wal")

    # ---- helpers -------------------------------------------------------
    def _run(self, fn, *args):
        def locked():
            with self._lock:
                return fn(*args)

        return asyncio.to_thread(locked)

    @staticmethod
    def _case(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        data = {key: row[key] for key in CASE_COLUMNS}
        data["structured_payload"] = json.loads(data["structured_payload"] or "{}")
        return data

    @staticmethod
    def _doc(row: sqlite3.Row | None) -> dict[str, Any] | None:
        if row is None:
            return None
        data = dict(row)
        data["analysis_payload"] = json.loads(data.get("analysis_payload") or "{}")
        return data

    def _owned_case_row(self, user_id: str, case_ref: str) -> sqlite3.Row | None:
        as_uuid = parse_uuid(case_ref)
        if as_uuid:
            return self._conn.execute("select * from cases where id = ? and user_id = ?", (as_uuid, user_id)).fetchone()
        return self._conn.execute("select * from cases where public_case_id = ? and user_id = ?",
                                  (case_ref, user_id)).fetchone()

    # ---- cases ---------------------------------------------------------
    async def create_case(self, user: CurrentUser, data: dict[str, Any]) -> dict[str, Any]:
        def op():
            now = _now()
            public_id = data.get("public_case_id") or new_public_case_id()
            row_id = str(uuid.uuid4())
            try:
                self._conn.execute(
                    "insert into cases (id, user_id, public_case_id, language, category, summary, urgency, status, "
                    "raw_description, structured_payload, created_at, updated_at) values (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (row_id, user.id, public_id, data.get("language", "en"), data.get("category"), data.get("summary"),
                     data.get("urgency"), data.get("status", "intake"), data["raw_description"],
                     json.dumps(data.get("structured_payload") or {}, ensure_ascii=False, default=str), now, now),
                )
            except sqlite3.IntegrityError as exc:
                raise ConflictError("public_case_id already exists") from exc
            return self._case(self._conn.execute("select * from cases where id = ?", (row_id,)).fetchone())

        return await self._run(op)

    async def list_cases(self, user: CurrentUser, limit: int, offset: int) -> list[dict[str, Any]]:
        def op():
            rows = self._conn.execute(
                "select * from cases where user_id = ? order by updated_at desc limit ? offset ?",
                (user.id, limit, offset)).fetchall()
            return [self._case(row) for row in rows]

        return await self._run(op)

    async def get_case(self, user: CurrentUser, case_ref: str) -> dict[str, Any] | None:
        return await self._run(lambda: self._case(self._owned_case_row(user.id, case_ref)))

    async def update_case(self, user: CurrentUser, case_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        def op():
            fields = {k: v for k, v in patch.items() if k in UPDATABLE_CASE}
            row = self._owned_case_row(user.id, case_id)
            if row is None:
                return None
            if fields:
                if "structured_payload" in fields:
                    fields["structured_payload"] = json.dumps(fields["structured_payload"], ensure_ascii=False, default=str)
                fields["updated_at"] = _now()
                assignments = ", ".join(f"{key} = ?" for key in fields)
                self._conn.execute(f"update cases set {assignments} where id = ? and user_id = ?",
                                   (*fields.values(), row["id"], user.id))
            return self._case(self._conn.execute("select * from cases where id = ?", (row["id"],)).fetchone())

        return await self._run(op)

    # ---- messages ------------------------------------------------------
    async def add_message(self, user: CurrentUser, case_id: str, data: dict[str, Any]) -> dict[str, Any]:
        def op():
            row = self._owned_case_row(user.id, case_id)
            if row is None:
                raise LookupError("case not found")
            msg_id, now = str(uuid.uuid4()), _now()
            self._conn.execute(
                "insert into case_messages (id, case_id, role, language, content, metadata, created_at) values (?,?,?,?,?,?,?)",
                (msg_id, row["id"], data["role"], data.get("language", "en"), data["content"],
                 json.dumps(data.get("metadata") or {}, ensure_ascii=False, default=str), now))
            self._conn.execute("update cases set updated_at = ? where id = ?", (now, row["id"]))
            return {"id": msg_id, "case_id": row["id"], "role": data["role"], "language": data.get("language", "en"),
                    "content": data["content"], "metadata": data.get("metadata") or {}, "created_at": now}

        return await self._run(op)

    async def list_messages(self, user: CurrentUser, case_id: str, limit: int) -> list[dict[str, Any]]:
        def op():
            row = self._owned_case_row(user.id, case_id)
            if row is None:
                raise LookupError("case not found")
            rows = self._conn.execute(
                "select * from case_messages where case_id = ? order by created_at asc limit ?", (row["id"], limit)).fetchall()
            out = []
            for item in rows:
                data = dict(item)
                data["metadata"] = json.loads(data["metadata"] or "{}")
                out.append(data)
            return out

        return await self._run(op)

    # ---- documents -----------------------------------------------------
    async def add_document(self, user: CurrentUser, case_id: str, data: dict[str, Any]) -> dict[str, Any]:
        def op():
            row = self._owned_case_row(user.id, case_id)
            if row is None:
                raise LookupError("case not found")
            doc_id = data.get("id") or str(uuid.uuid4())
            now = _now()
            self._conn.execute(
                "insert into case_documents (id, case_id, storage_path, original_file_name, mime_type, status, size_bytes, "
                "sha256, page_count, error, analysis_payload, created_at, updated_at) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (doc_id, row["id"], data["storage_path"], data["original_file_name"], data.get("mime_type"),
                 data.get("status", "queued"), data.get("size_bytes"), data.get("sha256"), data.get("page_count"),
                 data.get("error"), json.dumps(data.get("analysis_payload") or {}, ensure_ascii=False), now, now))
            return self._doc(self._conn.execute("select * from case_documents where id = ?", (doc_id,)).fetchone())

        return await self._run(op)

    def _owned_doc_row(self, user_id: str, document_id: str, case_id: str | None = None):
        doc_uuid = parse_uuid(document_id)
        if not doc_uuid:
            return None
        sql = ("select d.* from case_documents d join cases c on c.id = d.case_id "
               "where d.id = ? and c.user_id = ?")
        params: list[Any] = [doc_uuid, user_id]
        if case_id is not None:
            sql += " and d.case_id = ?"
            params.append(case_id)
        return self._conn.execute(sql, params).fetchone()

    async def update_document(self, user: CurrentUser, document_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        def op():
            row = self._owned_doc_row(user.id, document_id)
            if row is None:
                return None
            fields = {k: v for k, v in patch.items() if k in UPDATABLE_DOC}
            if "analysis_payload" in fields:
                fields["analysis_payload"] = json.dumps(fields["analysis_payload"], ensure_ascii=False, default=str)
            fields["updated_at"] = _now()
            assignments = ", ".join(f"{key} = ?" for key in fields)
            self._conn.execute(f"update case_documents set {assignments} where id = ?", (*fields.values(), row["id"]))
            return self._doc(self._conn.execute("select * from case_documents where id = ?", (row["id"],)).fetchone())

        return await self._run(op)

    async def list_documents(self, user: CurrentUser, case_id: str) -> list[dict[str, Any]]:
        def op():
            row = self._owned_case_row(user.id, case_id)
            if row is None:
                raise LookupError("case not found")
            rows = self._conn.execute("select * from case_documents where case_id = ? order by created_at desc",
                                      (row["id"],)).fetchall()
            return [self._doc(item) for item in rows]

        return await self._run(op)

    async def get_document(self, user: CurrentUser, case_id: str, document_id: str) -> dict[str, Any] | None:
        def op():
            case_row = self._owned_case_row(user.id, case_id)
            if case_row is None:
                return None
            return self._doc(self._owned_doc_row(user.id, document_id, case_row["id"]))

        return await self._run(op)

    async def health(self) -> dict[str, Any]:
        try:
            await self._run(lambda: self._conn.execute("select 1").fetchone())
            return {"store": self.name, "ok": True}
        except sqlite3.Error as exc:
            return {"store": self.name, "ok": False, "error": type(exc).__name__}
