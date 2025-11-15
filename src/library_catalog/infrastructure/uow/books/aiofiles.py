from pathlib import Path
from typing import Self

from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.domain.repositories.books import BookRepositoryProtocol
from src.library_catalog.infrastructure.persistence.repositories.books.aiofiles import BooksRepositoryAiofilesImpl


class BooksUowAiofilesImpl(BooksUOW):
    def __init__(self, file_path: Path | str):
        self._file_path = Path(file_path)

    async def __aenter__(self) -> Self:
        self._books = BooksRepositoryAiofilesImpl(self._file_path)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # No cleanup needed for file-based storage
        ...

    async def commit(self) -> None:
        """Stub: aiofiles writes happen immediately, no transaction support."""
        pass

    async def rollback(self) -> None:
        """Stub: aiofiles does not support rollback."""
        pass

    @property
    def books(self) -> BookRepositoryProtocol:
        return self._books
