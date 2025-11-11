from abc import abstractmethod
from typing import Any, Protocol

from src.library_catalog.infrastructure.http.response import HttpResponse


class HttpClientProtocol(Protocol):
    """Protocol for HTTP client implementations with support for all HTTP methods."""

    @abstractmethod
    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send GET request."""
        ...

    @abstractmethod
    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send POST request."""
        ...

    @abstractmethod
    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send PUT request."""
        ...

    @abstractmethod
    async def patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send PATCH request."""
        ...

    @abstractmethod
    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send DELETE request."""
        ...

    @abstractmethod
    async def head(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send HEAD request."""
        ...

    @abstractmethod
    async def options(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send OPTIONS request."""
        ...

    @abstractmethod
    async def __aenter__(self) -> "HttpClientProtocol":
        """Enter async context manager."""
        ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager."""
        ...
