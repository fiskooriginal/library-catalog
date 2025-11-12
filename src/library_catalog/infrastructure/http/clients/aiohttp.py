import json
from typing import Any

import aiohttp

from src.library_catalog.infrastructure.config import HttpClientSettings
from src.library_catalog.infrastructure.http.protocol import HttpClientProtocol
from src.library_catalog.infrastructure.http.response import HttpResponse

settings = HttpClientSettings()


class AioHttpClient(HttpClientProtocol):
    def __init__(
        self,
        auth_token: bytes | None = None,
        timeout: aiohttp.ClientTimeout | None = None,
    ) -> None:
        self.auth_token = auth_token
        self.timeout = timeout
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> "AioHttpClient":
        self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    def _build_headers(
        self,
        custom_headers: dict[str, str] | None = None,
        include_content_type: bool = False,
    ) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token.decode('utf-8')}"
        if include_content_type:
            headers["Content-Type"] = "application/json"
        if custom_headers:
            headers.update(custom_headers)
        return headers

    def _prepare_payload(self, data: dict[str, Any] | None) -> str | None:
        if data is None:
            return None
        return json.dumps(data)

    async def _parse_response(self, response: aiohttp.ClientResponse) -> HttpResponse:
        status_code = response.status
        headers = dict(response.headers.items())

        if settings.success_status_min <= status_code <= settings.success_status_max:
            try:
                data = await response.json()
            except (aiohttp.ContentTypeError, json.JSONDecodeError):
                data = await response.text()
            return HttpResponse(status_code=status_code, data=data, headers=headers)

        if status_code == settings.no_content_status:
            return HttpResponse(status_code=status_code, data=None, headers=headers)

        try:
            data = await response.text()
        except Exception:
            data = None
        return HttpResponse(status_code=status_code, data=data, headers=headers)

    def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            raise RuntimeError(
                "HTTP client session not initialized. Use 'async with AioHttpClient() as client:' pattern."
            )
        return self._session

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers)
        async with session.get(url, headers=request_headers, params=params) as response:
            return await self._parse_response(response)

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers, include_content_type=True)
        payload = self._prepare_payload(data)
        async with session.post(url, headers=request_headers, data=payload, params=params) as response:
            return await self._parse_response(response)

    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers, include_content_type=True)
        payload = self._prepare_payload(data)
        async with session.put(url, headers=request_headers, data=payload, params=params) as response:
            return await self._parse_response(response)

    async def patch(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers, include_content_type=True)
        payload = self._prepare_payload(data)
        async with session.patch(url, headers=request_headers, data=payload, params=params) as response:
            return await self._parse_response(response)

    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers)
        async with session.delete(url, headers=request_headers, params=params) as response:
            return await self._parse_response(response)

    async def head(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers)
        async with session.head(url, headers=request_headers, params=params) as response:
            return await self._parse_response(response)

    async def options(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        session = self._ensure_session()
        request_headers = self._build_headers(headers)
        async with session.options(url, headers=request_headers, params=params) as response:
            return await self._parse_response(response)
