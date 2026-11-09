"""Legal search (Phase 7) and grounded answers (Phase 8)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from app.core.rate_limit import rate_limit
from app.legal.answer_service import AnswerService
from app.legal.search_service import search
from app.schemas.answer import AnswerRequest, AnswerResponse
from app.schemas.search import SearchRequest, SearchResponse

search_router = APIRouter(tags=["legal-search"])
answer_router = APIRouter(tags=["legal-answers"])
answer_service = AnswerService()


async def _search(payload: SearchRequest, request: Request) -> SearchResponse:
    return await search(payload, request_id=getattr(request.state, "request_id", ""))


search_router.add_api_route("/v1/search", _search, methods=["POST"], response_model=SearchResponse,
                            dependencies=[Depends(rate_limit("search"))],
                            summary="Search official legal text (evidence-aware)")
search_router.add_api_route("/api/v1/search", _search, methods=["POST"], response_model=SearchResponse,
                            dependencies=[Depends(rate_limit("search"))], include_in_schema=False)


@answer_router.post("/answer", response_model=AnswerResponse, dependencies=[Depends(rate_limit("answer", ai=True))],
                    summary="Citation-backed answer grounded in retrieved official text")
async def answer(payload: AnswerRequest, request: Request) -> AnswerResponse:
    return await answer_service.answer(payload, request_id=getattr(request.state, "request_id", ""))
