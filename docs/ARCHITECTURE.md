# Arquitetura implementada

## Objetivo e limites de uso

Aplicação acadêmica que classifica textos de avaliações médicas como `negative`, `neutral` ou `positive`. A saída é uma estimativa de sentimento geral; o sistema não executa triagem clínica, diagnóstico ou aconselhamento e não foi validado para uso em saúde.

## Componentes observados no código

```text
CSV/Kaggle ──> limpeza ──> train/validation split ──> tokenizer Transformers
                                                          │
                                                          v
                                                   PyTorch DistilBERT
                                                          │
                                                  checkpoint state_dict
                                                          │
Cliente ──HTTP──> FastAPI ──> predictor PyTorch ──> resposta JSON
                    │
                    └── /metrics ──> Prometheus ──> Grafana provisionado

Treinamento ──métricas──> MLflow tracking server
Compose também inicia PostgreSQL e Airflow.
```

### Dados e pré-processamento

`src.data.dataset` tenta obter o CSV via Kaggle e grava `data/raw/medical_reviews.csv`; diante de qualquer exceção, gera um conjunto sintético de dez linhas para demonstração. Esse comportamento deve ser tratado com cautela: o sucesso da tarefa não prova que dados reais foram obtidos. `src.data.preprocessing` remove nulos/duplicatas, filtra classes não reconhecidas e oferece divisão estratificada.

### Treinamento e avaliação

`src.models.train_pipeline` é o ponto CLI implementado. Lê CSV, filtra linhas vazias, aceita rótulos textuais ou IDs, cria divisão estratificada treino/validação e chama `BertTrainer` de `src.models.train_bert`. O modelo padrão é `distilbert-base-uncased` com três classes. O pipeline grava checkpoint state_dict e loga loss e acurácia de validação no MLflow. Não há avaliação integrada em conjunto de teste independente nem artefato de resultados científicos reproduzíveis. `src.models.evaluate` contém auxiliares para métricas, não um pipeline de avaliação.

### Inferência

`src.models.predict.SentimentPredictor` tokeniza e executa inferência PyTorch; o lote itera item a item. Se pesos não forem fornecidos/encontrados, a cabeça de classificação recém-inicializada ainda produz escores. A API não seleciona um modelo por `model_version`. O health endpoint não verifica disponibilidade/carregamento do modelo.

### API e observabilidade

FastAPI declara `/health`, `/predict`, `/predict-batch` e `/metrics`. Pydantic limita texto individual a 2.000 caracteres; o endpoint em lote exige pelo menos um item, sem limite máximo explícito de itens. Middleware Prometheus agrega contagem/status/latência HTTP e a rota de predição registra duração e classe. Prometheus raspa `/metrics`; Grafana provisiona datasource e dashboard. Esses sinais observam serviço e utilização, não qualidade/deriva do modelo.

### ONNX e MLflow

`src.models.onnx_converter` exporta e quantiza ONNX; `src.models.benchmark` fornece benchmark separado. A rota de inferência continua em PyTorch. MLflow recebe parâmetros e métricas, mas não há chamada de registro no Model Registry nem carregamento de modelo registrado no serving.

### Orquestração e containers

Existe uma DAG Airflow com preparação, tarefa nominal de treino e tarefa nominal de avaliação. A tarefa de treino atual calcula contagens de split e retorna estado, sem invocar `BertTrainer`; avaliação apenas registra esse retorno. Compose descreve API, servidor MLflow, PostgreSQL, Airflow, Prometheus e Grafana. A configuração presente é voltada a desenvolvimento; revisar executor/metadata DB do Airflow, segredos, tags de imagem e dependências da imagem antes de depender da stack.

## Qualidade, reprodutibilidade e segurança

- Python suportado no projeto: `>=3.11,<3.14`.
- CI de GitHub Actions configura Python 3.11 e executa Ruff, Mypy, pytest e cobertura.
- Artefatos de dados/modelos são ignorados pelo Git; registrar fonte, hash, versão, divisão e proveniência fora do repositório, de forma segura.
- Não inserir credenciais em `.env.example`, imagens, notebooks ou logs. Rotacionar qualquer segredo que tenha sido exposto.
- `torch.load` deve receber apenas checkpoints confiáveis; erros da API não devem revelar detalhes internos em respostas externas.
- Textos sobre saúde podem conter dados sensíveis; minimizar coleta, retenção e exposição em logs/telemetria.

## Lacunas prioritárias

1. Bloquear inferência se não existir checkpoint aprovado e implementar readiness real.
2. Construir avaliação científica independente: baseline, split imutável, métricas por classe, macro-F1, matriz de confusão, calibração, intervalos de confiança e análise de erro.
3. Garantir proveniência do dataset, idioma, licenças, consentimento e tratamento de dados sensíveis; não confundir dados sintéticos com reais.
4. Conectar o DAG ao treinamento e avaliação reais, corrigir configuração Airflow e tornar operações reexecutáveis/idempotentes.
5. Limitar tamanho de lote/tamanho agregado, executar inferência síncrona fora do event loop e tratar timeouts/erros sem devolver exceções internas.
6. Definir pinagem de dependências/imagens, segredos externos, controles de acesso, TLS e política operacional antes de qualquer ambiente público.
7. Só publicar benchmarks após execução controlada com hardware, warm-up, concorrência, tamanho do texto e percentis documentados.

## Componentes explicitamente ausentes

Não foram encontrados fluxos funcionais de Streamlit, Prefect, TorchServe, DuckDB, Great Expectations, Evidently, A/B testing, model registry, alertas, Kubernetes ou implantação em cloud. Menções antigas a essas ferramentas não representam implementação.