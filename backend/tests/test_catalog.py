"""Catalog import: title normalisation and matching against official code listings (offline)."""
import csv
import json
from pathlib import Path

from app.core.config import settings
from app.legal.catalog import load_catalogs, match, name_key, year_of
from app.legal.manifest import destination, load_manifest
from app.legal.official_codes import Listing

CATALOG_DIR = settings.manifest_path.parent / "catalog"


def _listing(title: str, site: str = "pakistan_code", jurisdiction: str = "Federal") -> Listing:
    return Listing(site, jurisdiction, title, f"https://example.invalid/{title}")


def test_year_ignores_years_inside_site_notes():
    assert year_of("Customs Act, 1969 (Same as on the official website of FBR dated 30-06-2025)") == "1969"
    assert year_of("Industrial Relations Act, 2008 (Repealed by Act X of 2012)") == "2008"
    assert year_of("Khyber Pakhtunkhwa Land Revenue Act", "1967") == "1967"


def test_name_key_drops_province_prefix_abbreviation_and_plural():
    assert name_key("SIND RENTED PREMISES ORDINANCE, 1979") == name_key("Sindh Rented Premises Ordinance, 1979")
    assert name_key("SINDH CHILD MARRIAGES RESTRAINT ACT 2013") == name_key("Sindh Child Marriage Restraint Act, 2013")
    assert name_key("Code of Criminal Procedure, 1898 (CrPC)") == name_key("Code of Criminal Procedure, 1898")
    assert name_key("The West Pakistan Land- Revenue Act, 1967") == name_key("West Pakistan Land Revenue Act, 1967")
    # meaningful parentheses survive
    assert "restriction" in name_key("Dowry and Bridal Gifts (Restriction) Act, 1976")


def test_match_requires_same_year_and_rejects_repealed_versions():
    listings = [_listing("Industrial Relations Act, 2008 (Repealed by Act X of 2012)"),
                _listing("Industrial Relations Act, 2012")]
    targets, _, _ = load_catalogs([CATALOG_DIR / "pakistan_laws_master_dataset.json"])
    ira = next(t for t in targets if t.display_title == "Industrial Relations Act, 2012")
    assert [item.title for item in match(ira, listings)] == ["Industrial Relations Act, 2012"]


def test_catalog_portals_and_corrections_are_separated():
    targets, portals, skipped = load_catalogs(sorted(p for p in CATALOG_DIR.glob("*_dataset.json")))
    titles = {t.display_title for t in targets}
    assert "Right of Access to Information Act, 2017" in titles          # corrected from "Right to Information Act, 2002"
    assert "Workers' Welfare Fund Ordinance, 1971" in titles              # corrected year
    assert not any("—" in t for t in titles)                             # portal pages are not documents
    assert any("scp.gov.pk" in p["url"] for p in portals)
    assert [s["title"] for s in skipped] == ["Sindh Labour Policy / Labour Laws"]
    keys = [t.key for t in targets]
    assert len(keys) == len(set(keys))                                   # the two catalogs are deduplicated


def test_manifest_covers_every_province_with_official_pdfs():
    rows = load_manifest(settings.manifest_path)
    verified = [r for r in rows if r.status == "source_url_verified"]
    for jurisdiction in ("Federal", "Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan"):
        assert any(r.jurisdiction == jurisdiction for r in verified), jurisdiction
    assert all(r.is_official_host and r.acquirable for r in verified)
    assert len({r.document_id for r in rows}) == len(rows)


def test_new_provinces_get_their_own_corpus_folders(tmp_path: Path):
    rows = {r.document_id: r for r in load_manifest(settings.manifest_path)}
    assert destination(tmp_path, rows["PB-001"]).parent.name == "punjab_laws"
    assert destination(tmp_path, rows["KP-001"]).parent.name == "kp_laws"
    assert destination(tmp_path, rows["BL-001"]).parent.name == "balochistan_laws"
    assert destination(tmp_path, rows["PK-021"]).parent.name == "federal_laws"


def test_import_report_matches_manifest():
    report = json.loads((CATALOG_DIR / "import_report.json").read_text(encoding="utf-8"))
    with settings.manifest_path.open(encoding="utf-8-sig") as handle:
        manifest = {row["document_id"]: row for row in csv.DictReader(handle)}
    for record in report["resolved"]:
        assert manifest[record["document_id"]]["source_url"] == record["pdf_url"]
