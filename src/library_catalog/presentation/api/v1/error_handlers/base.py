import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.library_catalog.application.exceptions import ApplicationException
from src.library_catalog.domain.exceptions import DomainException
from src.library_catalog.presentation.api.v1.error_handlers.books import setup_books_error_handlers

logger = logging.getLogger(__name__)


def setup_base_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        client_ip = request.client.host if request.client else None
        logger.exception(
            "Unhandled exception",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "client_ip": client_ip,
                "exception_type": type(exc).__name__,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "internal_server_error", "detail": "An unexpected error occurred"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        client_ip = request.client.host if request.client else None
        logger.warning(
            "HTTP exception",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "status_code": exc.status_code,
                "client_ip": client_ip,
                "detail": str(exc.detail),
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": "http", "detail": str(exc.detail)},
        )


def setup_domain_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        client_ip = request.client.host if request.client else None
        logger.error(
            "Domain exception",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "client_ip": client_ip,
                "exception_type": type(exc).__name__,
                "detail": str(exc),
            },
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "domain", "detail": str(exc)},
        )


def setup_application_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    async def application_exception_handler(request: Request, exc: ApplicationException):
        client_ip = request.client.host if request.client else None
        logger.error(
            "Application exception",
            extra={
                "request_path": request.url.path,
                "request_method": request.method,
                "client_ip": client_ip,
                "exception_type": type(exc).__name__,
                "detail": str(exc),
            },
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "application", "detail": str(exc)},
        )


def setup_error_handlers(app: FastAPI) -> None:
    setup_base_error_handlers(app)
    setup_domain_error_handlers(app)
    setup_application_error_handlers(app)

    # v1 error handlers
    setup_books_error_handlers(app)
