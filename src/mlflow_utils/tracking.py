"""MLflow utilities."""

import logging
from typing import Any

import mlflow

logger = logging.getLogger(__name__)


def log_model_metadata(
    model_name: str,
    params: dict[str, Any],
    metrics: dict[str, float],
    tags: dict[str, str] | None = None,
) -> None:
    """Log model metadata to MLflow.

    Args:
        model_name: Name of the model
        params: Model parameters
        metrics: Model metrics
        tags: Additional tags
    """
    with mlflow.start_run():
        mlflow.set_tag("model_name", model_name)

        # Log parameters
        for key, value in params.items():
            mlflow.log_param(key, value)

        # Log metrics
        for key, value in metrics.items():
            mlflow.log_metric(key, value)

        # Log tags
        if tags:
            for key, value in tags.items():
                mlflow.set_tag(key, value)

        logger.info(f"Logged model {model_name} to MLflow")
