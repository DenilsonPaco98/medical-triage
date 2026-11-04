"""Prefect flow for sentiment analysis pipeline."""

from pathlib import Path

import pandas as pd
from prefect import flow
from prefect import task

from src.data.dataset import prepare_dataset
from src.data.preprocessing import DataPreprocessor


@task(retries=2, retry_delay_seconds=5)
def load_dataset() -> str:
    """Load dataset from Kaggle."""
    path = prepare_dataset()
    return str(path)


@task
def preprocess_data(dataset_path: str) -> str:
    """Preprocess dataset."""
    df = pd.read_csv(dataset_path)
    preprocessor = DataPreprocessor()
    df_clean = preprocessor.clean(df)

    output_path = dataset_path.replace(".csv", "_processed.csv")
    df_clean.to_csv(output_path, index=False)

    return output_path


@task
def train_model(processed_data_path: str) -> dict:
    """Train sentiment model."""
    # This would integrate with your training pipeline
    return {"status": "trained", "model_path": "data/models/bert_sentiment_model.pt"}


@flow(name="sentiment-training-pipeline")
def sentiment_pipeline() -> None:
    """Complete sentiment analysis pipeline."""
    dataset_path = load_dataset()
    processed_path = preprocess_data(dataset_path)
    model_info = train_model(processed_path)

    print(f"Pipeline completed: {model_info}")


if __name__ == "__main__":
    sentiment_pipeline()
