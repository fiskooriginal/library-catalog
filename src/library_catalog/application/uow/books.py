from abc import abstractmethod

from src.library_catalog.application.uow.protocol import UnitOfWorkProtocol
from src.library_catalog.domain.repositories.books import BookRepositoryProtocol


class BooksUOW(UnitOfWorkProtocol):
    @property
    @abstractmethod
    def books(self) -> BookRepositoryProtocol: ...
