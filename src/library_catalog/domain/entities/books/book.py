from dataclasses import dataclass

from src.library_catalog.domain.config import TEXT_MAX_LENGTH
from src.library_catalog.domain.entities.base import BaseEntity
from src.library_catalog.domain.exceptions import DomainException
from src.library_catalog.domain.vo.books import BookAvailability, BookMetadata


@dataclass(frozen=True, slots=True, kw_only=True)
class BookEntity(BaseEntity):
    name: str
    author: str
    year: int
    pages: int
    genre: str
    availability: BookAvailability
    metadata: BookMetadata

    def __post_init__(self) -> None:
        if self.pages is not None and self.pages <= 0:
            raise DomainException("Pages must be greater than 0")
        if self.year is not None and self.year <= 0:
            raise DomainException("Year must be greater than 0")
        if self.author and len(self.author) > TEXT_MAX_LENGTH:
            raise DomainException(f"Author must be less than {TEXT_MAX_LENGTH} characters")
        if self.name and len(self.name) > TEXT_MAX_LENGTH:
            raise DomainException(f"Name must be less than {TEXT_MAX_LENGTH} characters")
        if self.genre and len(self.genre) > TEXT_MAX_LENGTH:
            raise DomainException(f"Genre must be less than {TEXT_MAX_LENGTH} characters")
