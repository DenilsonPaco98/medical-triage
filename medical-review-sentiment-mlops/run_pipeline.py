#!/usr/bin/env python
"""
Script para iniciar o pipeline completo do projeto.
Permite escolher qual etapa executar.
"""

import subprocess
import sys
from pathlib import Path
from typing import List

# Cores para terminal
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

LOGO = f"""{BLUE}
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘                                                                        â•‘
â•‘          Medical Review Sentiment Analysis - MLOps Pipeline           â•‘
â•‘                                                                        â•‘
â•‘                   Interactive Setup & Execution Tool                  â•‘
â•‘                                                                        â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
{RESET}
"""

class PipelineRunner:
    def __init__(self):
        self.venv_python = ".venv\\Scripts\\python.exe"
        self.project_root = Path(".")
        
    def check_environment(self) -> bool:
        """Verificar se o ambiente estÃ¡ configurado."""
        print(f"\n{BLUE}ðŸ” Verificando ambiente...{RESET}\n")
        
        try:
            result = subprocess.run(
                [self.venv_python, "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"âœ… Python: {result.stdout.strip()}")
            
            # Verificar pacotes principais
            packages = {
                "torch": "PyTorch",
                "transformers": "Transformers",
                "mlflow": "MLflow",
                "fastapi": "FastAPI",
                "pandas": "Pandas",
                "airflow": "Airflow",
            }
            
            for package, name in packages.items():
                try:
                    subprocess.run(
                        [self.venv_python, "-c", f"import {package}"],
                        capture_output=True,
                        check=True
                    )
                    print(f"âœ… {name}")
                except subprocess.CalledProcessError:
                    print(f"âŒ {name} (NÃƒO INSTALADO)")
                    return False
            
            print(f"\n{GREEN}âœ… Ambiente configurado corretamente!{RESET}\n")
            return True
            
        except Exception as e:
            print(f"{RED}âŒ Erro ao verificar ambiente: {e}{RESET}\n")
            return False
    
    def run_command(self, cmd: List[str], description: str) -> bool:
        """Executar um comando e retornar sucesso/fracasso."""
        print(f"\n{BLUE}â³ {description}...{RESET}\n")
        
        try:
            subprocess.run(cmd, check=True)
            print(f"\n{GREEN}âœ… {description} - SUCESSO!{RESET}\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n{RED}âŒ {description} - FALHOU!{RESET}\n")
            print(f"Erro: {e}\n")
            return False
        except Exception as e:
            print(f"\n{RED}âŒ Erro inesperado: {e}{RESET}\n")
            return False
    
    def prepare_data(self) -> bool:
        """Preparar dataset."""
        return self.run_command(
            [self.venv_python, "-m", "src.data.dataset", "prepare"],
            "Preparando dataset do Kaggle"
        )
    
    def train_model(self) -> bool:
        """Treinar modelo BERT."""
        return self.run_command(
            [self.venv_python, "-m", "src.models.train_bert"],
            "Treinando modelo BERT"
        )
    
    def export_onnx(self) -> bool:
        """Converter para ONNX."""
        cmd = f"""
import sys
from src.models.onnx_converter import ONNXConverter
try:
    converter = ONNXConverter('data/models/bert_sentiment_model.pt')
    converter.convert()
    converter.validate()
    print("ONNX conversion successful!")
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
"""
        return self.run_command(
            [self.venv_python, "-c", cmd.strip()],
            "Convertendo modelo para ONNX"
        )
    
    def benchmark_latency(self) -> bool:
        """Benchmark de latÃªncia."""
        cmd = f"""
from src.models.benchmark import LatencyBenchmark
try:
    benchmark = LatencyBenchmark()
    results = benchmark.compare(
        'data/models/bert_sentiment_model.pt',
        'data/models/sentiment_model.onnx'
    )
    print(results)
except Exception as e:
    print(f"Error: {{e}}")
"""
        return self.run_command(
            [self.venv_python, "-c", cmd.strip()],
            "Benchmark de latÃªncia (PyTorch vs ONNX)"
        )
    
    def run_tests(self) -> bool:
        """Rodar testes."""
        return self.run_command(
            [self.venv_python, "-m", "pytest", "tests", "-v"],
            "Rodando testes unitÃ¡rios"
        )
    
    def lint_code(self) -> bool:
        """Lint com Ruff."""
        return self.run_command(
            [self.venv_python, "-m", "ruff", "check", "src"],
            "Lint com Ruff"
        )
    
    def typecheck(self) -> bool:
        """Type checking com Mypy."""
        return self.run_command(
            [self.venv_python, "-m", "mypy", "src"],
            "Type checking com Mypy"
        )
    
    def start_api(self) -> bool:
        """Iniciar API FastAPI."""
        print(f"\n{BLUE}â³ Iniciando API FastAPI...{RESET}\n")
        try:
            subprocess.Popen(
                [self.venv_python, "-m", "uvicorn", "src.api.app:app", "--reload"]
            )
            print(f"{GREEN}âœ… API iniciada em http://localhost:8000{RESET}\n")
            print(f"   DocumentaÃ§Ã£o: http://localhost:8000/docs\n")
            return True
        except Exception as e:
            print(f"{RED}âŒ Erro ao iniciar API: {e}{RESET}\n")
            return False
    
    def show_menu(self):
        """Mostrar menu interativo."""
        print(f"{YELLOW}Escolha uma opÃ§Ã£o:{RESET}\n")
        print("  1. Preparar Dataset (make prepare-data)")
        print("  2. Treinar Modelo BERT (make train)")
        print("  3. Converter para ONNX (make export-onnx)")
        print("  4. Benchmark de LatÃªncia (make benchmark-latency)")
        print("  5. Rodar Testes (make test)")
        print("  6. Lint com Ruff (make lint)")
        print("  7. Type checking com Mypy (make typecheck)")
        print("  8. Iniciar API FastAPI (make serve-dev)")
        print("  9. EXECUTAR TUDO (1-8 em sequÃªncia)")
        print(" 10. Sair\n")
    
    def run(self):
        """Executar menu interativo."""
        print(LOGO)
        
        # Verificar ambiente
        if not self.check_environment():
            print(f"{RED}Instale as dependÃªncias faltantes e tente novamente.{RESET}\n")
            sys.exit(1)
        
        while True:
            self.show_menu()
            choice = input(f"{BLUE}OpÃ§Ã£o (1-10): {RESET}").strip()
            
            if choice == "1":
                self.prepare_data()
            elif choice == "2":
                self.train_model()
            elif choice == "3":
                self.export_onnx()
            elif choice == "4":
                self.benchmark_latency()
            elif choice == "5":
                self.run_tests()
            elif choice == "6":
                self.lint_code()
            elif choice == "7":
                self.typecheck()
            elif choice == "8":
                self.start_api()
            elif choice == "9":
                # Executar tudo
                print(f"\n{YELLOW}Executando pipeline completo...{RESET}\n")
                self.prepare_data()
                self.train_model()
                self.export_onnx()
                self.benchmark_latency()
                self.lint_code()
                self.typecheck()
                self.run_tests()
                print(f"\n{GREEN}âœ… Pipeline completo executado!{RESET}\n")
            elif choice == "10":
                print(f"\n{GREEN}AtÃ© logo!{RESET}\n")
                break
            else:
                print(f"{RED}OpÃ§Ã£o invÃ¡lida. Tente novamente.{RESET}\n")


if __name__ == "__main__":
    runner = PipelineRunner()
    runner.run()

