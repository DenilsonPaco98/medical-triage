#!/usr/bin/env python
"""Script para verificar o setup do projeto."""

import sys
import subprocess

required_packages = [
    "torch",
    "transformers", 
    "mlflow",
    "fastapi",
    "pandas",
    "numpy",
    "sklearn",
    "onnx",
    "onnxruntime",
    "pytest",
    "jupyter",
    "airflow",
]

print("ðŸ” Verificando pacotes instalados...\n")

missing = []
installed = []

for package in required_packages:
    try:
        __import__(package if package != "sklearn" else "sklearn")
        installed.append(package)
        print(f"âœ… {package}")
    except ImportError:
        missing.append(package)
        print(f"âŒ {package} (NÃƒO INSTALADO)")

print(f"\nðŸ“Š Status: {len(installed)}/{len(required_packages)} pacotes instalados")

if missing:
    print(f"\nâš ï¸  Pacotes faltando: {', '.join(missing)}")
    print("\nPara instalar, execute:")
    print(f"  .venv\\Scripts\\python -m pip install {' '.join(missing)}")
else:
    print("\nâœ… Todos os pacotes necessÃ¡rios estÃ£o instalados!")

# Verificar Python version
print(f"\nðŸ Python version: {sys.version}")
print(f"   Executable: {sys.executable}")

