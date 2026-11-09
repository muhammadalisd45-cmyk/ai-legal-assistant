"""Build and load the local legal index (chunks JSONL + aligned 384-d embeddings + BM25 statistics)."""
from __future__ import annotations

import json
import logging
import math
import re
import threading
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from app.legal.acquisition import load_provenance, sha256
from app.legal.chunking import chunk_units, unit_label
from app.legal.embeddings import EXPECTED_DIM, Embedder, EmbeddingDimensionError, check_dim
from app.legal.extraction import extract_pages, split_sections
from app.legal.manifest import ManifestRow, destination, load_manifest

logger = logging.getLogger("pjn.index")

STOPWORDS = frozenset("""a an and are as at be been being by for from has have he her his if in into is it its of on or
shall she such that the their them then there these they this those to under upon was were which who whom will with
within without any all other may not no nor so than also be said section article act""".split())
_TOKEN = re.compile(r"[a-z0-9]+")


def stem(token: str) -> str:
    for suffix, min_len in (("ments", 7), ("ment", 6), ("ings", 6), ("ing", 5), ("ily", 6), ("ies", 5), ("ed", 4),
                            ("es", 4), ("s", 3)):
        if token.endswith(suffix) and len(token) >= min_len + 1:
            base = token[: -len(suffix)]
            return base + ("y" if suffix in ("ies", "ily") else "")
    return token


def tokenize(text: str) -> list[str]:
    return [stem(t) for t in _TOKEN.findall(text.lower()) if t not in STOPWORDS and (len(t) > 1 or t.isdigit())]


# --------------------------------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------------------------------

def build_chunk_rows(rows: list[ManifestRow], corpus_dir: Path, provenance_path: Path, log=print) -> list[dict]:
    provenance = load_provenance(provenance_path).get("documents", {})
    output: list[dict] = []
    for row in rows:
        if row.is_placeholder or row.status == "metadata_only":
            continue
        pdf = destination(corpus_dir, row)
        if not pdf.exists():
            continue
        prov = provenance.get(row.document_id)
        file_hash = sha256(pdf.read_bytes())
        if not prov or prov.get("sha256") != file_hash:
            log(f"SKIP {row.document_id}: no matching provenance record (run scripts/acquire_corpus.py)")
            continue
        pages = extract_pages(pdf)
        units = split_sections(pages, unit_label(row.document_type))
        chunks = chunk_units(row, units)
        for chunk in chunks:
            output.append({
                "chunk_id": chunk.chunk_id, "chunk_index": chunk.chunk_index,
                "document_id": row.document_id, "title": row.title, "document_type": row.document_type,
                "jurisdiction": row.jurisdiction, "court": row.court, "bench": row.bench, "authority": row.authority,
                "citation": row.citation, "section_or_article": chunk.section_or_article,
                "section_heading": chunk.section_heading, "section_confidence": chunk.section_confidence,
                "page_start": chunk.page_start, "page_end": chunk.page_end,
                "source_name": row.source_name, "source_url": row.source_url, "source_tier": row.source_tier,
                "language": row.language or "English",
                "content": chunk.content, "content_hash": chunk.content_hash, "word_count": chunk.word_count,
                "file_sha256": file_hash, "fetched_at": prov.get("fetched_at", ""),
                "embedding": None,  # embeddings live in the aligned .npy file
            })
        log(f"OK   {row.document_id}: {len(pages)} pages, {len(units)} provisions, {len(chunks)} chunks")
    return output


def embedding_text(row: dict) -> str:
    head = " ".join(part for part in (row["title"], row.get("section_or_article", ""), row.get("section_heading", "")) if part)
    return f"{head}\n{row['content']}"


def write_index(chunk_rows: list[dict], chunks_path: Path, embeddings_path: Path, meta_path: Path,
                embedder: Embedder | None, log=print) -> dict:
    chunks_path.parent.mkdir(parents=True, exist_ok=True)
    with chunks_path.open("w", encoding="utf-8") as handle:
        for row in chunk_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    meta = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "chunk_count": len(chunk_rows),
        "documents": sorted({row["document_id"] for row in chunk_rows}),
        "embedding_model": None, "embedding_dim": None,
        "chunk_ids": [row["chunk_id"] for row in chunk_rows],
        "content_hashes": [row["content_hash"] for row in chunk_rows],
    }
    if embedder is not None and chunk_rows:
        vectors = []
        batch = 128
        for start in range(0, len(chunk_rows), batch):
            vectors.append(embedder.embed([embedding_text(r) for r in chunk_rows[start:start + batch]]))
            log(f"embedded {min(start + batch, len(chunk_rows))}/{len(chunk_rows)}")
        matrix = check_dim(np.vstack(vectors), EXPECTED_DIM).astype(np.float32)
        np.save(embeddings_path, matrix)
        meta["embedding_model"] = embedder.name
        meta["embedding_dim"] = int(matrix.shape[1])
    elif embeddings_path.exists():
        embeddings_path.unlink()  # never leave stale vectors next to a rebuilt chunk file
    meta_path.write_text(json.dumps(meta, ensure_ascii=False) + "\n", encoding="utf-8")
    return meta


