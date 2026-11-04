# Medical Review Sentiment Analysis - MLOps

🏥 **Análise de Sentimento de Reviews Médicos** - Sistema MLOps de Classificação de Sentimentos usando Transformers (BERT) com otimização ONNX, Airflow, Docker Compose, Prometheus + Grafana e CI/CD completo.

**FIAP Tech Challenge - ML Engineering Especialization**

---

## 📊 O Projeto

Sistema end-to-end para classificação de sentimentos em avaliações médicas (Positivo, Neutro, Negativo):

- 🤖 **Modelo**: Fine-tuning BERT para classificação de texto
- ⚡ **Otimização**: Conversão ONNX para redução de latência
- 🔄 **Orquestração**: DAG Airflow para ingestão, treinamento e avaliação
- 📊 **Monitoramento**: Docker Compose com API FastAPI + Prometheus + Grafana
- 📈 **Tracking**: MLflow para experimentos e model registry
- ✅ **CI/CD**: GitHub Actions com testes automáticos
- 🐳 **Deployment**: Docker multi-stage otimizado
- 📊 **Dashboard**: Métricas em tempo real via Grafana

---

## 🛠️ Tech Stack

```
┌──────────────────────────────────────────────────────────┐
│ MODELAGEM & OTIMIZAÇÃO (20%)                             │
├──────────────────────────────────────────────────────────┤
│ • PyTorch + Transformers (HuggingFace BERT)              │
│ • ONNX Runtime (conversão & otimização)                  │
│ • Benchmark de latência (pré vs pós-ONNX)                │
│ • MLflow model tracking                                  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ ORQUESTRAÇÃO - AIRFLOW (15%)                             │
├──────────────────────────────────────────────────────────┤
│ • Apache Airflow 3.x                                      │
│ • DAG: data_preparation → model_training → evaluation     │
│ • Scheduling automático                                   │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ API & DEPLOYMENT (FastAPI)                               │
├──────────────────────────────────────────────────────────┤
│ • FastAPI (async REST endpoints)                         │
│ • Pydantic (request/response validation)                 │
│ • Docker multi-stage                                     │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ MONITORAMENTO (20%)                                      │
├──────────────────────────────────────────────────────────┤
│ • Prometheus (scraping de métricas)                      │
│ • Grafana (dashboards e alertas)                         │
│ • Docker Compose (stack completo)                        │
│ • Health checks e métricas de API                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ CI/CD - GITHUB ACTIONS (15%)                             │
├──────────────────────────────────────────────────────────┤
│ • Workflow de testes automáticos                         │
│ • Lint (ruff) + type-check (mypy)                        │
│ • Cobertura de testes (pytest + coverage)                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ DOCUMENTAÇÃO & VIDEO (30%)                               │
├──────────────────────────────────────────────────────────┤
│ • README com arquitetura                                 │
│ • Instructions de setup & execução                       │
│ • Video STAR ≤5 min demonstrando projeto                 │
└──────────────────────────────────────────────────────────┘
```

---

## 📋 Requisitos

