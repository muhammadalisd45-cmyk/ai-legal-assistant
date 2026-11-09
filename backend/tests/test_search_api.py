import pytest


def search(client, query, **kw):
    response = client.post("/v1/search", json={"query": query, **kw})
    assert response.status_code == 200, response.text
    return response.json()


def test_search_returns_traceable_chunk_evidence(client):
    body = search(client, "when can bail be granted for non-bailable offence")
    assert body["mode"] == "local-hybrid"
    top = body["results"][0]
    assert top["section_or_article"] == "Section 497"
    assert top["evidence_level"] == "chunk" and top["is_legal_provision"] is True
    assert top["page_start"] == 167 and top["page_reference"] == "pp. 167–168"
    assert top["provenance"]["page_url"].endswith("#page=167")
    assert top["provenance"]["file_sha256"] == "abc"
    assert top["source_url"].startswith("https://pakistancode.gov.pk/")
    assert body["evidence_summary"]["chunk"] >= 1
    # Legacy fields the Next.js UI relies on
    for field in ("document_id", "title", "jurisdiction", "authority", "court", "bench", "snippet", "status", "score"):
        assert field in top


def test_roman_urdu_query_is_bridged(client):
    body = search(client, "chacha ne zameen par kabza kar liya, kya karun")
    assert body["detected_language"] == "roman_urdu"
    assert body["results"][0]["document_id"] == "PK-007"
    assert "possession" in body["retrieval"]["bridged_terms"]


def test_urdu_query_is_bridged(client):
    body = search(client, "پولیس نے گرفتار کیا، ضمانت کیسے ہوگی")
    assert body["detected_language"] == "urdu"
    assert body["results"][0]["section_or_article"] == "Section 497"


def test_exact_section_reference_boost(client):
    body = search(client, "dafa 154 kya hai")
    assert body["results"][0]["section_or_article"] == "Section 154"
    assert "section_reference" in body["results"][0]["match_reasons"]


def test_filters(client):
    body = search(client, "fair trial due process", filters={"document_type": "Constitution"})
    assert body["results"] and all(r["document_type"] == "Constitution" for r in body["results"])


def test_metadata_only_fallback_is_labelled_and_never_shows_placeholders(client, empty_index):
    body = search(client, "Sindh High Court judgment rented premises")
    assert body["mode"] == "metadata-only"
    assert body["fallback_reason"] == "index_empty"
    assert body["warning"]
    assert body["results"], "expected metadata pointers"
    assert all(r["evidence_level"] == "metadata" and r["is_legal_provision"] is False for r in body["results"])
    assert all(not r["document_id"].startswith("SHC-") for r in body["results"])
    assert all(r["page_start"] is None for r in body["results"])


def test_unmatched_query_returns_transparent_empty_result(client):
    body = search(client, "zzqx qqzz")
    assert body["mode"] == "metadata-only" and body["results"] == [] and body["warning"]


@pytest.mark.parametrize("payload", [
    {"query": "ab"},
    {"query": "   "},
    {"query": "x" * 1201},
    {"query": "valid query", "limit": 50},
    {"query": "valid query", "drop_tables": True},
])
def test_query_validation(client, payload):
    assert client.post("/v1/search", json=payload).status_code == 422


def test_api_v1_alias(client):
    assert client.post("/api/v1/search", json={"query": "bail offence"}).status_code == 200
