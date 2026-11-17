"""Export the research report's tables to CSV/JSON, validate them, and (optionally) check every link.

    python scripts/export_research_data.py                 # parse + validate, write docs/research/data/
    python scripts/export_research_data.py --check-links   # ...and record HTTP status for every URL

Inputs:  docs/research/reports/Pakistan case law and statute sources.md
         frontend/data/sources/official_sources.csv   (the pipeline's source registry is link-checked too)
Outputs: docs/research/data/*.csv, research_repository.json, validation_report.json, link_check.csv

The report stays the human-readable master; these files are regenerated from it, never edited by hand.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402

from app.legal.acquisition import ssl_context  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
REPORT = REPO / "docs" / "research" / "reports" / "Pakistan case law and statute sources.md"
REGISTRY = REPO / "frontend" / "data" / "sources" / "official_sources.csv"
OUT = REPO / "docs" / "research" / "data"
USER_AGENT = "PakistanJusticeNavigator/0.3 (+research link check; contact via project maintainers)"

# Report section heading prefix -> output dataset name
DATASETS = {
    "B1": "source_directory", "B2": "source_directory", "B3": "source_directory", "B4": "source_directory",
    "B5": "source_directory",
    "C1": "extracted_courts", "C2": "extracted_tribunals", "C3": "extracted_statute_portals",
    "C4": "extracted_third_party_datasets", "C5": "extracted_legal_provisions",
    "Part D": "evidence", "E1": "gap_federal_ict_punjab_sindh", "E2": "gap_inaccessible_sources",
    "E3": "gap_open_questions", "Part F": "actions",
}
URL_RE = re.compile(r"https?://[^\s|<>\"'`\]]+")
# Different report tables name the same column differently; normalise so no values are dropped.
COLUMN_ALIASES = {"Owner": "Organisation", "Organisation/owner": "Organisation", "Date": "Date / last updated"}


def urls_in(text: str) -> list[str]:
    """URLs in a cell, without trailing punctuation or an unbalanced closing parenthesis."""
    out = []
    for url in URL_RE.findall(text):
        url = url.rstrip(".,;")
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
        out.append(url)
    return out
# Hosts whose robots rules ask automated agents to stay away: never fetched by the link checker.
DO_NOT_FETCH = {"scp.gov.pk", "www.scp.gov.pk", "supremecourt.gov.pk", "www.supremecourt.gov.pk",
                "digital.shc.gov.pk", "printing.balochistan.gov.pk"}
DO_NOT_FETCH_PATHS = [("bhc.gov.pk", "/media/")]


def clean(cell: str) -> str:
    cell = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 \2", cell)  # markdown links -> "text url"
    return re.sub(r"\s+", " ", cell.replace("`", "").replace("**", "")).strip()


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [clean(c) for c in body.split("|")]


def parse_tables(markdown: str) -> list[dict]:
    """Return [{"section", "heading", "columns", "rows"}] for every pipe table, tagged with its section."""
    tables, heading, section = [], "", ""
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            match = re.match(r"([A-F]\d)\.", heading)
            part = re.match(r"(Part [A-F])\b", heading)
            section = match.group(1) if match else (part.group(1) if part else section if line.startswith("###") else "")
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
            columns = split_row(line)
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = split_row(lines[i])
                cells += [""] * (len(columns) - len(cells))
                rows.append(dict(zip(columns, cells[:len(columns)])))
                i += 1
            tables.append({"section": section, "heading": heading, "columns": columns, "rows": rows})
            continue
        i += 1
    return tables


def to_csv(columns: list[str], rows: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def validate(datasets: dict[str, list[dict]]) -> list[dict]:
    problems = []
    seen_urls: dict[str, int] = {}
    for index, row in enumerate(datasets.get("source_directory", []), start=1):
        url = row.get("URL", "")
        for required in ("Title", "URL", "Organisation", "Credibility", "Access status"):
            if not row.get(required):
                problems.append({"dataset": "source_directory", "row": index, "field": required, "problem": "empty"})
        if url and urls_in(url) != [url]:
            problems.append({"dataset": "source_directory", "row": index, "field": "URL",
                             "problem": f"not a single absolute URL: {url[:80]}"})
        if url in seen_urls:
            problems.append({"dataset": "source_directory", "row": index, "field": "URL",
                             "problem": f"duplicate of row {seen_urls[url]}"})
        seen_urls.setdefault(url, index)
    for index, row in enumerate(datasets.get("evidence", []), start=1):
        if not urls_in(row.get("Source URL(s)", "")):
            problems.append({"dataset": "evidence", "row": index, "field": "Source URL(s)", "problem": "no URL"})
    return problems


def fetch_allowed(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host in DO_NOT_FETCH:
        return False
    return not any(host.endswith(h) and parsed.path.startswith(p) for h, p in DO_NOT_FETCH_PATHS)


def check_links(urls: list[str], delay: float) -> dict[str, dict]:
    results: dict[str, dict] = {}
    client = httpx.Client(timeout=30, follow_redirects=True, verify=ssl_context(), headers={"User-Agent": USER_AGENT})
    last_host_hit: dict[str, float] = {}
    try:
        for url in urls:
            checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if not fetch_allowed(url):
                results[url] = {"status": "", "final_url": "", "error": "not fetched: robots/AI-crawl restrictions",
                                "checked_at": checked_at}
                continue
            host = urlparse(url).hostname or ""
            wait = delay - (time.time() - last_host_hit.get(host, 0))
            if wait > 0:
                time.sleep(wait)
            try:
                response = client.head(url)
                if response.status_code in (405, 403, 400, 404, 501) or response.status_code >= 500:
                    response = client.get(url, headers={"Range": "bytes=0-2047"})
                results[url] = {"status": response.status_code, "final_url": str(response.url), "error": "",
                                "checked_at": checked_at}
            except httpx.HTTPError as exc:
                results[url] = {"status": "", "final_url": "", "error": f"{type(exc).__name__}: {str(exc)[:120]}",
                                "checked_at": checked_at}
            last_host_hit[host] = time.time()
    finally:
        client.close()
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-links", action="store_true")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between requests to the same host")
    args = parser.parse_args()

    tables = parse_tables(REPORT.read_text(encoding="utf-8"))
    datasets: dict[str, list[dict]] = {}
    columns: dict[str, list[str]] = {}
    for table in tables:
        name = DATASETS.get(table["section"])
        if not name:
            continue
        table_columns = [COLUMN_ALIASES.get(c, c) for c in table["columns"]]
        cols = columns.setdefault(name, ["section"] if name == "source_directory" else [])
        cols += [c for c in table_columns if c not in cols]  # union of columns across tables
        for row in table["rows"]:
            row = {COLUMN_ALIASES.get(k, k): v for k, v in row.items()}
            datasets.setdefault(name, []).append(({"section": table["heading"]} if name == "source_directory" else {})
                                                 | row)
    if "source_directory" not in datasets or "evidence" not in datasets:
        print("Could not find Part B / Part D tables in the report", file=sys.stderr)
        return 1

    problems = validate(datasets)
    link_rows: list[dict] = []
    if args.check_links:
        urls: list[tuple[str, str, str]] = []  # (url, dataset, label)
        for row in datasets["source_directory"]:
            urls += [(u, "source_directory", row["Title"]) for u in urls_in(row["URL"])]
        for row in datasets["evidence"]:
            urls += [(u, "evidence", row.get("#", "")) for u in urls_in(row["Source URL(s)"])]
        with REGISTRY.open(encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                for column in ("home_url", "listing_url", "new_items_url"):
                    value = row[column].split(" ")[0]
                    if urls_in(value) == [value] and "{" not in value:
                        urls.append((value, f"registry.{column}", row["source_id"]))
        unique = list(dict.fromkeys(u for u, _, _ in urls))
        print(f"Checking {len(unique)} unique URLs ...")
        results = check_links(unique, args.delay)
        for url, dataset, label in urls:
            link_rows.append({"dataset": dataset, "label": label, "url": url, **results[url]})
        status_of = {u: r for u, r in results.items()}
        for row in datasets["source_directory"]:
            first = (urls_in(row["URL"]) or [""])[0]
            result = status_of.get(first, {})
            row.update({"http_status": result.get("status", ""), "final_url": result.get("final_url", ""),
                        "check_error": result.get("error", ""), "checked_at": result.get("checked_at", "")})
        columns["source_directory"] += ["http_status", "final_url", "check_error", "checked_at"]

    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in datasets.items():
        (OUT / f"{name}.csv").write_text(to_csv(columns[name], rows), encoding="utf-8", newline="")
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    repository = {"generated_at": generated, "report": str(REPORT.relative_to(REPO)).replace("\\", "/"),
                  "datasets": {name: {"columns": columns[name], "rows": rows} for name, rows in datasets.items()}}
    (OUT / "research_repository.json").write_text(json.dumps(repository, indent=1, ensure_ascii=False) + "\n",
                                                  encoding="utf-8")
    summary = {"generated_at": generated, "rows": {n: len(r) for n, r in datasets.items()}, "problems": problems}
    if link_rows:
        (OUT / "link_check.csv").write_text(to_csv(["dataset", "label", "url", "status", "final_url", "error",
                                                    "checked_at"], link_rows), encoding="utf-8", newline="")
        ok = sum(1 for r in link_rows if isinstance(r["status"], int) and r["status"] < 400)
        summary["links"] = {"checked": len(link_rows), "ok": ok,
                            "not_fetched": sum(1 for r in link_rows if r["error"].startswith("not fetched")),
                            "failed": [{"url": r["url"], "status": r["status"], "error": r["error"]}
                                       for r in link_rows if not (isinstance(r["status"], int) and r["status"] < 400)
                                       and not r["error"].startswith("not fetched")]}
    (OUT / "validation_report.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                                                encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "links"} | (
        {"links": {k: v for k, v in summary["links"].items() if k != "failed"}} if "links" in summary else {}),
        indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
