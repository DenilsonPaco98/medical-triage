# Medical Review Sentiment Analysis — MLOps

Projeto acadêmico de classificação de sentimento em textos de avaliações médicas. O sistema estima as classes `negative`, `neutral` e `positive`; **não é um sistema de triagem clínica, diagnóstico ou recomendação médica**.

> O repositório contém componentes de treinamento, inferência e infraestrutura de observabilidade, mas ainda não demonstra validade clínica nem desempenho de modelo. Não use suas previsões para decisões sobre pacientes.

## Escopo implementado

- Classificador de sequência baseado em `distilbert-base-uncased`, PyTorch e Transformers.
- Preparação de CSV local e utilitário de download via Kaggle; se o download falhar, o código cria um pequeno conjunto sintético de demonstração. Esse fallback **não é dado de treinamento representativo**.
- API FastAPI com `/health`, `/predict`, `/predict-batch` e `/metrics`.
- Utilitários separados para avaliação de métricas, exportação/quantização ONNX e benchmark PyTorch/ONNX. A API atual serve PyTorch; não carrega o ONNX.
- Auxiliares de tracking de métricas/parâmetros via MLflow; não há registro/publicação de modelo no Model Registry.
- Compose com API, MLflow, PostgreSQL, Airflow, Prometheus e Grafana. O DAG Airflow atual prepara dados, mas as tarefas chamadas de treinamento/avaliação **não treinam nem avaliam o modelo**.
- GitHub Actions executa Ruff, Mypy, pytest e cobertura.

## O que não está implementado

Não há integração funcional com Streamlit, Prefect, TorchServe, DuckDB, Great Expectations, Evidently, A/B testing, alertas operacionais nem implantação em Kubernetes/cloud. Esses nomes aparecem em documentação histórica/configuração, mas não devem ser interpretados como capacidades entregues.

## Requisitos e instalação

- Python `>=3.11,<3.14` (a CI está configurada para Python 3.11).
- `uv`; Docker Desktop/Compose para executar a stack completa.
- Para Windows, comandos `make` podem exigir WSL ou uma instalação de GNU Make.

```bash
git clone https://github.com/DenilsonPaco98/medical-review-sentiment-mlops
cd medical-review-sentiment-mlops
uv sync --extra dev --extra ml --extra lint
```

Configure credenciais somente em ambiente local protegido, nunca em Git. `.env.example` contém placeholders; se uma credencial real já foi versionada ou compartilhada, revogue-a e gere outra.

## Dados e treinamento

O caminho de treinamento CLI implementado é `src.models.train_pipeline` (não `src.models.train_bert`). Exige um CSV com coluna `text` e uma coluna de rótulo chamada `sentiment`, `label_name` ou `label`. Rótulos aceitos: `negative`, `neutral`, `positive` ou IDs `0`, `1`, `2` nessa ordem.

```bash
# Baixa/prepara dados (requer acesso/configuração Kaggle; pode produzir fallback sintético)
uv run python -c "from src.data.dataset import prepare_dataset; print(prepare_dataset())"

# Treina usando o CSV padrão data/raw/medical_reviews.csv
uv run python -m src.models.train_pipeline --data data/raw/medical_reviews.csv --output-dir data/models
```

O treinamento separa treino/validação estratificados (80/20), tokeniza até 128 tokens por padrão, executa duas épocas e salva `data/models/bert_sentiment_model.pt`. Os parâmetros podem ser ajustados com `--epochs`, `--batch-size`, `--max-length`, `--device` e `--model-name`. É necessário ter acesso ao modelo/tokenizer Hugging Face na primeira execução. O treinamento registra perdas e acurácia de validação no MLflow quando a configuração de tracking está disponível.

O módulo `src.models.evaluate` fornece funções de cálculo de métricas para rótulos reais e predições; não existe atualmente um comando de avaliação de ponta a ponta que carregue um conjunto de teste e produza um relatório reproduzível. O treinamento não persiste um manifesto de dados, divisão, versões ou métricas de teste.

