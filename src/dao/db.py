import time
from typing import Any, AsyncGenerator

from sqlalchemy import Connection, ExecutionContext, event
from sqlalchemy.engine.interfaces import DBAPICursor
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


def before_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: Any,
    context: ExecutionContext,
    executemany: bool,
) -> None:
    """Execution of previous events"""

    context._query_start_time = time.time()     # type: ignore[attr-defined]


def after_cursor_execute(
    conn: Connection,
    cursor: DBAPICursor,
    statement: str,
    parameters: Any,
    context: ExecutionContext,
    executemany: bool,
) -> None:
    """Events after execution"""
    query_start = getattr(context, "_query_start_time")
    total = time.time() - query_start
    execution_time = f"{total * 1000:.02f}ms"
    logger.debug(
        f"Execute SQL: {statement}\nParameters: {parameters}\nExecution time: {execution_time}"
    )


class Database:
    def __init__(self, dsn: str, echo: bool):
        self._engine = create_async_engine(
            url=settings.db_url,
            echo=settings.db_echo,
            pool_size=5,
            max_overflow=10,
        )
        self.__register_events(self._engine)
        self._sessin_maker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )

    async def get_session(
        self,
    ) -> AsyncGenerator[AsyncSession]:
        """Get a new session."""
        async with self._sessin_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    def __register_events(self, engine: AsyncEngine) -> None:
        event.listen(engine.sync_engine, "before_cursor_execute", before_cursor_execute)
        event.listen(engine.sync_engine, "after_cursor_execute", after_cursor_execute)


database = Database(dsn=settings.db_url, echo=settings.db_echo)
