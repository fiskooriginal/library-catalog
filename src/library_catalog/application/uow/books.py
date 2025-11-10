from abc import abstractmethod

from src.library_catalog.domain.repositories.books import BookRepositoryProtocol
from src.library_catalog.domain.uow import UnitOfWorkProtocol


class BooksUOW(UnitOfWorkProtocol):
    @property
    @abstractmethod
    def books(self) -> BookRepositoryProtocol: ...
