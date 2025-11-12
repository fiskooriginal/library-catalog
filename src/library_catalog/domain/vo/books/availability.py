from dataclasses import dataclass
from enum import StrEnum

from src.library_catalog.domain.exceptions import DomainException


class BookAvailabilityEnum(StrEnum):
    IN_STOCK = "in_stock"
    BORROWED = "borrowed"

    def __str__(self):
        result = str(self.value)
        return result

    @classmethod
    def values(cls) -> list[str]:
        return [availability.value for availability in cls]


@dataclass(frozen=True, slots=True)
class BookAvailability:
    value: BookAvailabilityEnum | str

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            try:
                enum_value = BookAvailabilityEnum(self.value)
            except ValueError as err:
                raise DomainException(
                    f"Invalid availability value: {self.value}. Expected one of: {BookAvailabilityEnum.values()}."
                ) from err
            object.__setattr__(self, "value", enum_value)
        elif not isinstance(self.value, BookAvailabilityEnum):
            raise DomainException(
                f"Invalid availability value: {self.value}. Expected one of: {BookAvailabilityEnum.values()}."
            )

    def __str__(self) -> str:
        return str(self.value)
