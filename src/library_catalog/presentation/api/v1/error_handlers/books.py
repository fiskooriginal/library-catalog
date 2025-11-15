import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.library_catalog.domain.exceptions.books import BookAlreadyExistsException, BookNotFoundException

logger = logging.getLogger(__name__)


def setup_books_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(BookNotFoundException)
    async def not_found_handler(request: Request, exc: BookNotFoundException):
        client_ip = request.client.host if request.client else None
        logger.info(
            "Book not found",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "client_ip": client_ip,
                "detail": str(exc),
            },
        )
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "not_found", "detail": str(exc)})

    @app.exception_handler(BookAlreadyExistsException)
    async def already_exists_handler(request: Request, exc: BookAlreadyExistsException):
        client_ip = request.client.host if request.client else None
        logger.warning(
            "Book already exists",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "client_ip": client_ip,
                "detail": str(exc),
            },
        )
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"error": "conflict", "detail": str(exc)})
