from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.library_catalog.application.exceptions import ApplicationException
from src.library_catalog.domain.exceptions import DomainException
from src.library_catalog.presentation.api.v1.error_handlers.books import setup_books_error_handlers


def setup_base_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def exception_handler(_: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "exception", "detail": f"Unexpected error occurred: {exc!s}"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "http", "detail": f"HTTP error occurred: {exc!s}"},
        )


def setup_domain_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(_: Request, exc: DomainException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "domain", "detail": f"Domain error occurred: {exc!s}"},
        )


def setup_application_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(_: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "application", "detail": f"Application error occurred: {exc!s}"},
        )


def setup_error_handlers(app: FastAPI) -> None:
    setup_base_error_handlers(app)
    setup_domain_error_handlers(app)
    setup_application_error_handlers(app)

    # v1 error handlers
    setup_books_error_handlers(app)
