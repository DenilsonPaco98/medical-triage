"""Configuration management using Pydantic Settings."""

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"
    log_format: str = "json"  # json or plain

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_raw_dir: Path = Path("data/raw")
    data_processed_dir: Path = Path("data/processed")
    models_dir: Path = Path("data/models")

    # DuckDB
    duckdb_path: Path = Path("data/processed/medical_reviews.duckdb")
    duckdb_memory_limit: str = "8GB"

    # Kaggle API
    kaggle_username: str = ""
    kaggle_key: str = ""

    # Model
    model_name: str = "distilbert-base-uncased"
    max_seq_length: int = 256
    batch_size: int = 32
    learning_rate: float = 2e-5
    num_epochs: int = 3
    warmup_steps: int = 500
    random_seed: int = 42
    device: str = "cuda"  # cuda or cpu
    num_workers: int = 4

    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "medical-review-sentiment"
    mlflow_registry_uri: str = "sqlite:///mlruns/mlflow.db"
    mlflow_artifact_root: str = "./mlruns"

    # Prefect
    prefect_api_url: str = "http://localhost:4200/api"
    prefect_home: str = "./prefect"

    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8501"]

    # Monitoring
    prometheus_port: int = 9090
    grafana_port: int = 3000

    def __init__(self, **data: object) -> None:
        """Initialize settings and ensure paths exist."""
        super().__init__(**data)
        # Create directories if they don't exist
        self.data_raw_dir.mkdir(parents=True, exist_ok=True)
        self.data_processed_dir.mkdir(parents=True, exist_ok=True)
        self.models_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
