from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.databases import get_session
from src.library_catalog.repository import BookRepository
from src.library_catalog.schemas import Book as BookSchema
from src.library_catalog.schemas import BookCreate, BookUpdate

router = APIRouter(prefix="/api")


def get_book_repository(session: AsyncSession = Depends(get_session)) -> BookRepository:
    return BookRepository(session)


@router.get("/books", tags=["books"], response_model=list[BookSchema])
async def get_books(repository: BookRepository = Depends(get_book_repository)):
    return await repository.get_all()


@router.get("/books/{uuid}", tags=["books"], response_model=BookSchema)
async def get_book(uuid: UUID, repository: BookRepository = Depends(get_book_repository)):
    book = await repository.get_by_id(uuid)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/books", tags=["books"], response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate, repository: BookRepository = Depends(get_book_repository)):
    return await repository.create(book)


@router.put("/books/{uuid}", tags=["books"], response_model=BookSchema)
async def update_book(uuid: UUID, book: BookUpdate, repository: BookRepository = Depends(get_book_repository)):
    db_book = await repository.update(uuid, book)
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return db_book


@router.delete("/books/{uuid}", tags=["books"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(uuid: UUID, repository: BookRepository = Depends(get_book_repository)):
    deleted = await repository.delete(uuid)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
