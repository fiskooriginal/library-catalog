from dataclasses import dataclass
from decimal import Decimal

from src.library_catalog.domain.config import RATING_MAX, RATING_MIN, RATING_STEP, TEXT_MAX_LENGTH
from src.library_catalog.domain.exceptions import DomainException


@dataclass(frozen=True, slots=True)
class BookMetadata:
    cover_image_url: str | None
    description: str | None
    rating: Decimal | None

    def __post_init__(self) -> None:
        if self.rating is not None:
            if self.rating < RATING_MIN or self.rating > RATING_MAX:
                raise DomainException(f"Rating must be between {RATING_MIN} and {RATING_MAX}")
            if self.rating.quantize(RATING_STEP) != self.rating:
                raise DomainException(f"Rating must be a multiple of {RATING_STEP}")
        if self.cover_image_url and len(self.cover_image_url) > TEXT_MAX_LENGTH:
            raise DomainException(f"Cover image URL must be less than {TEXT_MAX_LENGTH} characters")
        if self.description and len(self.description) > TEXT_MAX_LENGTH:
            raise DomainException(f"Description must be less than {TEXT_MAX_LENGTH} characters")