## API local

```bash
uv run uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Exemplo de requisição:

```json
{"text": "Atendimento atencioso e profissional."}
```

`/predict` devolve texto, classe, confiança, escores das três classes e tempo de inferência. O campo opcional `model_version` ainda não é utilizado para selecionar um modelo. `/predict-batch` recebe `{"texts": ["texto 1", "texto 2"]}` e retorna uma lista; a implementação executa cada texto individualmente.

**Importante:** se o checkpoint não existir, a inferência instancia um classificador com cabeça de classificação recém-inicializada e ainda pode retornar resultados. Um `/health` com status `healthy` confirma apenas a resposta da aplicação, não que os pesos foram carregados ou que o modelo é válido. Forneça e valide explicitamente um checkpoint treinado antes de interpretar previsões.

## ONNX e benchmark

O exportador aceita o checkpoint PyTorch em `data/models/bert_sentiment_model.pt`; o benchmark mede localmente a inferência de PyTorch e ONNX. São ferramentas independentes da API, e nenhum resultado de latência ou redução de tamanho é garantido pelo código. Faça medições no hardware, dados e configuração alvo antes de divulgar números.

## Docker Compose e observabilidade

```bash
docker compose up --build
```

Endereços publicados: API `:8000`, MLflow `:5000`, Airflow `:4200`, Prometheus `:9090`, Grafana `:3000` e PostgreSQL `:5432`. Consulte a configuração do Compose antes do uso: há senhas de desenvolvimento e imagens com tags flutuantes. Troque as credenciais, restrinja exposição de portas e fixe versões antes de qualquer ambiente compartilhado.

Prometheus coleta `/metrics` da API. O dashboard provisionado do Grafana exibe disponibilidade, volume de requisições/predições e distribuições de latência HTTP/inferência. Métricas técnicas não medem acurácia, deriva de dados nem segurança clínica. A stack é uma configuração local de desenvolvimento, não uma implantação endurecida para produção.

## Comandos de qualidade

```bash
uv run ruff check src tests
uv run mypy src
uv run pytest tests -v --cov=src --cov-report=term-missing
```

Os testes existentes focam limpeza básica de dados e contratos HTTP com predições simuladas; o teste de modelo real está marcado como ignorado por depender dos pesos. Portanto, testes verdes não constituem validação da qualidade preditiva.

## Estrutura real (resumo)

```text
src/api/                 API, schemas, rotas e métricas Prometheus
src/config/              configurações via Pydantic Settings
src/data/                download/preparação e limpeza de CSV
src/models/              treinamento, predição, avaliação e ONNX
src/mlflow_utils/        helper de tracking
dags/                    DAG Airflow (esqueleto; sem treino real)
observability/            configuração Prometheus e provisioning/dashboard Grafana
tests/                   testes de API, preprocessing e modelos
docs/                    documentação de arquitetura e auditoria técnica
notebooks/               notebook de EDA
```

Dados, pesos e artefatos locais são ignorados pelo Git. Um clone limpo precisa recebê-los/gerá-los explicitamente; sua presença no computador do autor não garante sua disponibilidade em outro ambiente.

## Limitações e próximos passos científicos

Antes de qualquer alegação de desempenho, construir avaliação reproduzível com conjunto de teste independente e versionado, baseline, matriz de confusão, métricas por classe, intervalos de confiança, análise de desbalanceamento e revisão de vazamento/duplicatas. Também são prioritários: falhar de forma explícita quando não houver checkpoint; separar readiness de liveness; implementar avaliação e treino no DAG; adicionar limites ao batch e execução fora do event loop; persistir versões/configurações; remover credenciais/defaults inseguros; e validar o domínio/idioma dos dados. Nenhuma acurácia, latência ou adequação clínica é afirmada neste README.

## Licença

MIT — consulte [LICENSE](LICENSE).