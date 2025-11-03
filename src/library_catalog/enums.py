from enum import Enum


class MethodsEnum(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    def __str__(self):
        return self.value

    @classmethod
    def values(cls) -> list[str]:
        return [method.value for method in cls]


class AvailabilityEnum(str, Enum):
    IN_STOCK = "in_stock"
    BORROWED = "borrowed"

    def __str__(self):
        return self.value
