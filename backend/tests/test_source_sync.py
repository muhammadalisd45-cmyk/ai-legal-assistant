"""Source sync pipeline: change detection, safety guards and ingest policy (offline, fake adapter)."""
import csv
import json

import numpy as np
import pytest

from app.legal import official_codes, source_sync
from app.legal.auto_ingest import apply_plan, display_title, eligibility, plan_ingest
from app.legal.index import embedding_key, previous_vectors, write_index
from app.legal.official_codes import Listing
from app.legal.source_sync import Source, instrument_type, load_registry, parse_meta, run_sync

FAKE_PAGES: dict[str, list[Listing]] = {"current": []}


def fake_adapter(_fetcher):
    return list(FAKE_PAGES["current"])


def law(n: int, title: str, meta: str = "Civil Laws | I of 2020 | Promulgation Date: Jan 1 2020 | Views: 10",
        pdf: str | None = None) -> Listing:
    url = f"https://sindhlaws.gov.pk/setup/Publications_SindhCode/PUB-{n}.pdf"
    return Listing("fake", "Sindh", title, url, pdf_url=pdf or url, meta=meta)


@pytest.fixture()
def sync_env(tmp_path, monkeypatch):
    monkeypatch.setitem(official_codes.SITES, "fake", fake_adapter)
    monkeypatch.setitem(source_sync.SITES, "fake", fake_adapter)
    for name, filename in [("INVENTORY_CSV", "law_inventory.csv"), ("INVENTORY_JSON", "law_inventory.json"),
                           ("CHANGES_CSV", "changes.csv"), ("STATE_PATH", "sync_state.json")]:
        monkeypatch.setattr(source_sync, name, tmp_path / filename)
    monkeypatch.setattr(source_sync, "CHANGES_DIR", tmp_path / "changes")
    # Direct-PDF adapters skip detail-page resolution, so no network is touched.
    monkeypatch.setattr(source_sync, "to_listing", lambda row, src: Listing("fake", row["jurisdiction"], row["title"],
                                                                         row["detail_url"], pdf_url=row["pdf_url"]))
    monkeypatch.setattr(source_sync, "pdf_url", lambda _f, listing: listing.pdf_url)
    source = Source("fake_code", "Fake", "Sindh", "statutes", 1, "https://x", "fake", "open", "weekly", True, True)
    return source, tmp_path


def run(source, date):
    return run_sync([source], run_date=date, manifest_rows=[])


def test_first_crawl_is_a_baseline_then_new_laws_are_reported(sync_env):
    source, tmp = sync_env
    FAKE_PAGES["current"] = [law(1, "Sindh Alpha Act, 2020"), law(2, "Sindh Beta Act, 2021")]
    report = run(source, "2026-01-01")
    assert report.changes == [] and report.sources["fake_code"]["baseline"] is True
    FAKE_PAGES["current"].append(law(3, "Sindh Gamma Act, 2026"))
    report = run(source, "2026-01-08")
    assert [(c["change"], c["title"]) for c in report.changes] == [("new", "Sindh Gamma Act, 2026")]
    rows = list(csv.DictReader((tmp / "law_inventory.csv").open(encoding="utf-8")))
    assert len(rows) == 3 and all(r["pdf_url"].endswith(".pdf") for r in rows)
    assert json.loads((tmp / "changes" / "2026-01-08.json").read_text(encoding="utf-8"))[0]["change"] == "new"


def test_view_counter_changes_are_not_changes_but_real_edits_are(sync_env):
    source, _ = sync_env
    FAKE_PAGES["current"] = [law(1, "Sindh Alpha Act, 2020")]
    run(source, "2026-01-01")
    FAKE_PAGES["current"] = [law(1, "Sindh Alpha Act, 2020", meta="Civil Laws | I of 2020 | Promulgation Date: "
                                                                 "Jan 1 2020 | Views: 99999")]
    assert run(source, "2026-01-02").changes == []
    FAKE_PAGES["current"] = [law(1, "Sindh Alpha Act, 2020", meta="Civil Laws | I of 2020 | Promulgation Date: "
                                                                 "Jan 1 2020 | Last Updated On: Feb 2 2026")]
    assert [c["change"] for c in run(source, "2026-01-03").changes] == ["listing_changed"]


