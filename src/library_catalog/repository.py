from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.models import Book
from src.library_catalog.schemas import BookCreate, BookUpdate


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, book_data: BookCreate) -> Book:
        db_book = Book(**book_data.model_dump())
        self.session.add(db_book)
        await self.session.commit()
        await self.session.refresh(db_book)
        return db_book

    async def get_by_id(self, uuid: UUID) -> Book | None:
        result = await self.session.execute(select(Book).where(Book.uuid == uuid))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Book]:
        result = await self.session.execute(select(Book))
        return list(result.scalars().all())

    async def update(self, uuid: UUID, book_data: BookUpdate) -> Book | None:
        result = await self.session.execute(select(Book).where(Book.uuid == uuid))
        db_book = result.scalar_one_or_none()
        if not db_book:
            return None

        for key, value in book_data.model_dump().items():
            setattr(db_book, key, value)

        await self.session.commit()
        await self.session.refresh(db_book)
        return db_book

    async def delete(self, uuid: UUID) -> bool:
        result = await self.session.execute(delete(Book).where(Book.uuid == uuid))
        await self.session.commit()
        return result.rowcount > 0
