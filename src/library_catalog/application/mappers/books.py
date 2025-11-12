from src.library_catalog.application.dtos.books import CreateBookInput, UpdateBookInput
from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.vo.books import BookMetadata


def create_domain_book(input: CreateBookInput, metadata: BookMetadata) -> BookEntity:
    return BookEntity(
        name=input.name.strip(),
        author=input.author.strip(),
        year=input.year,
        genre=input.genre.strip(),
        pages=input.pages,
        availability=input.availability,
        metadata=metadata,
    )


def get_updated_domain_book(book: BookEntity, metadata: BookMetadata, input: UpdateBookInput) -> BookEntity:
    return BookEntity(
        uuid=book.uuid,
        created_at=book.created_at,
        updated_at=book.updated_at,
        name=input.name.strip() if input.name is not None else book.name,
        author=input.author.strip() if input.author is not None else book.author,
        genre=input.genre.strip() if input.genre is not None else book.genre,
        year=input.year if input.year is not None else book.year,
        pages=input.pages if input.pages is not None else book.pages,
        availability=input.availability if input.availability is not None else book.availability,
        metadata=metadata,
    )