def test_new_pdf_link_is_a_pdf_change(sync_env):
    source, _ = sync_env
    FAKE_PAGES["current"] = [law(1, "Sindh Alpha Act, 2020")]
    run(source, "2026-01-01")
    FAKE_PAGES["current"] = [law(1, "Sindh Alpha Act, 2020", pdf="https://sindhlaws.gov.pk/setup/new-version.pdf")]
    changes = run(source, "2026-01-02").changes
    assert [c["change"] for c in changes] == ["pdf_changed"]
    assert changes[0]["previous"].endswith("PUB-1.pdf")


def test_partial_crawl_never_marks_laws_removed(sync_env):
    source, tmp = sync_env
    FAKE_PAGES["current"] = [law(i, f"Sindh Law {i} Act, 2020") for i in range(10)]
    run(source, "2026-01-01")
    FAKE_PAGES["current"] = FAKE_PAGES["current"][:3]          # site outage: 3 of 10 listed
    report = run(source, "2026-01-02")
    assert report.sources["fake_code"]["partial"] is True and report.changes == []
    FAKE_PAGES["current"] = [law(i, f"Sindh Law {i} Act, 2020") for i in range(9)]   # one genuinely gone
    assert [c["change"] for c in run(source, "2026-01-03").changes] == ["removed"]
    rows = {r["title"]: r for r in csv.DictReader((tmp / "law_inventory.csv").open(encoding="utf-8"))}
    assert rows["Sindh Law 9 Act, 2020"]["removed"] == "true"


def test_metadata_parsing_and_instrument_types():
    meta = parse_meta("Higher Education | Act LXXI of 2025 | Promulgation Date: Mon Aug 11, 2025 | Views: 3 | "
                      "Last Updated On: Tue Sep 02, 2025")
    assert meta["act_number"] == "Act LXXI of 2025" and meta["category"] == "Higher Education"
    assert meta["promulgation_date"] == "Mon Aug 11, 2025" and meta["source_last_updated"] == "Tue Sep 02, 2025"
    sja = parse_meta("Sindh Judicial Academy consolidation | amended up to: Sindh Act No. VI of 2025")
    assert sja["act_number"] == "" and sja["site_status"].startswith("Consolidated")
    assert instrument_type("Qanun-e-Shahadat Order, 1984") == "Order"
    assert instrument_type("Sindh Public Procurement Rules, 2010") == "Rules"
    assert instrument_type("THE PUNJAB LAND REVENUE ACT, 1967") == "Act"
    # parenthetical notes must not decide the type (regressions found on the real 5,572-law inventory)
    assert instrument_type("Hajj and Umrah (Regulation) Act, 2024") == "Act"
    assert instrument_type("Boilers Act, 1923(Repeal by Ord. 52 of 2001, s,610)") == "Act"
    assert instrument_type("Code of Civil Procedure (Order XXXIX)") == "Code"
    assert instrument_type("Punjab Ordnance Factories Board Act") == "Act"
    assert instrument_type("Balochistan Ordianace X of 1981") == "Ordinance"          # site misspelling
    assert instrument_type("Agriculture Dept CRS (1-15) Agric-SR") == "Rules"         # Service Rules


def _inv(**over):
    row = {"law_key": "k", "source_id": "punjab_code", "jurisdiction": "Punjab", "title": "PUNJAB NEW ACT 2026",
           "year": "2026", "instrument_type": "Act", "is_amendment": "false", "site_marked_repealed": "false",
           "removed": "false", "pdf_url": "https://punjabcode.punjab.gov.pk/uploads/articles/new.pdf",
           "manifest_id": ""}
    row.update(over)
    return row


def test_ingest_eligibility_rules():
    assert eligibility(_inv()) == ""
    assert "amendment" in eligibility(_inv(is_amendment="true"))
    assert "repealed" in eligibility(_inv(site_marked_repealed="true"))
    assert "Rules" in eligibility(_inv(instrument_type="Rules"))
    assert "official" in eligibility(_inv(pdf_url="https://example.com/x.pdf"))
    assert "no direct PDF" in eligibility(_inv(pdf_url=""))


