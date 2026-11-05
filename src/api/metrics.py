"""Prometheus metrics for API traffic and model inference."""

from prometheus_client import Counter
from prometheus_client import Histogram

HTTP_REQUESTS = Counter(
    "medical_triage_http_requests_total",
    "Total HTTP requests handled by the API.",
    ("method", "endpoint", "status_code"),
)
HTTP_REQUEST_DURATION = Histogram(
    "medical_triage_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ("method", "endpoint"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
)
MODEL_INFERENCE_DURATION = Histogram(
    "medical_triage_model_inference_duration_seconds",
    "Model inference duration in seconds.",
    ("operation",),
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30),
)
MODEL_PREDICTIONS = Counter(
    "medical_triage_model_predictions_total",
    "Number of successful model predictions by sentiment.",
    ("sentiment",),
)
