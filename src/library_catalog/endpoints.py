from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.databases import get_session
from src.library_catalog.models import Book
from src.library_catalog.schemas import Book as BookSchema
from src.library_catalog.schemas import BookCreate, BookUpdate

router = APIRouter(prefix="/api")


@router.get("/books", tags=["books"], response_model=list[BookSchema])
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book))
    return result.scalars().all()


@router.get("/books/{uuid}", tags=["books"], response_model=BookSchema)
async def get_book(uuid: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.uuid == uuid))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/books", tags=["books"], response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    db_book = Book(**book.model_dump())
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.put("/books/{uuid}", tags=["books"], response_model=BookSchema)
async def update_book(uuid: UUID, book: BookUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.uuid == uuid))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    for key, value in book.model_dump().items():
        setattr(db_book, key, value)

    await session.commit()
    await session.refresh(db_book)
    return db_book


@router.delete("/books/{uuid}", tags=["books"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(uuid: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(delete(Book).where(Book.uuid == uuid))
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    await session.commit()
