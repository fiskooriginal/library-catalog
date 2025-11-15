import logging
import time
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        # Add timing header
        response.headers["X-Process-Time"] = str(round(process_time, 6))

        # Log slow requests (more than 1 second)
        if process_time > 1.0:
            logger.warning(
                "Slow request detected",
                extra={
                    "method": request.method,
                    "path": str(request.url.path),
                    "duration": round(process_time, 3),
                },
            )

        return response
