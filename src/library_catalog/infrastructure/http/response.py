from dataclasses import dataclass, field
from typing import Any

from src.library_catalog.infrastructure.config import HttpClientSettings

settings = HttpClientSettings()


@dataclass
class HttpResponse:
    """HTTP response model with type-safe attributes."""

    status_code: int
    data: Any = None
    headers: dict[str, str] | None = field(default=None)

    @classmethod
    def from_dict(cls, response_dict: dict[str, Any]) -> "HttpResponse":
        """
        Create HttpResponse from dictionary.

        Args:
            response_dict: Dictionary with status_code, data, and optionally headers

        Returns:
            HttpResponse instance
        """
        return cls(
            status_code=response_dict.get("status_code", settings.default_error_status),
            data=response_dict.get("data"),
            headers=response_dict.get("headers"),
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert HttpResponse to dictionary.

        Returns:
            Dictionary representation of the response
        """
        result: dict[str, Any] = {
            "status_code": self.status_code,
            "data": self.data,
        }
        if self.headers is not None:
            result["headers"] = self.headers
        return result

    def is_success(self) -> bool:
        """
        Check if response status code indicates success.

        Returns:
            True if status code is in success range (200-299 or 204)
        """
        return (
            settings.success_status_min <= self.status_code <= settings.success_status_max
            or self.status_code == settings.no_content_status
        )
