from fastapi import APIRouter
from ..dtos import HealthResponse

HealthRouter = APIRouter(prefix="/health", tags=["Health"])


@HealthRouter.get("/", summary="Health check")
async def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
