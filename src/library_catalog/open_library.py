import logging
from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

import aiohttp

from src.library_catalog.api_client import AioHttpClient
from src.library_catalog.enums import MethodsEnum
from src.library_catalog.settings import OpenLibrarySettings

LOGGER = logging.getLogger(__name__)

settings = OpenLibrarySettings()


class OpenLibraryClient:
    async def fetch_book_details(self, title: str, author: str | None = None) -> dict[str, Any] | None:
        document = await self._search(title, author)
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

        return enrichment or None

    async def _search(self, title: str, author: str | None) -> Mapping[str, Any] | None:
        params = {"title": title, "limit": str(settings.search_limit)}
        if author:
            params["author"] = author

        data = await self._get_json(settings.search_path, params=params)
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
        url = f"{settings.base_url}{path}"

        timeout = aiohttp.ClientTimeout(total=settings.request_timeout_seconds)
        client = AioHttpClient(url, method=MethodsEnum.GET, params=params, timeout=timeout)

        try:
            response = await client.send()
            status_code = response.get("status_code")
            data = response.get("data")

            if status_code and 200 <= status_code <= 299:
                return data

            LOGGER.warning("Open Library request failed with status %s: %s", status_code, data)
            return None
        except Exception as exc:
            LOGGER.warning("Open Library request failed: %s", exc)
            return None

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

        return settings.covers_url_template.format(cover_id=cover_id_int)

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

    def _extract_rating(self, document: Mapping[str, Any], work_details: Mapping[str, Any] | None) -> Decimal | None:
        rating = document.get("ratings_average")

        if rating is None and work_details:
            rating = work_details.get("ratings_average")

        try:
            rating_decimal = Decimal(str(rating))
        except (InvalidOperation, ValueError):
            return None

        quantized_rating = rating_decimal.quantize(settings.rating_quant, rounding=ROUND_HALF_UP)

        if quantized_rating < settings.rating_min or quantized_rating > settings.rating_max:
            return None

        return float(quantized_rating)
