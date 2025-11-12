from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.library_catalog.domain.exceptions.books import BookAlreadyExistsException, BookNotFoundException


def setup_books_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(BookNotFoundException)
    async def not_found_handler(_: Request, exc: BookNotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "not_found", "detail": str(exc)})

    @app.exception_handler(BookAlreadyExistsException)
    async def already_exists_handler(_: Request, exc: BookAlreadyExistsException):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "conflict", "detail": str(exc)})