def test_plan_adds_new_principal_law_once_and_updates_changed_pdfs():
    registry = {s.source_id: s for s in load_registry()}
    manifest = [{"document_id": "PB-001", "title": "Punjab Consumer Protection Act, 2005", "jurisdiction": "Punjab",
                 "status": "source_url_verified", "court": "", "source_url": "https://punjabcode.punjab.gov.pk/old.pdf",
                 "file_name": "punjab_consumer_protection_act_2005.pdf"}]
    inventory = {"new": _inv(law_key="new"),
                 "dup": _inv(law_key="dup", title="PUNJAB CONSUMER PROTECTION ACT 2005", year="2005"),
                 "amend": _inv(law_key="amend", title="PUNJAB CONSUMER PROTECTION (AMENDMENT) ACT 2026",
                               is_amendment="true"),
                 "chg": _inv(law_key="chg", manifest_id="PB-001",
                             pdf_url="https://punjabcode.punjab.gov.pk/uploads/articles/v2.pdf")}
    changes = [{"law_key": k, "change": c} for k, c in
               [("new", "new"), ("dup", "new"), ("amend", "new"), ("chg", "pdf_changed")]]
    plan = plan_ingest(changes, inventory, registry, manifest)
    assert [r["law_key"] for r in plan.add] == ["new"]
    assert plan.update == [("PB-001", inventory["chg"]["pdf_url"], "chg")]
    assert plan.linked_amendments == [("PUNJAB CONSUMER PROTECTION (AMENDMENT) ACT 2026", "PB-001")]
    fields = ["document_id", "title", "document_type", "jurisdiction", "court", "authority", "source_name",
              "source_url", "file_name", "status", "priority", "source_tier", "language"]
    rows = [dict({f: "" for f in fields}, **manifest[0])]
    added, updated = apply_plan(plan, fields, rows, registry)
    assert added == ["PB-002"] and updated == ["PB-001"]
    assert rows[-1]["title"] == "Punjab New Act 2026" and rows[-1]["status"] == "source_url_verified"


def test_display_title_keeps_roman_numerals():
    assert display_title("THE SINDH CIVIL COURTS (AMENDMENT) ACT, 2025") == "The Sindh Civil Courts (Amendment) Act, 2025"
    assert display_title("WEST PAKISTAN ACT XVII OF 1967") == "West Pakistan Act XVII of 1967"


def test_registry_is_well_formed():
    sources = load_registry()
    ids = [s.source_id for s in sources]
    assert len(ids) == len(set(ids))
    for s in sources:
        assert s.listing_url.startswith("http") and s.collection_status in {
            "open", "open_courtesy_request", "needs_permission", "blocked", "unavailable"}
        if s.syncable:
            assert s.content_type == "statutes"
    assert not any(s.syncable for s in sources if s.collection_status in {"blocked", "needs_permission"})


def test_incremental_index_reuses_unchanged_vectors(tmp_path):
    class Counting:
        name = "counting-384"
        calls = 0

        def embed(self, texts):
            Counting.calls += len(texts)
            return np.ones((len(texts), 384), dtype=np.float32)

    def chunk(i, text):
        return {"chunk_id": f"c{i}", "document_id": "D", "title": "T", "section_or_article": "", "section_heading": "",
                "content": text, "content_hash": text}

    paths = (tmp_path / "c.jsonl", tmp_path / "e.npy", tmp_path / "m.json")
    write_index([chunk(1, "alpha"), chunk(2, "beta")], *paths, Counting(), log=lambda *_: None)
    assert Counting.calls == 2
    reuse = previous_vectors(*paths, "counting-384")
    assert set(reuse) == {embedding_key(chunk(1, "alpha")), embedding_key(chunk(2, "beta"))}
    meta = write_index([chunk(1, "alpha"), chunk(2, "beta"), chunk(3, "gamma")], *paths, Counting(),
                       log=lambda *_: None, reuse=reuse)
    assert Counting.calls == 3 and meta["embeddings_reused"] == 2
    assert previous_vectors(*paths, "another-model") == {}


