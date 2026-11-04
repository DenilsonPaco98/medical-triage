"""API routes."""

import logging
import time
from typing import Any

from fastapi import APIRouter
from fastapi import HTTPException

from src.api.schemas import HealthResponse
from src.api.schemas import PredictionRequest
from src.api.schemas import PredictionResponse
from src.config import settings
from src.models.predict import SentimentPredictor

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize predictor (lazy loading)
_predictor = None


def get_predictor() -> SentimentPredictor:
    """Get or initialize sentiment predictor."""
    global _predictor
    if _predictor is None:
        logger.info("Initializing SentimentPredictor...")
        model_path = settings.models_dir / "bert_sentiment_model.pt"
        _predictor = SentimentPredictor(
            model_path=model_path if model_path.exists() else None,
            model_name=settings.model_name,
            device=settings.device,
        )
    return _predictor


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.2.0")


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest) -> PredictionResponse:
    """Predict sentiment for a single text.

    Args:
        request: Prediction request with text

    Returns:
        Prediction response with sentiment and confidence
    """
    try:
        predictor = get_predictor()
        start_time = time.time()

        result = predictor.predict(request.text)

        inference_time = (time.time() - start_time) * 1000

        return PredictionResponse(
            text=result["text"],
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            scores=result["scores"],
            inference_time_ms=inference_time,
        )

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/predict-batch")
async def predict_batch(texts: list[str]) -> list[dict[str, Any]]:
    """Predict sentiment for multiple texts.

    Args:
        texts: List of texts to predict

    Returns:
        List of predictions
    """
    try:
        if not texts:
            raise HTTPException(status_code=400, detail="No texts provided")

        predictor = get_predictor()
        results = predictor.predict_batch(texts)
        return results

    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e
