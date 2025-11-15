from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.library_catalog.infrastructure.cache.connection import close_redis_cache, create_redis_cache
from src.library_catalog.infrastructure.config.settings import (
    DatabaseSettings,
    OpenLibrarySettings,
    RedisSettings,
)
from src.library_catalog.infrastructure.di.providers.db import dispose_db_engine
from src.library_catalog.infrastructure.gateways.open_library import OpenLibraryGateway
from src.library_catalog.infrastructure.logging import setup_logging
from src.library_catalog.infrastructure.middleware import LoggingMiddleware, TimingMiddleware
from src.library_catalog.infrastructure.persistence.session import init_engine, make_session_factory
from src.library_catalog.presentation.api.v1.error_handlers.base import setup_error_handlers as setup_v1_error_handlers
from src.library_catalog.presentation.api.v1.main import router as v1_router


def setup_error_handlers(app: FastAPI) -> None:
    setup_v1_error_handlers(app)


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(TimingMiddleware)
    app.add_middleware(LoggingMiddleware)


def setup_routers(app: FastAPI) -> None:
    app.include_router(v1_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    # Initialize database
    db_settings = DatabaseSettings()
    engine = init_engine(db_settings.url)
    session_factory = make_session_factory(engine)
    app.state.engine = engine
    app.state.session_factory = session_factory

    # Initialize Redis cache
    redis_settings = RedisSettings()
    cache = create_redis_cache(redis_settings)
    app.state.cache = cache

    # Initialize OpenLibrary gateway
    open_library_settings = OpenLibrarySettings()
    app.state.open_library_gateway = OpenLibraryGateway(open_library_settings, cache)

    yield

    # Cleanup
    await dispose_db_engine(engine)
    await close_redis_cache(cache)


def create_app() -> FastAPI:
    return FastAPI(title="Library Catalog API", lifespan=lifespan)


app = create_app()
setup_middleware(app)
setup_error_handlers(app)
setup_routers(app)
