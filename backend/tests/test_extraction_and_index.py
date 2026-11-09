import json

import numpy as np
import pytest

from app.core.config import settings
from app.legal.acquisition import validate_pdf
from app.legal.chunking import chunk_units
from app.legal.embeddings import EmbeddingDimensionError, HashingEmbedder, check_dim
from app.legal.extraction import Page, clean_page_text, looks_like_contents, resolve_number, split_sections
from app.legal.index import LocalIndex, clear_index_cache, get_local_index, tokenize
from app.legal.manifest import ManifestRow, destination, load_manifest
from helpers import make_pdf


def row(**kw):
    base = dict(document_id="PK-T", title="Test Act, 2020", document_type="Federal Act", jurisdiction="Federal", court="",
                authority="Parliament", citation="", source_name="Pakistan Code",
                source_url="https://pakistancode.gov.pk/pdffiles/test.pdf", file_name="test.pdf",
                status="source_url_verified", priority="High", source_tier=1)
    base.update(kw)
    return ManifestRow(**base)


def test_clean_page_text_removes_headers_and_fixes_hyphenation():
    raw = " Page 4 of 47 \nThe tenant shall pay com�\nmitted rent. The landlord�s duty.\n\n\n\n 12 \n"
    clean = clean_page_text(raw)
    assert "Page 4 of 47" not in clean
    assert "committed" in clean and "landlord's" in clean
    assert "\n\n\n" not in clean


@pytest.mark.parametrize("raw,last,expected", [
    ("28", (7, ""), "8"),        # footnote 2 fused to section 8
    ("11", (0, ""), "1"),        # footnote 1 fused to article 1
    ("28", (27, ""), "28"),
    ("10A", (10, ""), "10A"),
    ("337 B", (337, "A"), "337B"),
    ("5", (40, ""), None),       # backwards → list item / cross reference
    ("900", (12, ""), None),     # implausible jump
])
def test_resolve_number(raw, last, expected):
    assert resolve_number(raw, last) == expected


def test_contents_page_detected():
    toc = "\n".join(f"{i}. Heading number {i}" for i in range(1, 20))
    body = ("1. Short title. (1) This Act may be called the Test Act and it extends to the whole of Pakistan and shall "
            "come into force at once, and every provision applies.\n") * 5
    assert looks_like_contents(toc)
    assert not looks_like_contents(body)


def test_split_sections_tracks_pages_skips_toc_and_handles_schedule():
    pages = [
        Page(1, "\n".join(f"{i}. Heading {i}" for i in range(1, 12)), is_contents=True),
        Page(2, "1. Short title. This Act may be called the Test Act.\n2. Definitions. In this Act tenant means a person."),
        Page(3, "continued definition text on the next page.\n3. Rent. The rent shall be paid monthly in advance."),
        Page(4, "THE FIRST SCHEDULE\n1. — For possession of immovable property twelve years."),
    ]
    units = split_sections(pages)
    labels = [u.label for u in units]
    assert labels[:3] == ["Section 1", "Section 2", "Section 3"]
    s2 = units[1]
    assert (s2.page_start, s2.page_end) == (2, 3) and "next page" in s2.text
    assert "First Schedule, Article 1" in labels
    assert all("Heading 5" not in u.text for u in units)  # TOC excluded


def test_chunks_have_stable_ids_page_ranges_and_hashes():
    pages = [Page(2, "1. Short title. This Act " + "word " * 900), Page(3, "more words " * 50)]
    chunks = chunk_units(row(), split_sections(pages))
    assert len(chunks) >= 3
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    assert all(c.content_hash and c.page_start <= c.page_end for c in chunks)
    assert chunks[0].section_or_article == "Section 1"


def test_far_continuations_do_not_claim_section_label():
    pages = [Page(p, ("1. Short title. The " if p == 1 else "") + "table cell text " * 200) for p in range(1, 9)]
    chunks = chunk_units(row(), split_sections(pages))
    assert chunks[0].section_or_article == "Section 1"
    assert chunks[-1].section_or_article == "" and chunks[-1].section_confidence == "low"


def test_pdf_validation():
    good = validate_pdf(make_pdf(["THE TEST ACT, 2020\n1. Short title. " + "text " * 60]), "Test Act, 2020")
    assert good.is_pdf and good.opens and good.pages == 1 and good.title_match
    bad = validate_pdf(b"<html>not a pdf</html>", "Test Act")
    assert not bad.ok and "not_a_pdf" in bad.problems


def test_manifest_destination_blocks_path_traversal(tmp_path):
    assert destination(tmp_path, row(file_name="../../etc/passwd")).parent == tmp_path / "federal_laws"


def test_manifest_acquirable_rules():
    assert row().acquirable
    assert not row(status="placeholder").acquirable
    assert not row(status="metadata_only").acquirable
    assert not row(source_url="https://evil.example.com/x.pdf").acquirable
    assert not row(source_url="http://pakistancode.gov.pk/x.pdf").acquirable  # https only


def test_real_manifest_quarantines_placeholders():
    rows = load_manifest(settings.manifest_path)
    placeholders = [r for r in rows if r.is_placeholder]
    assert placeholders and not any(r.acquirable for r in placeholders)


def test_embedding_dimension_enforced():
    assert check_dim(np.zeros((2, 384), dtype=np.float32)).shape == (2, 384)
    with pytest.raises(EmbeddingDimensionError):
        check_dim(np.zeros((2, 768), dtype=np.float32))
    assert HashingEmbedder().embed(["a b"]).shape == (1, 384)


def test_index_rejects_misaligned_embeddings():
    meta = json.loads(settings.embeddings_meta_path.read_text(encoding="utf-8"))
    meta["content_hashes"][0] = "tampered"
    settings.embeddings_meta_path.write_text(json.dumps(meta), encoding="utf-8")
    clear_index_cache()
    index, status = get_local_index(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path)
    assert index.size == 4 and index.embeddings is None
    assert status.problem == "embeddings_not_aligned_with_chunks"


def test_bm25_ranks_relevant_chunk_first():
    index, _ = LocalIndex.load(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path)
    scores = index.bm25(tokenize("bail non-bailable offence"))
    assert index.chunks[int(np.argmax(scores))]["section_or_article"] == "Section 497"
