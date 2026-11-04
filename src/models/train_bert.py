"""Model training for BERT fine-tuning."""

import logging
import time
from pathlib import Path
from typing import ClassVar

import mlflow
import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from torch import nn
from torch.optim import AdamW
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)


class SentimentModel(nn.Module):
    """Fine-tuned BERT model for sentiment classification."""

    def __init__(self, model_name: str = "distilbert-base-uncased", num_labels: int = 3) -> None:
        """Initialize model.

        Args:
            model_name: HuggingFace model identifier
            num_labels: Number of output classes (positive, neutral, negative)
        """
        super().__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
        )
        self.num_labels = num_labels

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            input_ids: Tokenized input IDs
            attention_mask: Attention mask

        Returns:
            Logits for classification
        """
        outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        return outputs.logits

    def predict(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """Get predictions (probabilities).

        Args:
            input_ids: Tokenized input IDs
            attention_mask: Attention mask

        Returns:
            Predicted class probabilities
        """
        with torch.no_grad():
            logits = self.forward(input_ids, attention_mask)
            probs = F.softmax(logits, dim=-1)
        return probs


class BertTrainer:
    """Trainer for BERT sentiment classification."""

    LABELS: ClassVar[list[str]] = ["negative", "neutral", "positive"]

    def __init__(
        self,
        model_name: str = "distilbert-base-uncased",
        device: str = "cuda",
        learning_rate: float = 2e-5,
        num_epochs: int = 3,
        batch_size: int = 32,
    ) -> None:
        """Initialize trainer.

        Args:
            model_name: HuggingFace model identifier
            device: Device to use (cuda or cpu)
            learning_rate: Learning rate
            num_epochs: Number of training epochs
            batch_size: Batch size
        """
        self.model_name = model_name
        self.device = device
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs
        self.batch_size = batch_size

        self.model = SentimentModel(model_name=model_name, num_labels=len(self.LABELS)).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def train_epoch(self, train_loader: DataLoader) -> float:
        """Train for one epoch.

        Args:
            train_loader: Training data loader

        Returns:
            Average training loss
        """
        self.model.train()
        total_loss = 0.0

        for batch in train_loader:
            input_ids = batch["input_ids"].to(self.device)
            attention_mask = batch["attention_mask"].to(self.device)
            labels = batch["labels"].to(self.device)

            self.optimizer.zero_grad()

            logits = self.model(input_ids, attention_mask)
            loss = F.cross_entropy(logits, labels)

            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(train_loader)

    def evaluate(self, eval_loader: DataLoader) -> dict[str, float]:
        """Evaluate on validation/test set.

        Args:
            eval_loader: Evaluation data loader

        Returns:
            Dictionary of metrics
        """
        self.model.eval()
        predictions = []
        true_labels = []
        total_loss = 0.0

        with torch.no_grad():
            for batch in eval_loader:
                input_ids = batch["input_ids"].to(self.device)
                attention_mask = batch["attention_mask"].to(self.device)
                labels = batch["labels"].to(self.device)

                logits = self.model(input_ids, attention_mask)
                loss = F.cross_entropy(logits, labels)
                total_loss += loss.item()

                preds = logits.argmax(dim=-1).cpu().numpy()
                predictions.extend(preds)
                true_labels.extend(labels.cpu().numpy())

        # Calculate metrics
        accuracy = accuracy_score(true_labels, predictions)
        precision = precision_score(true_labels, predictions, average="weighted", zero_division=0)
        recall = recall_score(true_labels, predictions, average="weighted", zero_division=0)
        f1 = f1_score(true_labels, predictions, average="weighted", zero_division=0)

        return {
            "loss": total_loss / len(eval_loader),
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    def fit(
        self,
        train_loader: DataLoader,
        val_loader: DataLoader,
        output_dir: Path | None = None,
    ) -> dict[str, list[float]]:
        """Train the model.

        Args:
            train_loader: Training data loader
            val_loader: Validation data loader
            output_dir: Directory to save model

        Returns:
            Training history
        """
        self.optimizer = AdamW(self.model.parameters(), lr=self.learning_rate)
        output_dir = output_dir or Path("data/models")
        output_dir.mkdir(parents=True, exist_ok=True)

        history = {"train_loss": [], "val_loss": [], "val_accuracy": []}

        logger.info(f"Starting training for {self.num_epochs} epochs...")
        start_time = time.time()

        for epoch in range(self.num_epochs):
            train_loss = self.train_epoch(train_loader)
            val_metrics = self.evaluate(val_loader)

            history["train_loss"].append(train_loss)
            history["val_loss"].append(val_metrics["loss"])
            history["val_accuracy"].append(val_metrics["accuracy"])

            logger.info(
                f"Epoch {epoch + 1}/{self.num_epochs} - "
                f"Train Loss: {train_loss:.4f}, "
                f"Val Loss: {val_metrics['loss']:.4f}, "
                f"Val Accuracy: {val_metrics['accuracy']:.4f}",
            )

            # Log to MLflow
            mlflow.log_metrics(
                {
                    "train_loss": train_loss,
                    "val_loss": val_metrics["loss"],
                    "val_accuracy": val_metrics["accuracy"],
                },
                step=epoch,
            )

        elapsed = time.time() - start_time
        logger.info(f"Training completed in {elapsed:.2f} seconds")

        # Save final model
        model_path = output_dir / "bert_sentiment_model.pt"
        torch.save(self.model.state_dict(), model_path)
        logger.info(f"Model saved to {model_path}")

        return history