def test_sites_with_per_visit_urls_get_stable_keys(sync_env):
    """Regression: Punjab Code gives every law a new URL on each visit; that must not look like new laws."""
    source, _ = sync_env
    visit = {"n": 0}

    def punjab_like(_f):
        visit["n"] += 1
        return [Listing("punjab_code", "Punjab", t, f"https://punjabcode.punjab.gov.pk/en/show_article/{t[:4]}{visit['n']}",
                        pdf_url=f"https://punjabcode.punjab.gov.pk/uploads/articles/{i}.pdf",
                        meta=f"Act {i} of 2020 | Promulgation Date: Mon Jan 0{i + 1}, 2020 | Views: {visit['n']}")
                for i, t in enumerate(["PUNJAB ALPHA ACT 2020", "PUNJAB BETA ACT 2020", "PUNJAB BETA ACT 2020"])]

    source_sync.SITES["fake"] = punjab_like
    try:
        first = run(source, "2026-01-01")
        assert first.sources["fake_code"]["listed"] == 3          # the site's own duplicate is kept, suffixed
        assert run(source, "2026-01-08").changes == []
    finally:
        source_sync.SITES["fake"] = fake_adapter


def test_mass_churn_is_an_anomaly_and_blocks_ingest(sync_env):
    source, _ = sync_env
    FAKE_PAGES["current"] = [law(i, f"Sindh Law {i} Act, 2020") for i in range(100)]
    run(source, "2026-01-01")
    FAKE_PAGES["current"] = [law(i + 1000, f"Sindh Law {i} Act, 2020") for i in range(100)]  # every id changed
    report = run(source, "2026-01-08")
    assert "implausible" in report.sources["fake_code"]["anomaly"]
    inventory = source_sync.load_inventory()
    registry = {"fake_code": source}
    plan = plan_ingest(report.changes, inventory, registry, [], source_stats=report.sources)
    assert plan.add == [] and plan.blocked_sources == {"fake_code": report.sources["fake_code"]["anomaly"]}


def test_per_run_cap_and_link_only_upgrade():
    registry = {s.source_id: s for s in load_registry()}
    inventory = {f"k{i}": _inv(law_key=f"k{i}", title=f"PUNJAB NEW LAW NUMBER {i} ACT 2026") for i in range(5)}
    inventory["sja"] = _inv(law_key="sja", source_id="sja_updated_laws", jurisdiction="Sindh",
                            title="The Sindh Civil Courts Ordinance, 1962", year="1962", instrument_type="Ordinance",
                            pdf_url="https://sja.gos.pk/assets/Updated_Laws/Sindh%20Civil%20Court%20Ordinance.pdf")
    manifest = [{"document_id": "SD-001", "title": "Sindh Civil Courts Ordinance, 1962", "jurisdiction": "Sindh",
                 "status": "metadata_only", "court": "", "source_url": "https://www.sindhlaws.gov.pk/SindhIndex.aspx",
                 "file_name": ""}]
    changes = [{"law_key": f"k{i}", "change": "new"} for i in range(5)]
    plan = plan_ingest(changes, inventory, registry, manifest, backfill_keys=["sja"], max_add=3)
    assert len(plan.add) == 3 and sum(r.startswith("deferred") for _, _, r in plan.skipped) == 2
    plan = plan_ingest([], inventory, registry, manifest, backfill_keys=["sja"])
    assert [d for d, _ in plan.upgrade] == ["SD-001"] and plan.add == []
    fields = ["document_id", "title", "document_type", "jurisdiction", "court", "authority", "source_name",
              "source_url", "file_name", "status", "priority", "source_tier", "language"]
    rows = [dict({f: "" for f in fields}, **manifest[0])]
    added, _ = apply_plan(plan, fields, rows, registry)
    assert added == ["SD-001"] and rows[0]["status"] == "source_url_verified"
    assert rows[0]["source_tier"] == "2" and rows[0]["source_url"].startswith("https://sja.gos.pk/")
