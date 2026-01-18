from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.core.config import settings
from src.core.logging import get_logger
from src.exceptions.base import ApplicationError

logger = get_logger(__name__)


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle Pydantic validation errors.
    """
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> ORJSONResponse:
    """
    Handle HTTP exceptions.
    """
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        },
    )


async def application_exception_handler(
    request: Request,
    exc: ApplicationError,
) -> ORJSONResponse:
    """
    Handle application exceptions.
    """
    logger.warning(f"Application exception: {exc.status_code} - {exc.message}")
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
        },
    )


async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> ORJSONResponse:
    """
    Handle general exceptions.
    """

    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.app_debug else "An error occurred",
        },
    )
