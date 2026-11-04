#!/usr/bin/env python
"""Script para converter modelo para ONNX apÃ³s treinamento."""

import os
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer

print("=" * 70)
print("[*] CONVERSAO PARA ONNX")
print("=" * 70)

model_path = "data/models/bert_sentiment_model.pt"
onnx_path = "data/models/sentiment_model.onnx"

# Verificar se modelo existe
if not os.path.exists(model_path):
    print(f"âŒ Modelo nÃ£o encontrado: {model_path}")
    print("Execute train_simple.py primeiro!")
    exit(1)

print(f"\nâœ… Modelo encontrado: {model_path}")

# Carregar modelo
print("\nðŸ“‚ Carregando modelo...")
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Carregar pesos treinados
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()
print("âœ… Modelo carregado")

# Converter para ONNX
print("\nðŸ”„ Convertendo para ONNX...")

# Input dummy
dummy_input = tokenizer(
    "This is a test sentence about medical review.",
    return_tensors="pt",
    max_length=256,
    padding=True,
    truncation=True,
)

input_ids = dummy_input["input_ids"]
attention_mask = dummy_input["attention_mask"]

# Export
torch.onnx.export(
    model,
    (input_ids, attention_mask),
    onnx_path,
    input_names=["input_ids", "attention_mask"],
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch_size", 1: "sequence_length"},
        "attention_mask": {0: "batch_size", 1: "sequence_length"},
        "logits": {0: "batch_size"},
    },
    opset_version=14,
    do_constant_folding=True,
)

print(f"âœ… Modelo ONNX salvo: {onnx_path}")

# Validar ONNX
print("\nðŸ” Validando modelo ONNX...")
try:
    import onnx
    onnx_model = onnx.load(onnx_path)
    onnx.checker.check_model(onnx_model)
    print("âœ… Modelo ONNX vÃ¡lido!")
except Exception as e:
    print(f"âš ï¸  Erro na validaÃ§Ã£o: {e}")

# Testar com ONNXRuntime
print("\nâš¡ Testando com ONNXRuntime...")
try:
    import onnxruntime as rt
    
    sess = rt.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
    
    # Fazer prediÃ§Ã£o
    output = sess.run(
        None,
        {
            "input_ids": input_ids.numpy(),
            "attention_mask": attention_mask.numpy(),
        }
    )
    
    print(f"âœ… ONNXRuntime funcionando!")
    print(f"   Output shape: {output[0].shape}")
except Exception as e:
    print(f"âš ï¸  Erro: {e}")

print("\n" + "=" * 70)
print("âœ… CONVERSÃƒO CONCLUÃDA!")
print("=" * 70)

