from __future__ import annotations

from app.core.config import settings
from app.repositories.base import CaseRepository

_repo: CaseRepository | None = None


def get_repository() -> CaseRepository:
    global _repo
    if _repo is None:
        if settings.case_store == "supabase":
            from app.repositories.supabase_repo import SupabaseCaseRepository

            _repo = SupabaseCaseRepository()
        else:
            from app.repositories.sqlite_repo import SQLiteCaseRepository

            _repo = SQLiteCaseRepository(settings.sqlite_path)
    return _repo


def set_repository(repo: CaseRepository | None) -> None:
    """Test hook."""
    global _repo
    _repo = repo
