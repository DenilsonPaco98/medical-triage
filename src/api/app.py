"""FastAPI application."""

import logging
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from src.api import routes
from src.api.metrics import HTTP_REQUEST_DURATION
from src.api.metrics import HTTP_REQUESTS
from src.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> Any:
    """Application lifespan context manager.

    This ensures the model is loaded on startup and any cleanup is done on shutdown.
    """
    logger.info("Starting up Medical Review Sentiment API...")
    # Load model on startup (optional - can be lazy loaded)
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Medical Review Sentiment API",
    description="API for sentiment analysis of medical reviews using fine-tuned BERT",
    version="0.2.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next: Any) -> Any:
    """Record request count and latency using the matched route template."""
    started_at = time.perf_counter()
    status_code = "500"
    try:
        response = await call_next(request)
        status_code = str(response.status_code)
        return response
    finally:
        route = request.scope.get("route")
        endpoint = getattr(route, "path", "unmatched")
        HTTP_REQUESTS.labels(request.method, endpoint, status_code).inc()
        HTTP_REQUEST_DURATION.labels(request.method, endpoint).observe(
            time.perf_counter() - started_at,
        )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
