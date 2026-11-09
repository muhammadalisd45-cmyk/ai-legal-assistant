"""Section-aware chunking with exact page ranges and stable chunk IDs."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from app.legal.extraction import SectionUnit
from app.legal.manifest import ManifestRow

TARGET_WORDS = 300
MAX_WORDS = 420
OVERLAP_WORDS = 50
# Beyond this many pages from its heading, a unit's text is probably an undetected schedule/table:
# chunks there keep their page numbers but do not claim the section label.
SECTION_CONFIDENT_PAGES = 3


@dataclass
class Chunk:
    chunk_id: str
    chunk_index: int
    section_or_article: str
    section_heading: str
    section_confidence: str
    page_start: int
    page_end: int
    content: str
    content_hash: str
    word_count: int


def _slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:40] or "x"


def unit_label(document_type: str) -> str:
    kind = document_type.lower()
    return "Article" if "constitution" in kind or kind.endswith("order") or "qanun" in kind else "Section"


def _windows(words: list[tuple[str, int]]) -> list[tuple[int, int]]:
    """Return [start, end) word windows, preferring to end at a sentence boundary."""
    if len(words) <= MAX_WORDS:
        return [(0, len(words))]
    out = []
    start = 0
    while start < len(words):
        end = min(len(words), start + TARGET_WORDS)
        if end < len(words):
            # extend up to MAX_WORDS to finish the sentence
            for probe in range(end, min(len(words), start + MAX_WORDS)):
                if re.search(r"[.;:]$", words[probe - 1][0]):
                    end = probe
                    break
        out.append((start, end))
        if end >= len(words):
            break
        start = max(start + 1, end - OVERLAP_WORDS)
    # merge a tiny tail into the previous window
    if len(out) > 1 and out[-1][1] - out[-1][0] < 60:
        prev = out[-2]
        out[-2:] = [(prev[0], out[-1][1])]
    return out


def chunk_units(row: ManifestRow, units: list[SectionUnit]) -> list[Chunk]:
    chunks: list[Chunk] = []
    used_ids: set[str] = set()
    for unit in units:
        words: list[tuple[str, int]] = []
        for page, text in unit.segments or [(unit.page_start, unit.text)]:
            words.extend((word, page) for word in text.split())
        if len(words) < 8:
            continue
        for part, (start, end) in enumerate(_windows(words)):
            piece = words[start:end]
            content = " ".join(word for word, _ in piece)
            page_start, page_end = piece[0][1], piece[-1][1]
            confident = page_start - unit.page_start < SECTION_CONFIDENT_PAGES
            label = unit.label if confident else ""
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            base = f"{row.document_id}-{_slug(unit.label)}-p{page_start:04d}-c{part:02d}"
            chunk_id = base
            n = 1
            while chunk_id in used_ids:
                n += 1
                chunk_id = f"{base}-{n}"
            used_ids.add(chunk_id)
            chunks.append(Chunk(
                chunk_id=chunk_id, chunk_index=len(chunks), section_or_article=label,
                section_heading=unit.heading if confident else "",
                section_confidence="high" if confident and unit.label != "Preamble" else ("low" if not confident else "preamble"),
                page_start=page_start, page_end=page_end, content=content, content_hash=content_hash,
                word_count=len(piece),
            ))
    return chunks
