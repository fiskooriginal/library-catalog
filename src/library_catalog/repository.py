from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.models import Book
from src.library_catalog.open_library import OpenLibraryClient
from src.library_catalog.schemas import BookCreate, BookUpdate


class BookRepository:
    def __init__(self, session: AsyncSession, open_library_client: OpenLibraryClient | None = None):
        self.session = session
        self.open_library_client = open_library_client

    async def _enrich_book_data(self, book_dict: dict) -> dict:
        if not self.open_library_client:
            return book_dict

        enrichment = await self.open_library_client.fetch_book_details(book_dict["name"], book_dict["author"])
        if enrichment:
            for key, value in enrichment.items():
                if book_dict.get(key) is None and value is not None:
                    book_dict[key] = value

        return book_dict

    async def create(self, request: BookCreate) -> Book:
        book_dict = await self._enrich_book_data({**request.model_dump()})
        book = Book(**book_dict)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def get_by_id(self, uuid: UUID) -> Book | None:
        result = await self.session.execute(select(Book).where(Book.uuid == uuid))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Book]:
        result = await self.session.execute(select(Book))
        return list(result.scalars().all())

    async def update(self, uuid: UUID, request: BookUpdate) -> Book | None:
        update_dict = request.model_dump(exclude_unset=True)
        await self.session.execute(update(Book).where(Book.uuid == uuid).values(**update_dict))
        await self.session.commit()
        return await self.get_by_id(uuid)

    async def delete(self, uuid: UUID) -> bool:
        result = await self.session.execute(delete(Book).where(Book.uuid == uuid))
        await self.session.commit()
        return result.rowcount > 0
