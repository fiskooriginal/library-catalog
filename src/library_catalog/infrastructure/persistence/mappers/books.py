from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.library_catalog.domain.config import RATING_STEP
from src.library_catalog.domain.entities.books.book import BookEntity
from src.library_catalog.domain.vo.books import BookAvailability, BookMetadata
from src.library_catalog.infrastructure.persistence.models.books import BookModel
from src.library_catalog.infrastructure.utils import decimal_to_numeric, numeric_to_decimal


def domain_to_model(book: BookEntity) -> BookModel:
    return BookModel(
        uuid=book.uuid,
        created_at=book.created_at,
        updated_at=book.updated_at,
        name=book.name,
        author=book.author,
        year=book.year,
        pages=book.pages,
        genre=book.genre,
        availability=book.availability.value,
        cover_image_url=book.metadata.cover_image_url,
        description=book.metadata.description,
        rating=book.metadata.rating,
    )


def domain_to_dict(book: BookEntity, exclude_none: bool = False) -> dict:
    result = {
        "name": book.name,
        "author": book.author,
        "year": book.year,
        "pages": book.pages,
        "genre": book.genre,
        "availability": book.availability.value,
        "cover_image_url": book.metadata.cover_image_url,
        "description": book.metadata.description,
        "rating": decimal_to_numeric(book.metadata.rating, RATING_STEP),
    }
    if exclude_none:
        result = {key: value for key, value in result.items() if value is not None}
    return result


def model_to_domain(book: BookModel) -> BookEntity:
    return BookEntity(
        uuid=book.uuid,
        created_at=book.created_at,
        updated_at=book.updated_at,
        name=book.name,
        author=book.author,
        year=book.year,
        pages=book.pages,
        genre=book.genre,
        availability=BookAvailability.from_str(book.availability.value),
        metadata=BookMetadata(
            cover_image_url=book.cover_image_url,
            description=book.description,
            rating=numeric_to_decimal(book.rating, RATING_STEP),
        ),
    )


def dict_to_domain(data: dict) -> BookEntity:
    """Convert dict from JSON to BookEntity."""
    return BookEntity(
        uuid=UUID(data["uuid"]) if isinstance(data["uuid"], str) else data["uuid"],
        created_at=datetime.fromisoformat(data["created_at"])
        if isinstance(data["created_at"], str)
        else data["created_at"],
        updated_at=datetime.fromisoformat(data["updated_at"])
        if data.get("updated_at") and isinstance(data["updated_at"], str)
        else data.get("updated_at"),
        name=data["name"],
        author=data["author"],
        year=data["year"],
        pages=data["pages"],
        genre=data["genre"],
        availability=BookAvailability.from_str(data["availability"])
        if isinstance(data["availability"], str)
        else data["availability"],
        metadata=BookMetadata(
            cover_image_url=data.get("cover_image_url"),
            description=data.get("description"),
            rating=Decimal(str(data["rating"])) if data.get("rating") is not None else None,
        ),
    )


def domain_to_json_dict(book: BookEntity) -> dict:
    """Convert BookEntity to dict for JSON serialization."""
    return {
        "uuid": str(book.uuid),
        "created_at": book.created_at.isoformat(),
        "updated_at": book.updated_at.isoformat() if book.updated_at else None,
        "name": book.name,
        "author": book.author,
        "year": book.year,
        "pages": book.pages,
        "genre": book.genre,
        "availability": book.availability.value.value,
        "cover_image_url": book.metadata.cover_image_url,
        "description": book.metadata.description,
        "rating": float(book.metadata.rating) if book.metadata.rating is not None else None,
    }
