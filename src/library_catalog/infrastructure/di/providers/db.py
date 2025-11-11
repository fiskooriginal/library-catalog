from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.library_catalog.infrastructure.config.settings import DatabaseSettings
from src.library_catalog.infrastructure.persistence.session import (
    dispose_engine,
    init_engine,
    make_session_factory,
)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        db_settings = DatabaseSettings()
        _engine = init_engine(db_settings.url)
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        bound_engine = get_engine()
        _session_factory = make_session_factory(bound_engine)
    return _session_factory


async def dispose_db_engine() -> None:
    global _engine
    if _engine is not None:
        await dispose_engine(_engine)
        _engine = None


# Builders for tests/explicit composition
def build_engine(settings: DatabaseSettings) -> AsyncEngine:
    return init_engine(settings.url)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return make_session_factory(engine)
