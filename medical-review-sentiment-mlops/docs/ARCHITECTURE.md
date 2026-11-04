"""Project documentation - Architecture Overview."""

# Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  • FastAPI REST API (async)                                     │
│  • Streamlit Dashboard (interactive)                            │
│  • CLI Tools (batch processing)                                 │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  • Sentiment Prediction (BERT-based)                            │
│  • Model Inference (TorchServe)                                 │
│  • Request Validation (Pydantic)                                │
│  • Caching Layer                                                │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                       MODEL LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│  • Fine-tuned BERT (3-class: positive/neutral/negative)         │
│  • Model versioning (MLflow Registry)                           │
│  • Model serving (TorchServe)                                   │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
├─────────────────────────────────────────────────────────────────┤
│  • DuckDB (OLAP queries)                                        │
│  • Data validation (Great Expectations)                         │
│  • Data drift detection (Evidently AI)                          │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  • Prefect Flows (data prep → train → deploy)                  │
│  • Task scheduling & monitoring                                │
│  • Error handling & retries                                    │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                   MONITORING LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  • MLflow Experiment Tracking                                   │
│  • Prometheus Metrics                                           │
│  • Grafana Dashboards                                           │
│  • Structured Logging (JSON)                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Key Architectural Decisions

### 1. **Model: Transformers (BERT) over TF-IDF**
- **Why**: BERT captures semantic meaning, not just term frequency
- **Benefit**: Better accuracy (~95%) vs TF-IDF (~85%)
- **Trade-off**: Higher latency (100ms vs 5ms), but acceptable for production

### 2. **Orchestration: Prefect over Airflow**
- **Why**: Python-native DAGs, less boilerplate
- **Benefit**: Easier to understand, debug, and extend
- **Features**: Built-in retries, error handling, logging

### 3. **Database: DuckDB over PostgreSQL/CSV**
- **Why**: OLAP (analytical queries), not OLTP (transactional)
- **Benefit**: 10x faster analytics, lower storage
- **Use case**: Time-series analysis, ML dataset queries

### 4. **Experiment Tracking: MLflow**
- **Why**: Industry standard, comprehensive
- **Features**: Experiment tracking, model registry, artifact storage
- **Integration**: Works with any ML framework

### 5. **Dashboard: Streamlit over Grafana**
- **Why**: User-friendly, code-based, no UI builder needed
- **Benefit**: Faster development, version control
- **Use case**: Interactive data exploration, model evaluation

## Data Flow

```
Kaggle API
    ↓
[data/raw/medical_reviews.csv]
    ↓
Data Cleaning (Preprocessing)
    ↓
Data Validation (Great Expectations)
    ↓
[DuckDB - data/processed/medical_reviews.duckdb]
    ↓
Feature Engineering (Tokenization)
    ↓
BERT Fine-tuning (Training)
    ↓
[MLflow - Model Registry]
    ↓
Model Serving (FastAPI + TorchServe)
    ↓
[API Response - Sentiment + Confidence]
    ↓
Monitoring (Prometheus + Grafana)
```

## Model Training Pipeline

```
Load Dataset
    ↓
Data Cleaning & Splitting
    ↓
Tokenization (HuggingFace Tokenizer)
    ↓
PyTorch DataLoaders
    ↓
BERT Fine-tuning
    ├─ Learning Rate: 2e-5
    ├─ Epochs: 3
    ├─ Batch Size: 32
    └─ Optimizer: AdamW
    ↓
Evaluation Metrics
    ├─ Accuracy
    ├─ Precision
    ├─ Recall
    └─ F1 Score
    ↓
MLflow Logging
    ├─ Parameters
    ├─ Metrics
    ├─ Model Artifacts
    └─ Tags
    ↓
[Model Ready for Serving]
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────┐
│         Docker (Multi-stage Build)               │
│  Base → Builder → Runtime → Development          │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│      Docker Compose (Local Development)          │
│  ├─ API (FastAPI)                                │
│  ├─ Streamlit (Dashboard)                        │
│  ├─ MLflow (Tracking)                            │
│  ├─ PostgreSQL (Backend)                         │
│  ├─ Prefect (Orchestration)                      │
│  ├─ Prometheus (Metrics)                         │
│  ├─ Grafana (Dashboards)                         │
│  └─ Adminer (DB UI)                              │
└──────────────────────────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│   Production (Kubernetes/Cloud)                   │
│  ├─ API Deployment (FastAPI)                     │
│  ├─ Model Serving (TorchServe)                   │
│  ├─ Data Store (Cloud DuckDB)                    │
│  ├─ Orchestration (Prefect Cloud)                │
│  └─ Monitoring (Datadog/New Relic)               │
└──────────────────────────────────────────────────┘
```

## Technology Stack Justification

| Layer | Technology | Why Not | Tradeoff |
|-------|-----------|--------|----------|
| **Model Training** | PyTorch + Transformers | TensorFlow | PyTorch has better community for NLP |
| **Experiment Tracking** | MLflow | Wandb | Open-source, no vendor lock-in |
| **Orchestration** | Prefect | Airflow | Simpler Python API |
| **Database** | DuckDB | PostgreSQL | OLAP is faster for analytics |
| **Dashboard** | Streamlit | Dash/Tableau | Code-based, easier versioning |
| **Deployment** | Docker | K8s | Simpler for small projects |
| **API** | FastAPI | Flask | Async, automatic docs (OpenAPI) |

## Performance Targets

- **Inference Latency**: < 100ms (p95)
- **Model Accuracy**: > 92% (3-class)
- **Throughput**: > 1000 req/sec
- **Data Pipeline Duration**: < 30 min

## Security Considerations

- ✅ Non-root Docker user
- ✅ Healthchecks for all services
- ✅ CORS configured
- ✅ Input validation (Pydantic)
- ✅ Secrets in .env (not committed)
- ⚠️ TODO: Rate limiting
- ⚠️ TODO: Authentication/Authorization
- ⚠️ TODO: TLS/HTTPS

## Scalability

- **Horizontal**: Multiple API instances behind load balancer
- **Vertical**: GPU support, batch inference
- **Caching**: Redis for hot predictions
- **Async**: FastAPI async handlers, Prefect tasks
