from enum import Enum


class AvailabilityEnum(str, Enum):
    IN_STOCK = "in_stock"
    BORROWED = "borrowed"
