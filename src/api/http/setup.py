from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src import __version__
from src.api.http.exceptions import (
    application_exception_handler,
    general_exception_handler,
)
from src.api.http.middlewares import config_middleware
from src.api.http.routes.health import router as health_router
from src.api.http.routes.users import router as users_router
from src.core.config import settings
from src.core.logging import get_logger
from src.exceptions.base import ApplicationError

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(f"Starting {settings.app_name} v{__version__}")
    logger.info(f"Debug mode: {settings.app_debug}")

    yield

    logger.info(f"Shutting down {settings.app_name}")


def setup_routes(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(users_router, prefix="/api/v1", tags=["users"])


def config_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="A production-ready FastAPI template with best practices",
        version=__version__,
        debug=settings.app_debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        swagger_ui_parameters={
            "syntaxHighlight": {"theme": "obsidian"},
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
        },
        contact={
            "name": "API Support",
            "email": "support@example.com",
        },
        license_info={
            "name": "MIT",
        },
    )

    config_middleware(app)

    app.add_exception_handler(Exception, general_exception_handler)

    app.add_exception_handler(ApplicationError, application_exception_handler) # type: ignore

    setup_routes(app)

    return app


app = config_app()
