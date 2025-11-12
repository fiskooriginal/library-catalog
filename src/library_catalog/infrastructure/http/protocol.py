from abc import abstractmethod
from typing import Any, Protocol

from src.library_catalog.infrastructure.http.response import HttpResponse


class HttpClientProtocol(Protocol):
    @abstractmethod
    async def get(
        self, url: str, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None
    ) -> HttpResponse: ...

    @abstractmethod
    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...

    @abstractmethod
    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...

    @abstractmethod
    async def patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...

    @abstractmethod
    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...

    @abstractmethod
    async def head(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...

    @abstractmethod
    async def options(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse: ...

    @abstractmethod
    async def __aenter__(self) -> "HttpClientProtocol": ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
