"""Quick start guide for the Medical Review Sentiment Analysis project."""

# Quick Start Guide

## Installation (5 minutes)

### 1. Prerequisites
- Python 3.11+
- uv package manager
- Git

### 2. Clone and Setup
```bash
git clone https://github.com/DenilsonPaco98/medical-review-sentiment-mlops
cd medical-review-sentiment-mlops

# Create virtual environment
uv venv

# Activate (choose one)
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
uv sync --extra dev --extra ml --extra ui
```

### 3. Prepare Data
```bash
# Download dataset from Kaggle (requires credentials)
make prepare-data

# Or use sample data (auto-generated)
```

### 4. Run Streamlit Dashboard
```bash
streamlit run src/ui/dashboard.py
# Open: http://localhost:8501
```

### 5. Start FastAPI Server
```bash
make serve-dev
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 6. Launch MLflow UI
```bash
make mlflow-ui
# Open: http://localhost:5000
```

## Docker Quick Start

```bash
# Build image
make docker-build

# Start all services
make docker-up

# Services running:
# - API: http://localhost:8000
# - Streamlit: http://localhost:8501
# - MLflow: http://localhost:5000
# - Grafana: http://localhost:3000 (admin/admin)

# Stop services
make docker-down
```

## Training Your First Model

### Option A: Command Line (Simple)
```bash
make train
```

### Option B: Python Script (Advanced)
```python
from src.models.train_bert import BertTrainer
from src.data.dataset import prepare_dataset
from src.data.preprocessing import DataPreprocessor
import pandas as pd

# 1. Prepare data
dataset_path = prepare_dataset()
df = pd.read_csv(dataset_path)

# 2. Preprocess
preprocessor = DataPreprocessor()
df_clean = preprocessor.clean(df)
train_df, val_df, test_df = preprocessor.split_data(df_clean)

# 3. Train
trainer = BertTrainer(model_name="distilbert-base-uncased")
# Create DataLoaders and train (see examples for full code)
```

## Making Predictions

### Via API
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Great doctor!"}'
```

### Via Python
```python
from src.models.predict import SentimentPredictor

predictor = SentimentPredictor(
    model_path="data/models/bert_sentiment_model.pt"
)

result = predictor.predict("Excelente médico, muito atencioso!")
print(result)
# {
#   "text": "Excelente médico, muito atencioso!",
#   "sentiment": "positive",
#   "confidence": 0.98,
#   "scores": {"positive": 0.98, "neutral": 0.015, "negative": 0.005}
# }
```

## Testing

```bash
# Run all tests
make test

# Run with coverage report
make test-cov

# Run specific test
pytest tests/test_api.py::test_health_check -v
```

## Code Quality

```bash
# Lint code
make lint

# Format code
make format

# Type checking
make typecheck

# Run all checks
make check
```

## Common Issues

### Issue: "No module named 'src'"
**Solution**: Make sure you're in the project root directory and virtual environment is activated

### Issue: "CUDA not available"
**Solution**: Set `device: cpu` in `.env` or code

### Issue: "Kaggle credentials not found"
**Solution**: Provide credentials in `.env` or use sample data (auto-created)

## Next Steps

1. **Read the docs**: Check `/docs` folder for architecture and deployment guides
2. **Explore notebooks**: Run notebooks in `/notebooks` for deeper analysis
3. **Run the pipeline**: Execute `dags/sentiment_training_flow.py` with Prefect
4. **Deploy to production**: Follow `docs/DEPLOYMENT.md`

## Documentation

- 📖 [README.md](README.md) - Project overview
- 🏗️ [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- 🚀 [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment
- 📊 [MONITORING.md](docs/MONITORING.md) - Observability
- 📡 [API_REFERENCE.md](docs/API_REFERENCE.md) - API docs

## Support

- 🐛 Report bugs: https://github.com/DenilsonPaco98/medical-review-sentiment-mlops/issues
- 💬 Discussions: https://github.com/DenilsonPaco98/medical-review-sentiment-mlops/discussions
- 📧 Email: denilson.paco98@gmail.com

---

**Happy coding! 🚀**
