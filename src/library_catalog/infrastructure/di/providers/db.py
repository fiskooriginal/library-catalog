from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.library_catalog.infrastructure.config.settings import DatabaseSettings
from src.library_catalog.infrastructure.persistence.session import (
    dispose_engine,
    init_engine,
    make_session_factory,
)


def get_engine(request: Request) -> AsyncEngine:
    if not hasattr(request.app.state, "engine"):
        raise RuntimeError("Engine not initialized. Check lifespan configuration.")
    return request.app.state.engine


def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    if not hasattr(request.app.state, "session_factory"):
        raise RuntimeError("Session factory not initialized. Check lifespan configuration.")
    return request.app.state.session_factory


async def dispose_db_engine(engine: AsyncEngine) -> None:
    await dispose_engine(engine)


# Builders for tests/explicit composition
def build_engine(settings: DatabaseSettings) -> AsyncEngine:
    return init_engine(settings.url)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return make_session_factory(engine)
