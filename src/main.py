import uvicorn

from src.api.http.setup import app
from src.core.config import settings


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level=settings.app_log_level,
    )
