"""Train a sentiment classifier from the project's labeled CSV dataset."""

import argparse
import logging
from pathlib import Path
from typing import Any

import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from src.models.train_bert import BertTrainer

LOGGER = logging.getLogger(__name__)
LABEL_TO_ID = {"negative": 0, "neutral": 1, "positive": 2}


def _label_to_id(value: object) -> int:
    """Normalize text or integer sentiment labels to the model's class IDs."""
    if isinstance(value, str) and value.strip().lower() in LABEL_TO_ID:
        return LABEL_TO_ID[value.strip().lower()]

    if not isinstance(value, (int, float)):
        raise ValueError(f"Unsupported sentiment label: {value!r}")
    label_id = int(value)

    if label_id not in LABEL_TO_ID.values():
        raise ValueError(f"Sentiment label must be 0, 1, or 2; got {value!r}")
    return label_id


def _tokenized_items(
    texts: list[str],
    labels: list[int],
    tokenizer: Any,
    max_length: int,
) -> Dataset[dict[str, torch.Tensor]]:
    """Tokenize reviews into batches accepted by BertTrainer."""
    encoded = tokenizer(
        texts,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=max_length,
    )
    return TokenizedReviews(
        input_ids=encoded["input_ids"],
        attention_mask=encoded["attention_mask"],
        labels=torch.tensor(labels, dtype=torch.long),
    )


class TokenizedReviews(Dataset[dict[str, torch.Tensor]]):
    """PyTorch dataset for tokenized reviews and sentiment labels."""

    def __init__(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        labels: torch.Tensor,
    ) -> None:
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.labels = labels

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int) -> dict[str, torch.Tensor]:
        return {
            "input_ids": self.input_ids[index],
            "attention_mask": self.attention_mask[index],
            "labels": self.labels[index],
        }


def train_from_csv(
    dataset_path: Path,
    output_dir: Path,
    model_name: str = "distilbert-base-uncased",
    device: str = "cpu",
    epochs: int = 2,
    batch_size: int = 8,
    max_length: int = 128,
) -> Path:
    """Fine-tune a sequence classifier and return its checkpoint path."""
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Training dataset not found: {dataset_path}")

    frame = pd.read_csv(dataset_path)
    label_column = next(
        (column for column in ("sentiment", "label_name", "label") if column in frame.columns),
        None,
    )
    if "text" not in frame.columns or label_column is None:
        raise ValueError("Dataset must have a 'text' column and a sentiment/label column")

    frame = frame.dropna(subset=["text", label_column]).copy()
    texts = frame["text"].astype(str).str.strip().tolist()
    labels = [_label_to_id(value) for value in frame[label_column].tolist()]
    nonempty = [(text, label) for text, label in zip(texts, labels, strict=True) if text]
    if len(nonempty) < 6:
        raise ValueError("At least six non-empty labeled reviews are required for training")

    texts, labels = map(list, zip(*nonempty, strict=True))
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    train_items = _tokenized_items(train_texts, train_labels, tokenizer, max_length)
    val_items = _tokenized_items(val_texts, val_labels, tokenizer, max_length)
    train_loader: DataLoader[dict[str, torch.Tensor]] = DataLoader(
        train_items,
        batch_size=batch_size,
        shuffle=True,
    )
    val_loader: DataLoader[dict[str, torch.Tensor]] = DataLoader(
        val_items,
        batch_size=batch_size,
    )

    trainer = BertTrainer(
        model_name=model_name,
        device=device,
        learning_rate=2e-5,
        num_epochs=epochs,
        batch_size=batch_size,
    )
    trainer.fit(train_loader, val_loader, output_dir=output_dir)
    return output_dir / "bert_sentiment_model.pt"


def main() -> None:
    """Parse command-line options and train the sentiment model."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("data/raw/medical_reviews.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/models"))
    parser.add_argument("--model-name", default="distilbert-base-uncased")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=128)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    checkpoint = train_from_csv(
        dataset_path=args.data,
        output_dir=args.output_dir,
        model_name=args.model_name,
        device=args.device,
        epochs=args.epochs,
        batch_size=args.batch_size,
        max_length=args.max_length,
    )
    LOGGER.info("Saved fine-tuned sentiment checkpoint to %s", checkpoint)


if __name__ == "__main__":
    main()
