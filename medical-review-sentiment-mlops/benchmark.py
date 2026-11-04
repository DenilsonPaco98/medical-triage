#!/usr/bin/env python
"""Script para benchmark de latÃªncia PyTorch vs ONNX."""

import os
import time
import torch
import numpy as np
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import onnxruntime as rt

print("=" * 70)
print("âš¡ BENCHMARK DE LATÃŠNCIA")
print("=" * 70)

model_path = "data/models/bert_sentiment_model.pt"
onnx_path = "data/models/sentiment_model.onnx"

# Verificar se arquivos existem
if not os.path.exists(model_path):
    print(f"âŒ Modelo PyTorch nÃ£o encontrado: {model_path}")
    exit(1)

if not os.path.exists(onnx_path):
    print(f"âŒ Modelo ONNX nÃ£o encontrado: {onnx_path}")
    exit(1)

print(f"\nâœ… Modelos encontrados")

# ===== PYTORCH BENCHMARK =====
print("\n" + "=" * 70)
print("ðŸ PYTORCH BENCHMARK")
print("=" * 70)

model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=3)
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

# Texto de teste
test_text = "Excelente mÃ©dico! Muito atencioso e profissional. Recomendo!"

# Warm-up
print("\nWarm-up PyTorch...")
with torch.no_grad():
    inputs = tokenizer(
        test_text,
        return_tensors="pt",
        max_length=256,
        padding=True,
        truncation=True,
    )
    model(**inputs)

# Benchmark
print("Medindo latÃªncia PyTorch...")
num_iterations = 10
pytorch_times = []

with torch.no_grad():
    for i in range(num_iterations):
        inputs = tokenizer(
            test_text,
            return_tensors="pt",
            max_length=256,
            padding=True,
            truncation=True,
        )
        
        start = time.time()
        model(**inputs)
        end = time.time()
        
        pytorch_times.append((end - start) * 1000)  # ms
        print(f"  IteraÃ§Ã£o {i+1}/{num_iterations}: {pytorch_times[-1]:.2f}ms")

pytorch_mean = np.mean(pytorch_times)
pytorch_std = np.std(pytorch_times)
pytorch_min = np.min(pytorch_times)
pytorch_max = np.max(pytorch_times)

print(f"\nðŸ“Š PyTorch Results:")
print(f"   Mean:  {pytorch_mean:.2f}ms")
print(f"   Std:   {pytorch_std:.2f}ms")
print(f"   Min:   {pytorch_min:.2f}ms")
print(f"   Max:   {pytorch_max:.2f}ms")

# ===== ONNX BENCHMARK =====
print("\n" + "=" * 70)
print("ðŸš€ ONNX BENCHMARK")
print("=" * 70)

# Preparar inputs
inputs = tokenizer(
    test_text,
    return_tensors="pt",
    max_length=256,
    padding=True,
    truncation=True,
)

# Carregar ONNX
print("\nCarregando modelo ONNX...")
sess = rt.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])

# Warm-up
print("Warm-up ONNX...")
sess.run(
    None,
    {
        "input_ids": inputs["input_ids"].numpy(),
        "attention_mask": inputs["attention_mask"].numpy(),
    }
)

# Benchmark
print("Medindo latÃªncia ONNX...")
onnx_times = []

for i in range(num_iterations):
    start = time.time()
    sess.run(
        None,
        {
            "input_ids": inputs["input_ids"].numpy(),
            "attention_mask": inputs["attention_mask"].numpy(),
        }
    )
    end = time.time()
    
    onnx_times.append((end - start) * 1000)  # ms
    print(f"  IteraÃ§Ã£o {i+1}/{num_iterations}: {onnx_times[-1]:.2f}ms")

onnx_mean = np.mean(onnx_times)
onnx_std = np.std(onnx_times)
onnx_min = np.min(onnx_times)
onnx_max = np.max(onnx_times)

print(f"\nðŸ“Š ONNX Results:")
print(f"   Mean:  {onnx_mean:.2f}ms")
print(f"   Std:   {onnx_std:.2f}ms")
print(f"   Min:   {onnx_min:.2f}ms")
print(f"   Max:   {onnx_max:.2f}ms")

# ===== COMPARAÃ‡ÃƒO =====
print("\n" + "=" * 70)
print("ðŸ“ˆ COMPARAÃ‡ÃƒO")
print("=" * 70)

speedup = pytorch_mean / onnx_mean

print(f"\nðŸ PyTorch:  {pytorch_mean:.2f}ms")
print(f"ðŸš€ ONNX:     {onnx_mean:.2f}ms")
print(f"âš¡ Speedup:  {speedup:.2f}x faster with ONNX")
print(f"ðŸ“‰ ReduÃ§Ã£o:  {(1 - onnx_mean/pytorch_mean) * 100:.1f}%")

if speedup >= 5:
    print(f"\nðŸŽ‰ EXCELENTE! ONNX Ã© {speedup:.2f}x mais rÃ¡pido!")
elif speedup >= 2:
    print(f"\nâœ… Ã“TIMO! ONNX Ã© {speedup:.2f}x mais rÃ¡pido!")
else:
    print(f"\nâš ï¸  ONNX Ã© {speedup:.2f}x mais rÃ¡pido (esperado 5-10x)")

print("\n" + "=" * 70)
print("âœ… BENCHMARK CONCLUÃDO!")
print("=" * 70)

