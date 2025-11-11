from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.infrastructure.config.settings import FileStorageSettings, JsonBinSettings
from src.library_catalog.infrastructure.di.providers.db import get_session_factory
from src.library_catalog.infrastructure.uow.books.aiofiles import BooksUowAiofilesImpl
from src.library_catalog.infrastructure.uow.books.jsonbinio import BooksUowJsonbinioImpl
from src.library_catalog.infrastructure.uow.books.sqlalchemy import BooksUowSqlAlchemyImpl


def get_books_uow_sqlalchemy() -> BooksUOW:
    factory = get_session_factory()
    return BooksUowSqlAlchemyImpl(factory)


def get_books_uow_aiofiles() -> BooksUOW:
    storage = FileStorageSettings().file_path
    return BooksUowAiofilesImpl(storage)


def get_books_uow_jsonbinio() -> BooksUOW:
    settings = JsonBinSettings()
    return BooksUowJsonbinioImpl(settings.api_key, settings.bin_id)


# Builders for tests/explicit composition
def build_books_uow_sqlalchemy(session_factory: async_sessionmaker[AsyncSession]) -> BooksUOW:
    return BooksUowSqlAlchemyImpl(session_factory)


def build_books_uow_aiofiles(file_path: str | Path) -> BooksUOW:
    return BooksUowAiofilesImpl(file_path)


def build_books_uow_jsonbinio(api_key: str, bin_id: str | None = None) -> BooksUowJsonbinioImpl:
    return BooksUowJsonbinioImpl(api_key, bin_id)
