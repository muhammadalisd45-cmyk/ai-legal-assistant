"""Read and write the corpus manifest and every file derived from it.

The manifest (frontend/data/member4_manifest.csv) is the single source of truth. Whenever it changes, the
derived copies must be rewritten together so the backend, frontend and Supabase seed never disagree:

  member4_manifest.json, legal_documents.csv/.json (source library), supabase/seed.sql
"""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from app.core.config import settings
from app.legal.catalog import ID_PREFIX

DATA_DIR = settings.manifest_path.parent
SEED_PATH = DATA_DIR.parent / "supabase" / "seed.sql"
DIRECTORY_FIELDS = ["document_id", "title", "document_type", "jurisdiction", "authority", "source_name", "source_url",
                    "priority"]
ID_ORDER = {"PK": 0, "PB": 1, "SD": 2, "KP": 3, "BL": 4}


def newline_of(path: Path) -> str:
    return "\r\n" if path.exists() and b"\r\n" in path.read_bytes()[:4096] else "\n"


def write_text(path: Path, text: str) -> None:
    """Write UTF-8 text, keeping the file's existing line endings so diffs stay minimal."""
    newline = newline_of(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", newline).encode("utf-8"))


def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    if not path.exists():
        return [], []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def read_manifest(path: Path | None = None) -> tuple[list[str], list[dict]]:
    return read_csv(path or settings.manifest_path)


def csv_text(fields: list[str], rows: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def _sql(value: str | None) -> str:
    if value is None or value == "":
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def seed_sql(rows: list[dict]) -> str:
    values = []
    for row in rows:
        meta = json.dumps({"source_name": row["source_name"], "priority": row["priority"]}, ensure_ascii=False,
                          separators=(",", ":"))
        values.append("(" + ", ".join([
            _sql(row["document_id"]), _sql(row["title"]), _sql(row["document_type"]), _sql(row["jurisdiction"]),
            _sql(row["court"]), _sql(row["bench"]), _sql(row["authority"]), _sql(row["citation"]),
            _sql(row["case_number"]), _sql(row["case_year"]), _sql(row["date"]), _sql(row["section_or_article"]),
            _sql(row["parties"]), _sql(row["language"]), _sql(row["source_url"]), _sql(row["file_name"]),
            _sql(row["status"]), str(int(row["source_tier"] or 1)), _sql(meta) + "::jsonb"]) + ")")
    return (
        "-- Generated from data/member4_manifest.csv\n"
        "-- Tier-1 starter registry. Placeholder judgments remain quarantined and are not evidence.\n\n"
        "insert into public.legal_documents\n"
        "(document_id, title, document_type, jurisdiction, court, bench, authority, citation, case_number, case_year, "
        "document_date, section_or_article, parties, language, source_url, file_name, status, source_tier, metadata)\n"
        "values\n" + ",\n".join(values) + "\n"
        "on conflict (document_id) do update set\n"
        "  title = excluded.title, document_type = excluded.document_type, jurisdiction = excluded.jurisdiction,\n"
        "  court = excluded.court, bench = excluded.bench, authority = excluded.authority, citation = excluded.citation,\n"
        "  case_number = excluded.case_number, case_year = excluded.case_year, document_date = excluded.document_date,\n"
        "  section_or_article = excluded.section_or_article, parties = excluded.parties, language = excluded.language,\n"
        "  source_url = excluded.source_url, file_name = excluded.file_name, status = excluded.status,\n"
        "  source_tier = excluded.source_tier, metadata = excluded.metadata;\n"
    )


def next_id(rows: list[dict], jurisdiction: str) -> str:
    prefix = ID_PREFIX[jurisdiction]
    used = [int(r["document_id"].split("-")[1]) for r in rows if r["document_id"].startswith(prefix + "-")
            and r["document_id"].split("-")[1].isdigit()]
    return f"{prefix}-{(max(used) if used else 0) + 1:03d}"


def sort_rows(rows: list[dict]) -> None:
    rows.sort(key=lambda r: (ID_ORDER.get(r["document_id"].split("-")[0], 9), r["document_id"]))


def write_manifest(fields: list[str], rows: list[dict]) -> None:
    """Write the manifest CSV and all derived files in one go."""
    sort_rows(rows)
    write_text(settings.manifest_path, csv_text(fields, rows))
    write_text(DATA_DIR / "member4_manifest.json", json.dumps(rows, indent=2, ensure_ascii=False) + "\n")
    directory = [{key: row[key] for key in DIRECTORY_FIELDS} for row in rows]
    write_text(DATA_DIR / "legal_documents.csv", csv_text(DIRECTORY_FIELDS, directory))
    write_text(DATA_DIR / "legal_documents.json", json.dumps(directory, indent=2, ensure_ascii=False) + "\n")
    write_text(SEED_PATH, seed_sql(rows))
