"""Retrieval-quality regression test on the REAL ingested corpus (skipped until the index is built)."""
import json

import pytest

from app.core.config import BACKEND_DIR, REPO_DIR, settings
from app.legal import embeddings as embeddings_module
from app.legal.index import LocalIndex

REAL = REPO_DIR / "frontend" / "data" / "rag_index"
pytestmark = pytest.mark.skipif(not (REAL / "legal_chunks.jsonl").exists() or (REAL / "legal_chunks.jsonl").stat().st_size == 0,
                                reason="real corpus index not built (run scripts/acquire_corpus.py && scripts/build_index.py)")

THRESHOLDS = {"english": (0.9, 0.8), "roman_urdu": (0.9, 0.75), "urdu": (0.85, 0.7)}  # (document hit@5, provision hit@5)


@pytest.fixture(scope="module")
def real_index():
    index, status = LocalIndex.load(REAL / "legal_chunks.jsonl", REAL / "legal_chunk_embeddings.npy",
                                    REAL / "legal_chunk_embeddings.meta.json")
    assert status.problem == "", status.problem
    return index


@pytest.fixture(scope="module")
def real_embedder(real_index):
    if real_index.embeddings is None:
        return None
    try:
        return embeddings_module.FastEmbedEmbedder()
    except Exception:  # noqa: BLE001
        return None


def test_real_index_integrity(real_index):
    assert real_index.size > 1000
    assert all(c["source_url"].startswith("https://pakistancode.gov.pk/") for c in real_index.chunks)
    assert not any(c["document_id"].startswith("SHC-") for c in real_index.chunks), "placeholders must never be indexed"
    assert len({c["chunk_id"] for c in real_index.chunks}) == real_index.size
    assert all(c["page_start"] >= 1 and c["page_end"] >= c["page_start"] for c in real_index.chunks)
    if real_index.embeddings is not None:
        assert real_index.embeddings.shape == (real_index.size, 384)


@pytest.mark.parametrize("query,expect_strong", [
    ("What is the income tax rate on crypto profits?", False),
    ("car accident insurance claim", False),
    ("how to apply for a passport", False),
    ("how to get divorce khula", False),          # family law not in the verified corpus yet
    ("What are my rights if I am arrested?", True),
    ("chacha ne zameen par qabza kar liya", True),
    ("ضمانت کب ملتی ہے", True),
    ("FIR kaise darj karwayen", True),
])
def test_relevance_gate_on_real_corpus(real_index, real_embedder, query, expect_strong):
    if real_embedder is None:
        pytest.skip("embedding model unavailable")
    from app.legal.retrieval import analyze_query, search_local

    results, _ = search_local(real_index, analyze_query(query), 5, real_embedder)
    assert any(r.strong for r in results) is expect_strong, [(r.chunk["document_id"], r.semantic_score) for r in results]


@pytest.mark.parametrize("query,expected", [
    # A real citizen's wording (misspelling, filler) once returned CPC mortgage rules and the AML Act.
    ("there is theif case where a person robbed my laptop and now it is gone",
     {("PK-002", "Section 390"), ("PK-002", "Section 392"), ("PK-002", "Section 378")}),
    ("someone stole my phone", {("PK-002", "Section 378"), ("PK-002", "Section 379")}),
    ("mera mobile chori ho gaya", {("PK-002", "Section 378"), ("PK-002", "Section 379")}),
])
def test_colloquial_theft_finds_penal_provisions(real_index, real_embedder, query, expected):
    from app.legal.retrieval import analyze_query, search_local

    results, _ = search_local(real_index, analyze_query(query), 5, real_embedder)
    labels = {(r.chunk["document_id"], r.chunk["section_or_article"]) for r in results if r.strong}
    assert labels & expected, [(r.chunk["document_id"], r.chunk["section_or_article"], r.strong) for r in results]
    assert not any(r.chunk["document_id"] in {"PK-004", "PK-015"} for r in results[:3])


def test_retrieval_quality_per_language(real_index, real_embedder):
    import sys

    sys.path.insert(0, str(BACKEND_DIR / "scripts"))
    from evaluate_retrieval import EVAL_FILE, evaluate

    spec = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    report = evaluate(real_index, real_embedder, "hybrid" if real_embedder else "lexical", spec["k"], spec["queries"])
    for language, (doc_min, prov_min) in THRESHOLDS.items():
        r = report[language]
        assert r["document_hit_at_k"] >= doc_min, (language, r)
        if real_embedder is not None:
            assert r["provision_hit_at_k"] >= prov_min, (language, r)
