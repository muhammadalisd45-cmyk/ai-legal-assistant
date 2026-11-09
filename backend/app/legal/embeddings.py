"""Embedding providers. The pgvector column is `vector(384)`; every provider must produce 384-d vectors."""
from __future__ import annotations

import hashlib
import logging
import os
import threading
from typing import Protocol, Sequence

import numpy as np

from app.core.config import BACKEND_DIR, settings

logger = logging.getLogger("pjn.embeddings")

EXPECTED_DIM = 384


class EmbeddingDimensionError(ValueError):
    pass


class Embedder(Protocol):
    name: str
    dim: int

    def embed(self, texts: Sequence[str]) -> np.ndarray: ...


def check_dim(matrix: np.ndarray, expected: int = EXPECTED_DIM) -> np.ndarray:
    if matrix.ndim != 2 or matrix.shape[1] != expected:
        raise EmbeddingDimensionError(f"expected (n, {expected}) embeddings, got {matrix.shape}")
    if not np.isfinite(matrix).all():
        raise EmbeddingDimensionError("embeddings contain non-finite values")
    return matrix


def l2_normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (matrix / norms).astype(np.float32)


class FastEmbedEmbedder:
    """Local ONNX sentence-transformer (multilingual MiniLM, 384-d). Model files are cached under backend/.cache."""

    # Cosine similarity at/above which a hit counts as a strong match (calibrated, see docs/RETRIEVAL_EVAL.md).
    strong_threshold = 0.48

    def __init__(self, model_name: str | None = None):
        self.name = model_name or settings.embedding_model
        self.dim = EXPECTED_DIM
        self._model = None
        self._lock = threading.Lock()

    def _load(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
                    from fastembed import TextEmbedding

                    cache = BACKEND_DIR / ".cache" / "fastembed"
                    cache.mkdir(parents=True, exist_ok=True)
                    self._model = TextEmbedding(self.name, cache_dir=str(cache))
        return self._model

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        model = self._load()
        vectors = np.array(list(model.embed(list(texts), batch_size=32)), dtype=np.float32)
        return l2_normalize(check_dim(vectors, self.dim))


class HashingEmbedder:
    """Deterministic test double. NOT semantic — used only by unit tests."""

    name = "test-hashing-384"
    dim = EXPECTED_DIM
    strong_threshold = 0.2

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in text.lower().split():
                digest = hashlib.md5(token.encode("utf-8")).digest()
                out[row, int.from_bytes(digest[:4], "little") % self.dim] += 1.0
        return l2_normalize(out)


_default: Embedder | None = None
_default_failed = False


def get_embedder() -> Embedder | None:
    """Shared embedder, or None when semantic search is disabled/unavailable (lexical still works)."""
    global _default, _default_failed
    if not settings.semantic_search_enabled or _default_failed:
        return None
    if _default is None:
        try:
            _default = FastEmbedEmbedder()
        except Exception:  # noqa: BLE001
            _default_failed = True
            logger.warning("embedder_unavailable")
            return None
    return _default


def set_embedder(embedder: Embedder | None) -> None:
    """Test hook."""
    global _default, _default_failed
    _default = embedder
    _default_failed = embedder is None
