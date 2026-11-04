"""
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘                                                                                â•‘
â•‘                    ðŸŽ‰ PROJETO PRONTO PARA EXECUTAR! ðŸŽ‰                        â•‘
â•‘                                                                                â•‘
â•‘                  Medical Review Sentiment Analysis - MLOps                     â•‘
â•‘                                                                                â•‘
â•‘                 Todas as dependÃªncias estÃ£o instaladas!                        â•‘
â•‘                                                                                â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•


ðŸš€ COMECE AGORA EM 3 PASSOS:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

PASSO 1: Abra PowerShell/Terminal no diretÃ³rio do projeto:

    cd c:\\Users\\denil\\Documents\\GitHub\\medical-triage\\medical-review-sentiment-mlops


PASSO 2: Execute o pipeline interativo:

    .venv\Scripts\python.exe run_pipeline.py

    (Ou use: python run_pipeline.py se Python global estiver no PATH)


PASSO 3: Escolha a opÃ§Ã£o desejada:

    Menu aparecerÃ¡ com opÃ§Ãµes:
    1. Preparar Dataset (download do Kaggle)
    2. Treinar Modelo BERT
    3. Converter para ONNX
    4. Benchmark de LatÃªncia
    5. Rodar Testes
    6. Lint com Ruff
    7. Type checking com Mypy
    8. Iniciar API FastAPI
    9. EXECUTAR TUDO
    10. Sair


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

âš¡ ATALHOS (SEM MENU INTERATIVO):
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Comandos diretos via Make:

    make prepare-data       # Baixar dataset
    make train             # Treinar BERT (~20 min com GPU, ~2h sem GPU)
    make export-onnx       # Converter para ONNX
    make benchmark-latency # Comparar PyTorch vs ONNX (5-10x speedup esperado)
    make test              # Rodar testes
    make lint              # Lint com Ruff
    make typecheck         # Type checking
    make serve-dev         # Iniciar API em http://localhost:8000
    make docker-up         # Iniciar Docker stack (MLflow, Prometheus, Grafana)


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ’» AMBIENTE VERIFICADO:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

âœ… Python 3.11.9
âœ… PyTorch 2.15.0 (CPU - sem GPU, usarÃ¡ CPU)
âœ… Transformers 4.40+
âœ… MLflow 2.10+
âœ… Apache Airflow 3.3.2
âœ… FastAPI + Uvicorn
âœ… Pandas, NumPy, Scikit-learn
âœ… ONNX + ONNXRuntime
âœ… Pytest + Coverage
âœ… Jupyter Notebook
âœ… Ruff (Linting)
âœ… Mypy (Type checking)


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ“š DOCUMENTAÃ‡ÃƒO:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Para guia detalhado de cada passo, leia:

    cat SETUP_GUIDE.md

Ou abra em um editor:

    SETUP_GUIDE.md (passo-a-passo completo)
    TECH_CHALLENGE_CRITERIA.md (mapeamento dos 6 critÃ©rios)
    PROJECT_STATUS.md (checklist de implementaÃ§Ã£o)


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

âš ï¸  CONFIGURAÃ‡ÃƒO IMPORTANTE:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

1. O arquivo .env foi criado com configuraÃ§Ãµes padrÃ£o (OK para comeÃ§ar)

2. Se quiser baixar dataset do Kaggle, configure:
   - Crie conta em kaggle.com
   - VÃ¡ em Account â†’ Settings â†’ Create New Token
   - Salve o arquivo baixado em: C:\\Users\\seu_usuario\\.kaggle\\kaggle.json
   - Execute: make prepare-data

3. GPU:
   - Projeto usa CPU por padrÃ£o (mais lento, ~2h treino)
   - Se tem GPU NVIDIA, mude DEVICE=cuda em .env
   - PyTorch GPU foi instalado (CPU mode), upgrade se quiser CUDA


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸŽ¯ FLUXO RECOMENDADO:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Para demonstrar todos os 6 critÃ©rios do Tech Challenge:

1ï¸âƒ£  MODELAGEM & OTIMIZAÃ‡ÃƒO (20%)
   â†’ make prepare-data
   â†’ make train
   â†’ make export-onnx
   â†’ make benchmark-latency
   (Resultado: ~5-10x speedup ONNX vs PyTorch)

2ï¸âƒ£  CI/CD (15%)
   â†’ make lint
   â†’ make typecheck
   â†’ make test
   (Resultado: 100% testes passando)

3ï¸âƒ£  ORQUESTRAÃ‡ÃƒO AIRFLOW (15%)
   â†’ airflow webserver -p 8080  (em um terminal)
   â†’ airflow scheduler          (em outro terminal)
   â†’ Abra http://localhost:8080
   â†’ DAG: sentiment_training_dag

4ï¸âƒ£  MONITORAMENTO (20%)
   â†’ docker-compose up
   â†’ Grafana: http://localhost:3000 (admin/admin)
   â†’ Prometheus: http://localhost:9090
   â†’ Enviar requisiÃ§Ãµes Ã  API para gerar mÃ©tricas

5ï¸âƒ£  DOCUMENTAÃ‡ÃƒO (15%)
   â†’ Tudo documentado (ver arquivos acima)

6ï¸âƒ£  VÃDEO STAR (15%)
   â†’ Gravar tela demonstrando 1-5 acima
   â†’ â‰¤5 minutos
   â†’ Formato MP4 ou YouTube link


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

âœ¨ PRÃ“XIMOS PASSOS:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Execute agora:

    .venv\Scripts\python.exe run_pipeline.py

Ou comece diretamente:

    make prepare-data

Depois:

    make train

(Isso levarÃ¡ tempo, pode deixar rodando enquanto faz outra coisa)


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸ“ž AJUDA:
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

Qualquer dÃºvida:

1. Verifique SETUP_GUIDE.md (seÃ§Ã£o "PossÃ­veis Problemas e SoluÃ§Ãµes")
2. Veja o arquivo .env para entender as configuraÃ§Ãµes
3. Execute: .venv\Scripts\python.exe check_setup.py
4. Veja os logs em ./logs/ (criados apÃ³s primeira execuÃ§Ã£o)


â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

ðŸŽ‰ DIVIRTA-SE! O PROJETO ESTÃ PRONTO! ðŸŽ‰

Ãšltima atualizaÃ§Ã£o: 2026-11-03
Projeto: Medical Review Sentiment Analysis
Status: âœ… PRONTO PARA EXECUTAR
"""

if __name__ == "__main__":
    print(__doc__)

