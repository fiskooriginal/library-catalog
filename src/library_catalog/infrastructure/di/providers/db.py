from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.library_catalog.infrastructure.persistence.session import (
    dispose_engine,
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
