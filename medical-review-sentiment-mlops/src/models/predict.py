"""Model inference and prediction."""

import logging
from pathlib import Path
from typing import Optional

import torch
from transformers import AutoTokenizer

from src.models.train_bert import SentimentModel

logger = logging.getLogger(__name__)


class SentimentPredictor:
    """Sentiment prediction using fine-tuned BERT model."""

    LABELS = ["negative", "neutral", "positive"]

    def __init__(
        self,
        model_path: Optional[Path] = None,
        model_name: str = "distilbert-base-uncased",
        device: str = "cuda",
    ) -> None:
        """Initialize predictor.

        Args:
            model_path: Path to saved model weights
            model_name: HuggingFace model identifier
            device: Device to use (cuda or cpu)
        """
        self.model_name = model_name
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = SentimentModel(model_name=model_name, num_labels=len(self.LABELS)).to(device)

        if model_path and Path(model_path).exists():
            logger.info(f"Loading model weights from {model_path}")
            self.model.load_state_dict(torch.load(model_path, map_location=device))

        self.model.eval()

    def predict(self, text: str) -> dict[str, float | str]:
        """Predict sentiment for a single text.

        Args:
            text: Input text

        Returns:
            Dictionary with sentiment and confidence scores
        """
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=256,
            padding="max_length",
        ).to(self.device)

        # Predict
        with torch.no_grad():
            probs = self.model.predict(inputs["input_ids"], inputs["attention_mask"])

        # Get results
        scores = probs[0].cpu().numpy()
        predicted_class_idx = scores.argmax()
        predicted_sentiment = self.LABELS[predicted_class_idx]
        confidence = float(scores[predicted_class_idx])

        return {
            "text": text,
            "sentiment": predicted_sentiment,
            "confidence": confidence,
            "scores": {
                "negative": float(scores[0]),
                "neutral": float(scores[1]),
                "positive": float(scores[2]),
            },
        }

    def predict_batch(self, texts: list[str]) -> list[dict[str, float | str]]:
        """Predict sentiment for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of prediction dictionaries
        """
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
