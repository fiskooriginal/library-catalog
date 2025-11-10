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
        name=input.name.strip() if input.name else book.name,
        author=input.author.strip() if input.author else book.author,
        year=input.year if input.year else book.year,
        genre=input.genre.strip() if input.genre else book.genre,
        pages=input.pages if input.pages else book.pages,
        availability=input.availability if input.availability else book.availability,
        metadata=metadata,
    )
