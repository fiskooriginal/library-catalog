from dataclasses import dataclass, field
from typing import TypeVar

from src.library_catalog.domain.exceptions import DomainException


@dataclass(frozen=True, slots=True, kw_only=True)
class PaginationSpec:
    limit: int = 0
    offset: int = 0

    def __post_init__(self) -> None:
        if self.limit < 0:
            raise DomainException("Limit must be greater than or equal to 0")
        if self.offset < 0:
            raise DomainException("Offset must be greater than or equal to 0")


T = TypeVar("T")


@dataclass(frozen=True, slots=True, kw_only=True)
class QueryResult[T]:
    count: int = 0
    offset: int = 0
    limit: int = 0
    data: list[T] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.count < 0:
            raise DomainException("Count must be greater than or equal to 0")
        if self.offset < 0:
            raise DomainException("Offset must be greater than or equal to 0")
        if self.limit < 0:
            raise DomainException("Limit must be greater than or equal to 0")
        if self.data is None:
            raise DomainException("Data must be a list")
