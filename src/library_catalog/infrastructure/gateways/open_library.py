from collections.abc import Mapping
from contextlib import suppress
from typing import Any

import aiohttp

from src.library_catalog.domain.cache import CacheProtocol
from src.library_catalog.domain.gateways.books.metadata import BookMetadataGatewayProtocol
from src.library_catalog.domain.vo.books import BookMetadata
from src.library_catalog.infrastructure.config import OpenLibrarySettings
from src.library_catalog.infrastructure.gateways.mappers.open_library import map_api_response_to_metadata
from src.library_catalog.infrastructure.http.clients.aiohttp import AioHttpClient


class OpenLibraryGateway(BookMetadataGatewayProtocol):
    def __init__(self, settings: OpenLibrarySettings, cache: CacheProtocol) -> None:
        self.settings = settings
        self._cache = cache

    def _get_cache_key(self, name: str, author: str) -> str:
        return f"metadata:{name}:{author}"

    async def fetch_metadata(self, name: str, author: str) -> BookMetadata | None:
        """
        Получает метаданные книги из Open Library API.

        Args:
            name: Название книги
            author: Автор книги

        Returns:
            BookMetadata или None если данные не найдены
        """
        cache_key = self._get_cache_key(name, author)

        with suppress(Exception):
            cached_data = await self._cache.get(cache_key)
            if cached_data is not None:
                return map_api_response_to_metadata(cached_data)

        document = await self._search(name, author)
        if not document:
            return None

        work_key = document.get("key")
        work_details = await self._fetch_work_details(work_key) if work_key else None

        cover_image_url = self._extract_cover_url(document, work_details)
        description = self._extract_description(work_details)
        rating = self._extract_rating(document, work_details)

        enrichment: dict[str, Any] = {}
        if cover_image_url:
            enrichment["cover_image_url"] = cover_image_url
        if description:
            enrichment["description"] = description
        if rating is not None:
            enrichment["rating"] = rating

        metadata = map_api_response_to_metadata(enrichment)

        with suppress(Exception):
            await self._cache.set(cache_key, enrichment, ttl=self.settings.metadata_cache_ttl)

        return metadata

    async def _search(self, title: str, author: str | None) -> Mapping[str, Any] | None:
        params = {"title": title, "limit": str(self.settings.search_limit)}
        if author:
            params["author"] = author

        data = await self._get_json(self.settings.search_path, params=params)
        if not data:
            return None

        documents = data.get("docs")
        if not isinstance(documents, list) or not documents:
            return None

        first_document = documents[0]
        if not isinstance(first_document, Mapping):
            return None
        return first_document

    async def _fetch_work_details(self, work_key: str) -> Mapping[str, Any] | None:
        normalized_key = work_key.strip("/")
        if not normalized_key:
            return None

        path = f"/{normalized_key}"
        if not normalized_key.endswith(".json"):
            path = f"{path}.json"

        if not path.startswith("/works/"):
            path = f"/works/{normalized_key}.json"

        data = await self._get_json(path)
        if not isinstance(data, Mapping):
            return None
        return data

    async def _get_json(self, path: str, params: dict[str, str] | None = None) -> Any:
        url = f"{self.settings.base_url}{path}"

        timeout = aiohttp.ClientTimeout(total=self.settings.request_timeout_seconds)

        async with AioHttpClient(timeout=timeout) as client:
            response = await client.get(url, params=params)

            if not response.is_success():
                return None
            return response.data

    def _extract_cover_url(self, document: Mapping[str, Any], work_details: Mapping[str, Any] | None) -> str | None:
        cover_id = document.get("cover_i")
        if cover_id is None and work_details:
            covers = work_details.get("covers")
            if isinstance(covers, list) and covers:
                cover_id = covers[0]

        try:
            cover_id_int = int(cover_id)
        except (TypeError, ValueError):
            return None

        return self.settings.covers_url_template.format(cover_id=cover_id_int)

    def _extract_description(self, work_details: Mapping[str, Any] | None) -> str | None:
        if not work_details:
            return None

        description = work_details.get("description")
        if isinstance(description, str):
            stripped = description.strip()
            return stripped or None

        if isinstance(description, Mapping):
            value = description.get("value")
            if isinstance(value, str):
                stripped = value.strip()
                return stripped or None

        return None

    def _extract_rating(self, document: Mapping[str, Any], work_details: Mapping[str, Any] | None) -> float | None:
        rating = document.get("ratings_average")

        if rating is None and work_details:
            rating = work_details.get("ratings_average")

        if rating is None:
            return None

        # Возвращаем как float, маппер сконвертирует в Decimal
        try:
            return float(rating)
        except (TypeError, ValueError):
            return None
