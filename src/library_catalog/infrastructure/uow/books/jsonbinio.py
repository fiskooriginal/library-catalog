from typing import Self

from src.library_catalog.application.uow.books import BooksUOW
from src.library_catalog.domain.repositories.books import BookRepositoryProtocol
from src.library_catalog.infrastructure.persistence.repositories.books.jsonbinio import BooksRepositoryJsonbinioImpl


class BooksUowJsonbinioImpl(BooksUOW):
    """
    JSONBinIO does not support Transactions.
    """

    def __init__(self, api_key: str, bin_id: str | None = None):
        self._api_key = api_key
        self._bin_id = bin_id

    async def __aenter__(self) -> Self:
        self._books = BooksRepositoryJsonbinioImpl(self._api_key, self._bin_id)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # No cleanup needed for API-based storage
        ...

    async def commit(self) -> None:
        """Stub: JSONBin.io writes happen immediately, no transaction support."""
        pass

    async def rollback(self) -> None:
        """Stub: JSONBin.io does not support rollback."""
        pass

    @property
    def books(self) -> BookRepositoryProtocol:
        return self._books
