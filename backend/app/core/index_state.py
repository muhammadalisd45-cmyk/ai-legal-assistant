from __future__ import annotations

from app.core.config import settings
from app.legal.index import IndexStatus, LocalIndex, get_local_index


def local_index() -> tuple[LocalIndex, IndexStatus]:
    return get_local_index(settings.chunks_path, settings.embeddings_path, settings.embeddings_meta_path)
