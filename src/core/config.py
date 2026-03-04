from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(
        default="FastAPI APP",
        description="Application name",
    )
    app_version: str = Field(
        default="1.0.0",
        description="Application version",
    )
    app_debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )

    db_url: str = Field(
        default="sqlite+aiosqlite:///./sqlite/app.db",
        description="Database connection URL",
    )
    db_echo: bool = Field(
        default=True,
        description="Enable SQLAlchemy query logging",
    )

    app_log_level: str = Field(
        default="INFO",
        description="Logging level",
    )
    log_file: str = Field(
        default="./logs/app.log",
        description="Log file path",
    )

    cors_origins: str = Field(
        default="*",
        description="CORS allowed origins",
    )

    host: str = Field(
        default="0.0.0.0",
        description="Server host",
    )
    port: int = Field(
        default=8000,
        description="Server port",
    )

    open_router_api_key: str = Field(
        ...,
    )
    phoenix_url: str = Field(
        ...,
    )
    phoenix_api_key: str | None = Field(
        default=None,
    )

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @field_validator("app_log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, v: str | None) -> str:
        """Приводит уровень логирования к верхнему регистру."""
        if v is None:
            return "INFO"
        return v.upper() if isinstance(v, str) else str(v).upper()


settings = Settings()  # type: ignore[call-arg]
