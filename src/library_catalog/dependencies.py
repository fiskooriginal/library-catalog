from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.databases import get_session
from src.library_catalog.open_library import OpenLibraryClient
from src.library_catalog.repository import BookRepository


def get_open_library_client() -> OpenLibraryClient:
    return OpenLibraryClient()


def get_book_repository(
    session: AsyncSession = Depends(get_session),
    open_library_client: OpenLibraryClient = Depends(get_open_library_client),
) -> BookRepository:
    return BookRepository(session, open_library_client)
