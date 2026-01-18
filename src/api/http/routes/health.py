from fastapi import APIRouter, status
from pydantic import BaseModel

from src.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    version: str
    app_name: str


@router.get(
    path="",
    name="health:check",
    description="Health check endpoint",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    response_model=HealthResponse,
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        app_name=settings.app_name,
    )

