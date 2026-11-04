"""API request/response schemas."""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class PredictionRequest(BaseModel):
    """Request schema for sentiment prediction."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Excelente atendimento do médico!",
                "model_version": "production",
            }
        }
    )

    text: str = Field(..., min_length=1, max_length=2000, description="Text to analyze")
    model_version: str | None = Field(None, description="Model version to use")


class ScoresResponse(BaseModel):
    """Sentiment scores."""

    negative: float = Field(..., ge=0, le=1)
    neutral: float = Field(..., ge=0, le=1)
    positive: float = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    """Response schema for sentiment prediction."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Excelente atendimento do médico!",
                "sentiment": "positive",
                "confidence": 0.98,
                "scores": {"positive": 0.98, "neutral": 0.015, "negative": 0.005},
                "inference_time_ms": 45.23,
            }
        }
    )

    text: str
    sentiment: str = Field(..., description="Predicted sentiment: positive, neutral, or negative")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")
    scores: ScoresResponse
    inference_time_ms: float = Field(..., description="Inference time in milliseconds")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
