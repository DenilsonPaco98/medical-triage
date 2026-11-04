.PHONY: help install install-dev lint format typecheck test test-cov check clean docker-build docker-up docker-down prepare-data train evaluate export-onnx benchmark-latency serve serve-dev mlflow-ui airflow-ui airflow-start benchmark

# Color output
BLUE = \033[0;34m
GREEN = \033[0;32m
RED = \033[0;31m
NC = \033[0m # No Color

help:
	@echo "$(BLUE)Medical Review Sentiment Analysis - MLOps Pipeline$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Install:$(NC)"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install all dependencies (dev, lint, test, ml)"
	@echo ""
	@echo "$(GREEN)Code Quality (CI/CD):$(NC)"
	@echo "  make lint             - Run ruff linter (Criterion 2)"
	@echo "  make format           - Format code with ruff"
	@echo "  make typecheck        - Run mypy type checking (Criterion 2)"
	@echo "  make check            - Run lint + typecheck"
	@echo ""
	@echo "$(GREEN)Testing (CI/CD):$(NC)"
	@echo "  make test             - Run pytest suite (Criterion 2)"
	@echo "  make test-cov         - Run pytest with coverage report"
	@echo ""
	@echo "$(GREEN)Data Pipeline (Criterion 1,3):$(NC)"
	@echo "  make prepare-data     - Download dataset from Kaggle"
	@echo "  make train            - Fine-tune BERT model (with MLflow)"
	@echo "  make evaluate         - Evaluate model on test set"
	@echo ""
	@echo "$(GREEN)Model Optimization (Criterion 1):$(NC)"
	@echo "  make export-onnx      - Convert PyTorch → ONNX"
	@echo "  make benchmark-latency - Benchmark PyTorch vs ONNX latency"
	@echo ""
	@echo "$(GREEN)Orchestration (Criterion 3):$(NC)"
	@echo "  make airflow-start    - Start Airflow webserver & scheduler"
	@echo "  make airflow-ui       - Open Airflow UI (http://localhost:4200)"
	@echo ""
	@echo "$(GREEN)API Server:$(NC)"
	@echo "  make serve            - Run FastAPI server (production)"
	@echo "  make serve-dev        - Run FastAPI server (development)"
	@echo ""
	@echo "$(GREEN)Monitoring (Criterion 4):$(NC)"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start full Docker Compose stack"
	@echo "  make docker-down      - Stop Docker Compose stack"
	@echo "  make docker-logs      - Show Docker logs"
	@echo "  make mlflow-ui        - Open MLflow UI (http://localhost:5000)"
	@echo ""
	@echo "$(GREEN)Cleanup:$(NC)"
	@echo "  make clean            - Remove build artifacts and cache"
	@echo "  make clean-all        - Remove all generated files"
	@echo ""

# =====================================================================
# Setup
# =====================================================================

install:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	uv sync

install-dev:
	@echo "$(GREEN)Installing all dependencies (including dev & ml)...$(NC)"
	uv sync --extra dev --extra ml --extra llm --extra ui --extra serving --extra lint

# =====================================================================
# Code Quality
# =====================================================================

lint:
	@echo "$(GREEN)Running ruff linter...$(NC)"
	uv run ruff check src tests

format:
	@echo "$(GREEN)Formatting code with ruff...$(NC)"
	uv run ruff format src tests

typecheck:
	@echo "$(GREEN)Running mypy type checker...$(NC)"
	uv run mypy src

check: lint typecheck
	@echo "$(GREEN)All checks passed!$(NC)"

# =====================================================================
# Testing
# =====================================================================

test:
	@echo "$(GREEN)Running tests...$(NC)"
	uv run pytest tests -v

test-cov:
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	uv run pytest tests -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report: htmlcov/index.html"

test-watch:
	@echo "$(GREEN)Running tests in watch mode (Ctrl+C to exit)...$(NC)"
	uv run pytest-watch tests

test-specific:
	@echo "Usage: make test-specific TEST=tests/test_models.py::test_bert_training"
	uv run pytest $(TEST) -v

# =====================================================================
# Data & Model
# =====================================================================

prepare-data:
	@echo "$(GREEN)Preparing dataset from Kaggle...$(NC)"
	uv run python -m src.data.dataset prepare

train:
	@echo "$(GREEN)Training BERT model (with MLflow tracking)...$(NC)"
	uv run python -m src.models.train_bert

evaluate:
	@echo "$(GREEN)Evaluating model on test set...$(NC)"
	uv run python -m src.models.evaluate

export-onnx:
	@echo "$(GREEN)Converting model to ONNX format...$(NC)"
	uv run python -c "from src.models.onnx_converter import ONNXConverter; c = ONNXConverter('data/models/bert_sentiment_model.pt'); c.convert(); c.validate()"

benchmark-latency:
	@echo "$(GREEN)Benchmarking inference latency (PyTorch vs ONNX)...$(NC)"
	uv run python -c "from src.models.benchmark import LatencyBenchmark; b = LatencyBenchmark(); results = b.compare('data/models/bert_sentiment_model.pt', 'data/models/sentiment_model.onnx'); print(results)"

# =====================================================================
# Serving
# =====================================================================

serve:
	@echo "$(GREEN)Starting FastAPI server (production)...$(NC)"
	uv run uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --workers 4

serve-dev:
	@echo "$(GREEN)Starting FastAPI server (development with reload)...$(NC)"
	uv run uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

# =====================================================================
# Monitoring & Dashboards
# =====================================================================

mlflow-ui:
	@echo "$(GREEN)Starting MLflow UI (http://localhost:5000)...$(NC)"
	uv run mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db --default-artifact-root ./mlruns

# =====================================================================
# Orchestration (Airflow)
# =====================================================================

airflow-start:
	@echo "$(GREEN)Starting Airflow (webserver + scheduler)...$(NC)"
	@echo "$(BLUE)Make sure AIRFLOW_HOME is set in .env$(NC)"
	@echo "$(BLUE)Terminal 1: airflow webserver -p 8080$(NC)"
	@echo "$(BLUE)Terminal 2: airflow scheduler$(NC)"
	@echo "$(BLUE)UI: http://localhost:4200 (docker-compose remaps 8080→4200)$(NC)"

airflow-ui:
	@echo "$(GREEN)Opening Airflow UI (make sure server is running)...$(NC)"
	@python -c "import webbrowser; webbrowser.open('http://localhost:4200')" 2>/dev/null || echo "Open: http://localhost:4200"

# =====================================================================
# Docker
# =====================================================================

docker-build:
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t medical-review-sentiment:latest .

docker-up:
	@echo "$(GREEN)Starting Docker Compose stack...$(NC)"
	docker-compose up -d
	@echo ""
	@echo "$(BLUE)Services Started:$(NC)"
	@echo "  ✓ API (FastAPI):        http://localhost:8000"
	@echo "  ✓ MLflow:               http://localhost:5000"
	@echo "  ✓ Airflow:              http://localhost:4200"
	@echo "  ✓ Prometheus:           http://localhost:9090"
	@echo "  ✓ Grafana:              http://localhost:3000 (admin/admin)"
	@echo ""
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Wait ~30s for services to start"
	@echo "  2. Open Grafana: http://localhost:3000"
	@echo "  3. Configure Prometheus data source (localhost:9090)"
	@echo "  4. Generate metrics:"
	@echo "     for i in {1..100}; do curl -X POST http://localhost:8000/predict -H 'Content-Type: application/json' -d '{\"text\": \"Great doctor!\"}'; done"
	@echo ""

docker-down:
	@echo "$(GREEN)Stopping Docker Compose stack...$(NC)"
	docker-compose down

docker-logs:
	@echo "$(GREEN)Showing Docker logs...$(NC)"
	docker-compose logs -f

docker-clean:
	@echo "$(RED)Removing Docker images and volumes...$(NC)"
	docker-compose down -v
	docker rmi medical-review-sentiment:latest 2>/dev/null || true

# =====================================================================
# Cleanup
# =====================================================================

clean:
	@echo "$(GREEN)Removing build artifacts and cache...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage

clean-all: clean
	@echo "$(RED)Removing all generated files...$(NC)"
	rm -rf data/raw/* data/processed/* .dvc/cache mlruns/ .venv/
	rm -f .env

# =====================================================================
# Development Utilities
# =====================================================================

pre-commit-install:
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	uv run pre-commit install

pre-commit-run:
	@echo "$(GREEN)Running pre-commit hooks...$(NC)"
	uv run pre-commit run --all-files

requirements-txt:
	@echo "$(GREEN)Generating requirements.txt...$(NC)"
	uv pip compile -o requirements.txt

jupyter:
	@echo "$(GREEN)Starting Jupyter Lab...$(NC)"
	uv run jupyter lab notebooks/

version:
	@echo "$(BLUE)medical-review-sentiment-mlops v0.2.0$(NC)"
