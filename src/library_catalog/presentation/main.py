from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.library_catalog.infrastructure.config.settings import DatabaseSettings, OpenLibrarySettings
from src.library_catalog.infrastructure.di.providers.db import dispose_db_engine
from src.library_catalog.infrastructure.gateways.open_library import OpenLibraryGateway
from src.library_catalog.infrastructure.persistence.session import init_engine, make_session_factory
from src.library_catalog.presentation.api.v1.error_handlers.base import setup_error_handlers as setup_v1_error_handlers
from src.library_catalog.presentation.api.v1.main import router as v1_router


def setup_error_handlers(app: FastAPI) -> None:
    setup_v1_error_handlers(app)


def setup_routers(app: FastAPI) -> None:
    app.include_router(v1_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_settings = DatabaseSettings()

    engine = init_engine(db_settings.url)
    session_factory = make_session_factory(engine)
    app.state.engine = engine
    app.state.session_factory = session_factory

    open_library_settings = OpenLibrarySettings()
    app.state.open_library_gateway = OpenLibraryGateway(open_library_settings)

    yield

    await dispose_db_engine(engine)


def create_app() -> FastAPI:
    return FastAPI(title="Library Catalog API", lifespan=lifespan)


app = create_app()
setup_error_handlers(app)
setup_routers(app)
