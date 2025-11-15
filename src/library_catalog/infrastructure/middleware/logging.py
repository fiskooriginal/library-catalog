import logging
import time
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        start_time = time.time()
        client_ip = request.client.host if request.client else None

        # Log request
        logger.info(
            "Request started",
            extra={
                "request_method": request.method,
                "request_path": str(request.url.path),
                "client_ip": client_ip,
                "query_params": str(request.url.query) if request.url.query else None,
            },
        )

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Log response
            logger.info(
                "Request completed",
                extra={
                    "request_method": request.method,
                    "request_path": str(request.url.path),
                    "status_code": response.status_code,
                    "duration": round(process_time, 3),
                    "client_ip": client_ip,
                },
            )

            return response

        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                extra={
                    "request_method": request.method,
                    "request_path": str(request.url.path),
                    "duration": round(process_time, 3),
                    "client_ip": client_ip,
                    "exception": str(exc),
                },
                exc_info=True,
            )
            raise
