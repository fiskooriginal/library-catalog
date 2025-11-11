from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from src.library_catalog.domain.exceptions import DomainException


class BookAvailabilityEnum(StrEnum):
    IN_STOCK = "in_stock"
    BORROWED = "borrowed"

    def __str__(self):
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        return [availability.value for availability in cls]


@dataclass(frozen=True, slots=True)
class BookAvailability:
    value: BookAvailabilityEnum

    def __post_init__(self) -> None:
        if not isinstance(self.value, BookAvailabilityEnum):
            raise DomainException(
                f"Invalid availability value: {self.value}. Expected one of: {BookAvailabilityEnum.values()}."
            )

    @classmethod
    def from_str(cls, value: str) -> Self:
        return cls(BookAvailabilityEnum(value))
