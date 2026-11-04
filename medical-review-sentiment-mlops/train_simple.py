#!/usr/bin/env python
"""Script para treinar modelo BERT rapidamente."""

import os
import torch
import pandas as pd
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    TextClassificationPipeline,
)

print("=" * 70)
print("ðŸ¤– TREINAMENTO DO MODELO BERT")
print("=" * 70)

os.environ["DEVICE"] = "cpu"
device = torch.device("cpu")

print(f"\nðŸ“ Device: {device}")
print(f"ðŸ”¢ PyTorch: {torch.__version__}")

# Carregar dataset
print("\nðŸ“‚ Carregando dataset...")
df = pd.read_csv("data/processed/medical_reviews_processed.csv")
print(f"   âœ… {len(df)} exemplos carregados")
print(f"   DistribuiÃ§Ã£o: {dict(df['label_name'].value_counts())}")

# Verificar se modelo jÃ¡ foi treinado
model_path = "data/models/bert_sentiment_model.pt"
if os.path.exists(model_path):
    print(f"\nâœ… Modelo jÃ¡ existe em: {model_path}")
    print("   Pulando treinamento...")
else:
    print("\nðŸŽ“ Treinando modelo...")
    print("   â³ Isso levarÃ¡ alguns minutos em CPU...")
    
    # Carregar modelo prÃ©-treinado
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertForSequenceClassification.from_pretrained(
        model_name,
        num_labels=3,
    )
    model.to(device)
    
    # Preparar dados
    texts = df["text"].tolist()
    labels = df["label"].tolist()
    
    # Tokenizar
    print("   Tokenizando textos...")
    encodings = tokenizer(
        texts,
        truncation=True,
        max_length=256,
        padding=True,
        return_tensors="pt"
    )
    
    # Dataset
    class SentimentDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = torch.tensor(labels)
        
        def __getitem__(self, idx):
            item = {k: v[idx].clone().detach() for k, v in self.encodings.items()}
            item["labels"] = self.labels[idx]
            return item
        
        def __len__(self):
            return len(self.labels)
    
    dataset = SentimentDataset(encodings, labels)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=8, shuffle=True)
    
    # Otimizador
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
    
    # Treino
    num_epochs = 2
    model.train()
    
    for epoch in range(num_epochs):
        print(f"\n   Epoch {epoch+1}/{num_epochs}")
        total_loss = 0
        
        for i, batch in enumerate(dataloader):
            optimizer.zero_grad()
            
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels,
            )
            
            loss = outputs.loss
            total_loss += loss.item()
            
            loss.backward()
            optimizer.step()
            
            if (i + 1) % 5 == 0:
                print(f"      Batch {i+1}/{len(dataloader)} - Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(dataloader)
        print(f"   ðŸ“Š Average Loss: {avg_loss:.4f}")
    
    # Salvar modelo
    os.makedirs("data/models", exist_ok=True)
    torch.save(model.state_dict(), model_path)
    print(f"\nâœ… Modelo salvo em: {model_path}")

print("\n" + "=" * 70)
print("âœ… TREINAMENTO CONCLUÃDO!")
print("=" * 70)

