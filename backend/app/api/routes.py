from fastapi import APIRouter, HTTPException
from app.schemas.triage import TriageRequest, TriageResult
from app.services.triage_service import TriageService

router = APIRouter(tags=["legal-triage"])
service = TriageService()

@router.post("/triage", response_model=TriageResult)
async def triage(request: TriageRequest) -> TriageResult:
    try:
        return await service.analyze(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The legal triage service is temporarily unavailable.",
        ) from exc
