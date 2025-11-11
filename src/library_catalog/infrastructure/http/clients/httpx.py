# import httpx
from typing import Any

from src.library_catalog.infrastructure.config import HttpClientSettings
from src.library_catalog.infrastructure.http.protocol import HttpClientProtocol
from src.library_catalog.infrastructure.http.response import HttpResponse

settings = HttpClientSettings()


class HttpxClient(HttpClientProtocol):
    """HTTP client implementation using httpx library (placeholder for future implementation)."""

    def __init__(
        self,
        auth_token: bytes | None = None,
        timeout: int | None = None,
    ) -> None:
        """Initialize HTTP client with optional configuration."""
        self.auth_token = auth_token
        self.timeout = timeout
        self._client = None

    async def __aenter__(self) -> "HttpxClient":
        """Enter async context manager."""
        # self._client = httpx.AsyncClient(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager."""
        # if self._client:
        #     await self._client.aclose()
        #     self._client = None
        pass

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send GET request."""
        raise NotImplementedError("HttpxClient is not yet implemented")

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send POST request."""
        raise NotImplementedError("HttpxClient is not yet implemented")

    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send PUT request."""
        raise NotImplementedError("HttpxClient is not yet implemented")

    async def patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send PATCH request."""
        raise NotImplementedError("HttpxClient is not yet implemented")

    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send DELETE request."""
        raise NotImplementedError("HttpxClient is not yet implemented")

    async def head(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send HEAD request."""
        raise NotImplementedError("HttpxClient is not yet implemented")

    async def options(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Send OPTIONS request."""
        raise NotImplementedError("HttpxClient is not yet implemented")
