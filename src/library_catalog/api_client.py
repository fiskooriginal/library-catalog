import json
from typing import Protocol, Union

import aiohttp

from src.library_catalog.enums import MethodsEnum
from src.library_catalog.settings import HttpClientSettings

settings = HttpClientSettings()


class HttpClientProtocol(Protocol):
    async def send(self) -> dict: ...


class HttpResponseBuilder:
    @staticmethod
    def success(
        status_code: int = settings.default_success_status, data: Union[dict, list, str, int, None] = None
    ) -> dict:
        return {"status_code": status_code, "data": data or {}}

    @staticmethod
    def error(
        status_code: int = settings.default_error_status,
        data: str = settings.default_error_message,
    ) -> dict:
        return {"status_code": status_code, "data": data}


class AioHttpClient:
    def __init__(
        self,
        url: str,
        method: MethodsEnum,
        auth_token: bytes | None = None,
        data_to_send: dict | None = None,
        params: dict[str, str] | None = None,
        timeout: aiohttp.ClientTimeout | None = None,
    ) -> None:
        self.url = url
        self.method = method
        self.auth_token = auth_token
        self.data_to_send = data_to_send or {}
        self.params = params
        self.timeout = timeout

    def _build_headers(self) -> dict:
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token.decode('utf-8')}"
        if self.method in (MethodsEnum.POST, MethodsEnum.PUT, MethodsEnum.PATCH):
            headers["Content-Type"] = "application/json"
        return headers

    def _prepare_payload(self) -> str:
        return json.dumps(self.data_to_send)

    def _get_query_params(self) -> dict[str, str] | None:
        if self.params:
            return self.params
        if self.method == MethodsEnum.GET and self.data_to_send:
            return {str(k): str(v) for k, v in self.data_to_send.items()}
        return None

    async def _parse_response(self, response: aiohttp.ClientResponse) -> dict:
        if settings.success_status_min <= response.status <= settings.success_status_max:
            return HttpResponseBuilder.success(response.status, await response.json())
        if response.status == settings.no_content_status:
            return HttpResponseBuilder.success(response.status, {})
        return HttpResponseBuilder.error(response.status, await response.text())

    async def _execute_request(self, session: aiohttp.ClientSession) -> dict:
        headers = self._build_headers()
        query_params = self._get_query_params()

        if self.method == MethodsEnum.GET:
            response = await session.get(self.url, headers=headers, params=query_params)
        elif self.method == MethodsEnum.POST:
            payload = self._prepare_payload()
            response = await session.post(self.url, headers=headers, data=payload, params=query_params)
        elif self.method == MethodsEnum.PUT:
            payload = self._prepare_payload()
            response = await session.put(self.url, headers=headers, data=payload, params=query_params)
        elif self.method == MethodsEnum.PATCH:
            payload = self._prepare_payload()
            response = await session.patch(self.url, headers=headers, data=payload, params=query_params)
        elif self.method == MethodsEnum.DELETE:
            response = await session.delete(self.url, headers=headers, params=query_params)
        else:
            return HttpResponseBuilder.error(
                settings.method_not_allowed_status,
                f"Not allowed method, choose from: {MethodsEnum.values()}",
            )

        return await self._parse_response(response)

    async def send(self) -> dict:
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            return await self._execute_request(session)
