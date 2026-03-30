import time
import uuid

import structlog
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.stdlib.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(  # noqa: PLR6301
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = str(uuid.uuid4())

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )
        if request.url.query:
            structlog.contextvars.bind_contextvars(
                query_string=request.url.query,
            )
        # TODO: возможно сохранять ip запрещено  # noqa: TD002, TD003
        if request.client:
            structlog.contextvars.bind_contextvars(
                host=request.client.host,
                port=request.client.port,
            )

        start = time.perf_counter()
        logger.info("request.started")

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "request.failed",
                duration_ms=round((time.perf_counter() - start) * 1000, 2),
            )
            raise

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request.finished",
            status_code=response.status_code,
            duration_ms=round((time.perf_counter() - start) * 1000, 2),
        )
        return response
