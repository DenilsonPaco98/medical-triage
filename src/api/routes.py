"""API routes."""

import logging
import time

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest

from src.api.metrics import MODEL_INFERENCE_DURATION
from src.api.metrics import MODEL_PREDICTIONS
from src.api.schemas import BatchPredictionRequest
from src.api.schemas import HealthResponse
from src.api.schemas import PredictionRequest
from src.api.schemas import PredictionResponse
from src.api.schemas import ScoresResponse
from src.config import settings
from src.models.predict import PredictionResult
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
        start_time = time.perf_counter()
        with MODEL_INFERENCE_DURATION.labels("single").time():
            result = predictor.predict(request.text)
        inference_time = (time.perf_counter() - start_time) * 1000
        MODEL_PREDICTIONS.labels(result["sentiment"]).inc()

        # Type-safe extraction from result dict
        result_text = str(result["text"])
        result_sentiment = str(result["sentiment"])
        result_confidence = result["confidence"]
        result_scores = result["scores"]

        return PredictionResponse(
            text=result_text,
            sentiment=result_sentiment,
            confidence=result_confidence,
            scores=ScoresResponse(
                negative=result_scores["negative"],
                neutral=result_scores["neutral"],
                positive=result_scores["positive"],
            ),
            inference_time_ms=inference_time,
        )

    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/predict-batch")
async def predict_batch(request: BatchPredictionRequest) -> list[PredictionResult]:
    """Predict sentiment for multiple texts.

    Args:
        texts: List of texts to predict

    Returns:
        List of predictions
    """
    try:
        predictor = get_predictor()
        with MODEL_INFERENCE_DURATION.labels("batch").time():
            results = predictor.predict_batch(request.texts)
        for result in results:
            MODEL_PREDICTIONS.labels(result["sentiment"]).inc()
        return results

    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    """Expose Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