# --------------------------------------------------------------------------------------------------
# Load
# --------------------------------------------------------------------------------------------------

@dataclass
class IndexStatus:
    chunks: int = 0
    documents: int = 0
    embeddings: bool = False
    embedding_model: str | None = None
    embedding_dim: int | None = None
    problem: str = ""


class LocalIndex:
    def __init__(self, chunks: list[dict], embeddings: np.ndarray | None, embedding_model: str | None):
        self.chunks = chunks
        self.embeddings = embeddings
        self.embedding_model = embedding_model
        self.doc_freq: Counter[str] = Counter()
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        self.lengths = np.zeros(len(chunks), dtype=np.float32)
        for i, chunk in enumerate(chunks):
            # Field weighting: title/section/heading tokens count twice.
            head = " ".join(filter(None, [chunk.get("title", ""), chunk.get("section_or_article", ""),
                                          chunk.get("section_heading", "")]))
            tokens = tokenize(chunk.get("content", "")) + tokenize(head) * 2
            counts = Counter(tokens)
            self.lengths[i] = len(tokens)
            for token, tf in counts.items():
                self.postings[token].append((i, tf))
                self.doc_freq[token] += 1
        self.avg_len = float(self.lengths.mean()) if len(chunks) else 0.0
        self.by_section: dict[tuple[str, str], list[int]] = defaultdict(list)
        self.by_label: dict[tuple[str, str], list[int]] = defaultdict(list)
        for i, chunk in enumerate(chunks):
            label = (chunk.get("section_or_article") or "").lower()
            if label:
                self.by_label[(chunk.get("document_id", ""), label)].append(i)
            match = re.search(r"(section|article|rule)\s+([0-9]+[a-z]*)$", label)
            if match:
                self.by_section[(match.group(1), match.group(2))].append(i)

    @property
    def size(self) -> int:
        return len(self.chunks)

    def bm25(self, terms: list[str], k1: float = 1.4, b: float = 0.72) -> np.ndarray:
        scores = np.zeros(len(self.chunks), dtype=np.float32)
        n = len(self.chunks)
        if not n:
            return scores
        for term in dict.fromkeys(terms):
            postings = self.postings.get(term)
            if not postings:
                continue
            idf = math.log(1 + (n - len(postings) + 0.5) / (len(postings) + 0.5))
            for i, tf in postings:
                denom = tf + k1 * (1 - b + b * self.lengths[i] / max(self.avg_len, 1.0))
                scores[i] += idf * (tf * (k1 + 1)) / denom
        return scores

    @classmethod
    def load(cls, chunks_path: Path, embeddings_path: Path, meta_path: Path) -> tuple["LocalIndex", IndexStatus]:
        status = IndexStatus()
        chunks: list[dict] = []
        if chunks_path.exists():
            with chunks_path.open(encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        row = json.loads(line)
                        if row.get("content"):
                            chunks.append(row)
        embeddings = None
        model = None
        if chunks and embeddings_path.exists() and meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                matrix = check_dim(np.load(embeddings_path), EXPECTED_DIM)
                aligned = (matrix.shape[0] == len(chunks)
                           and meta.get("chunk_ids") == [c["chunk_id"] for c in chunks]
                           and meta.get("content_hashes") == [c.get("content_hash") for c in chunks])
                if aligned:
                    embeddings, model = matrix.astype(np.float32), meta.get("embedding_model")
                else:
                    status.problem = "embeddings_not_aligned_with_chunks"
            except (EmbeddingDimensionError, ValueError, OSError) as exc:
                status.problem = f"embeddings_invalid:{type(exc).__name__}"
        status.chunks = len(chunks)
        status.documents = len({c["document_id"] for c in chunks})
        status.embeddings = embeddings is not None
        status.embedding_model = model
        status.embedding_dim = int(embeddings.shape[1]) if embeddings is not None else None
        if status.problem:
            logger.warning("index_embeddings_disabled", extra={"problem": status.problem})
        return cls(chunks, embeddings, model), status


_cache: dict[str, tuple[float, LocalIndex, IndexStatus]] = {}
_lock = threading.Lock()


def get_local_index(chunks_path: Path, embeddings_path: Path, meta_path: Path) -> tuple[LocalIndex, IndexStatus]:
    """Cached load; reloads automatically when the chunk/embedding files change."""
    def mtime(path: Path) -> float:
        return path.stat().st_mtime if path.exists() else 0.0

    stamp = mtime(chunks_path) + mtime(embeddings_path) + mtime(meta_path)
    key = str(chunks_path)
    with _lock:
        cached = _cache.get(key)
        if cached and cached[0] == stamp:
            return cached[1], cached[2]
        index, status = LocalIndex.load(chunks_path, embeddings_path, meta_path)
        _cache[key] = (stamp, index, status)
        return index, status


def clear_index_cache() -> None:
    with _lock:
        _cache.clear()
