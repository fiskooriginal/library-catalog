from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.domain.repositories.books import BookRepositoryProtocol
from src.library_catalog.infrastructure.persistence.repositories.books.sqlalchemy import BooksRepositorySqlAlchemyImpl


class BooksUowSqlAlchemyImpl(BooksUOW):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._books: BookRepositoryProtocol | None = None

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()
        self._books = BooksRepositorySqlAlchemyImpl(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if self._session is None:
            return

        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self.close()

    async def close(self) -> None:
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    @property
    def books(self) -> BookRepositoryProtocol:
        if self._books is None:
            raise RuntimeError("Repository is not initialized. Use 'async with' context manager.")
        return self._books
