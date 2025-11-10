from src.library_catalog.domain.exceptions import DomainException


class BookAlreadyExistsException(DomainException): ...


class BookNotFoundException(DomainException): ...