- **Python 3.11** ou superior
- **uv** - gerenciador de pacotes ultra-rápido ([instalação](https://docs.astral.sh/uv/getting-started/installation/))
- **Docker + Docker Compose**
- **Git**
- **Makefile** (opcional, recomendado no WSL no Windows)

---

## ⚡ Quick Start

### 1. Setup Inicial

```bash
git clone https://github.com/DenilsonPaco98/medical-review-sentiment-mlops
cd medical-review-sentiment-mlops

uv venv && .venv\Scripts\activate
uv sync --extra dev --extra ml
```

### 2. Treinamento e Otimização

```bash
# Prepara dados do Kaggle
make prepare-data

# Treina modelo BERT
make train

# Converte para ONNX (redução de latência)
make export-onnx

# Compara latência: BERT vs ONNX
make benchmark-latency
```

### 3. Orquestração com Airflow

```bash
# Terminal 1: Webserver (UI)
airflow webserver -p 8080

# Terminal 2: Scheduler
airflow scheduler

# Acessa: http://localhost:8080
# DAG: sentiment_training_dag
```

### 4. Monitoramento (Docker Compose)

```bash
docker-compose up

# Serviços:
# - API FastAPI:    http://localhost:8000
# - Grafana:        http://localhost:3000 (admin/admin)
# - Prometheus:     http://localhost:9090
```

### 5. Testes & CI/CD

```bash
make test           # Pytest + coverage
make lint           # Ruff linting
make typecheck      # Mypy strict

# GitHub Actions roda automaticamente
```

---

## 📁 Estrutura do Projeto

```
medical-review-sentiment-mlops/
├── README.md                          # Este arquivo
├── LICENSE                            # MIT License
├── Makefile                           # Comandos úteis (make train, make test, etc)
├── pyproject.toml                     # Dependências e configuração do projeto
├── .env.example                       # Template de variáveis de ambiente
│
├── Dockerfile                         # Multi-stage: base -> builder -> runtime
├── docker-compose.yml                 # Stack: API + MLflow + Prometheus + Grafana
│
├── src/
│   ├── __init__.py
│   ├── py.typed                       # PEP 561 - Type hints
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                # Pydantic BaseSettings para env vars
│   │   └── logging.py                 # Configuração centralizada de logging
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── dataset.py                 # Download e preparação de dados (Kaggle API)
│   │   ├── preprocessing.py           # Cleaning, normalization, tokenization
│   │   ├── validation.py              # Great Expectations rules
│   │   └── duckdb_manager.py          # Interface com DuckDB
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── engineering.py             # Feature extraction (text embeddings, etc)
│   │   └── transformers_utils.py      # Tokenizers, preprocessors
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── architectures.py           # Arquitetura do modelo (BertForSequenceClassification)
│   │   ├── train_bert.py              # Pipeline de treinamento (fine-tuning)
│   │   ├── evaluate.py                # Métricas (precision, recall, f1, etc)
│   │   ├── predict.py                 # Inference (batch + single)
│   │   └── model_wrapper.py           # Wrapper para MLflow + reproducibilidade
│   │
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── drift_detector.py          # Evidently AI - data/model drift
│   │   ├── metrics.py                 # Prometheus metrics + custom metrics
│   │   └── logging_utils.py           # Structured logging (JSON)
│   │
│   ├── mlflow_utils/
│   │   ├── __init__.py
│   │   ├── tracking.py                # MLflow logging helpers
│   │   ├── registry.py                # Model registry operations
│   │   └── callbacks.py               # Callbacks para logging automático
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py                     # FastAPI application
│   │   ├── routes.py                  # Endpoints (/predict, /health, /metrics)
│   │   ├── schemas.py                 # Pydantic models (request/response)
│   │   ├── middleware.py              # Logging, error handling, CORS
│   │   └── inference_service.py       # Integração com TorchServe
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── dashboard.py               # Streamlit - EDA e exploração
│   │   ├── metrics_viewer.py          # Streamlit - visualização de métricas
│   │   └── components/                # Componentes reutilizáveis
│   │
│   ├── orchestration/
│   │   ├── __init__.py
│   │   ├── flows.py                   # Prefect flows (data prep -> train -> eval)
│   │   └── tasks.py                   # Prefect tasks
│   │
│   └── cli.py                         # CLI com Typer (uv run src.cli <command>)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Pytest fixtures
│   ├── test_data_preprocessing.py     # Tests para data pipeline
│   ├── test_models.py                 # Tests para modelos
│   ├── test_api.py                    # Tests para API endpoints
│   └── test_monitoring.py             # Tests para monitoring
│
├── notebooks/
│   ├── 01_eda_medical_reviews.ipynb   # Exploratory Data Analysis
│   ├── 02_sentiment_analysis.ipynb    # Sentiment classification
│   └── 03_model_comparison.ipynb      # Comparação de modelos
│
├── dags/
│   └── sentiment_training_flow.py     # Prefect flow (alternativa a Airflow DAG)
│
├── observability/
│   ├── prometheus.yml                 # Config Prometheus
│   └── grafana/
│       ├── dashboards/
│       │   └── sentiment-overview.json
│       └── provisioning/
│           ├── dashboards.yml
│           └── datasources/
│               └── prometheus.yml
│
├── docs/
│   ├── ARCHITECTURE.md                # Diagrama e decisões arquiteturais
│   ├── DATA_PIPELINE.md               # Documentação do pipeline de dados
│   ├── MODEL_TRAINING.md              # Guia de treinamento
│   ├── DEPLOYMENT.md                  # Instruções de deploy
│   ├── MONITORING.md                  # Guia de monitoramento
│   └── API_REFERENCE.md               # Documentação da API
│
├── data/
│   ├── raw/                           # Dados brutos (do Kaggle)
│   ├── processed/                     # Dados processados (DuckDB)
│   └── models/                        # Modelos treinados
│
├── mlruns/                            # MLflow artifacts (gitignored)
├── .dvc/                              # DVC config (opcional, para versionar dados)
│
├── .env.example                       # Template para variáveis de ambiente
├── .github/
│   └── workflows/
│       ├── tests.yml                  # Testes automáticos
│       ├── lint.yml                   # Linting (ruff, mypy)
│       └── deploy.yml                 # Deploy automático
│
├── Makefile                           # Comandos convenientes
└── pyproject.toml                     # Definição do projeto e dependências
```

---

## 🚀 Workflow

### Desenvolvimento Local

```bash
# 1. Prepare o ambiente
make install

# 2. Execute os testes
make test
make test-cov

# 3. Lint e type checking
make lint
make typecheck

# 4. Treinar um modelo (com MLflow tracking)
make train

# 5. Visualizar resultados
make mlflow-ui
streamlit run src/ui/dashboard.py

# 6. Deploy local com Docker
docker-compose up

# 7. Testar API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Great doctor, very professional!"}'
```

### Pipeline de Produção

```
Data Prep (Prefect) → Feature Engineering → Model Training → Evaluation
                                                ↓
                                        MLflow Registry
                                                ↓
                                        A/B Testing
                                                ↓
                                    Deployment (TorchServe)
                                                ↓
                                    Monitoring (Evidently)
```

---

## 📊 Recursos Principais

### 1. **MLflow Experiment Tracking**
```python
# Automático em cada treinamento
mlflow.start_run(run_name="bert-base-uncased-lr-2e5")
mlflow.log_params({"learning_rate": 2e-5, "epochs": 3})
mlflow.log_metrics({"val_loss": 0.25, "val_f1": 0.92})
mlflow.pytorch.log_model(model, "model")
# Visualizar: make mlflow-ui
```

### 2. **Streamlit Dashboard**
- 📊 EDA interativa
- 📈 Distribuição de sentimentos
- 🔍 Análise de exemplos incorretos
- 📉 Métricas em tempo real

### 3. **Prefect Orchestration**
```python
# Flows pythônicas, sem YAML complexo
@flow(name="sentiment-training")
def train_pipeline():
    data = prepare_data()
    model, metrics = train_model(data)
    evaluate_model(model)
```

### 4. **Great Expectations**
- Validação automática de dados
- Data drift detection
- Quality rules customizadas

### 5. **Evidently AI**
- Monitoramento de model/data drift
- Alerts automáticos
- Reports em HTML

---

## 📈 Performance Esperada

- **Accuracy**: 92-96% (3-class sentiment)
- **Inference latency**: <100ms (GPU), <500ms (CPU)
- **Training time**: ~15-30 min (single GPU)
- **Model size**: ~410MB (BERT base)

---

## 🔗 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/predict` | Predição de sentimento |
| `POST` | `/predict-batch` | Predição em lote |
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Métricas Prometheus |
| `GET` | `/docs` | Swagger UI |

### Exemplo de Requisição

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Excelente atendimento, médico muito atencioso!",
    "model_version": "production"
  }'
```

**Response:**
```json
{
  "text": "Excelente atendimento, médico muito atencioso!",
  "sentiment": "positive",
  "confidence": 0.98,
  "scores": {
    "positive": 0.98,
    "neutral": 0.015,
    "negative": 0.005
  },
  "inference_time_ms": 45
}
```

---

## 👨‍💻 Desenvolvimento

### Setup de IDE

```bash
# VSCode - copiar .vscode/settings.json
cp .vscode/settings.example.json .vscode/settings.json

# PyCharm - Auto-detect venv criado pelo uv
# File > Project Settings > Python Interpreter
```

### Pre-commit Hooks

```bash
pre-commit install
# Roda automaticamente antes de cada commit
```

### Type Hints (Strict Mode)

```bash
make typecheck  # mypy em strict mode
```

---

## 🧪 Testing

```bash
# Todos os testes
make test

# Com coverage report
make test-cov

# Teste específico
pytest tests/test_models.py::test_bert_training -v

# Watch mode
ptw
```

---

## 📚 Documentação

Ver pasta `/docs` para:
- 🏗️ [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Decisões de design
- 🔀 [DATA_PIPELINE.md](docs/DATA_PIPELINE.md) - Fluxo de dados
- 🤖 [MODEL_TRAINING.md](docs/MODEL_TRAINING.md) - Guia de treinamento
- 🚀 [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy em produção
- 📊 [MONITORING.md](docs/MONITORING.md) - Observabilidade
- 📡 [API_REFERENCE.md](docs/API_REFERENCE.md) - Referência da API

---

## 🤝 Contribuindo

```bash
# 1. Crie uma branch
git checkout -b feature/minha-feature

# 2. Faça as mudanças
# 3. Rode os testes e lint
make test && make lint

# 4. Commit com mensagens descritivas
git commit -m "feat: adiciona novo modelo"

# 5. Push e abra um PR
```

---

## 📄 Licença

MIT License - Ver [LICENSE](LICENSE)

---

## 📞 Contato & Suporte

- 🐛 Issues: https://github.com/DenilsonPaco98/medical-review-sentiment-mlops/issues
- 💬 Discussions: https://github.com/DenilsonPaco98/medical-review-sentiment-mlops/discussions
- 📧 Email: denilson.paco98@gmail.com

---

**Made with ❤️ by Denilson Paco | FIAP Machine Learning Engineering Specialist**
