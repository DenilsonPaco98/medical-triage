"""FastAPI application."""

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import routes
from src.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
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
