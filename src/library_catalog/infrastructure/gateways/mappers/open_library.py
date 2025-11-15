from typing import Any

from src.library_catalog.domain.config import TEXT_MAX_LENGTH
from src.library_catalog.domain.vo.books import BookMetadata
from src.library_catalog.infrastructure.utils import to_decimal


def map_api_response_to_metadata(api_data: dict[str, Any]) -> BookMetadata | None:
    if not api_data:
        return None

    cover_image_url = api_data.get("cover_image_url")
    description = api_data.get("description")
    rating_raw = api_data.get("rating")

    if description and len(description) > TEXT_MAX_LENGTH:
        description = description[:TEXT_MAX_LENGTH]

    if cover_image_url and len(cover_image_url) > TEXT_MAX_LENGTH:
        cover_image_url = cover_image_url[:TEXT_MAX_LENGTH]

    rating = to_decimal(rating_raw) if rating_raw is not None else None

    if cover_image_url is None and description is None and rating is None:
        return None

    return BookMetadata(cover_image_url=cover_image_url, description=description, rating=rating)
