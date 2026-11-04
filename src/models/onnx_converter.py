"""ONNX model conversion and optimization."""

import logging
from pathlib import Path

import torch
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)


class ONNXConverter:
    """Convert PyTorch BERT model to ONNX format."""

    def __init__(
        self,
        model_path: Path,
        output_path: Path | None = None,
        model_name: str = "distilbert-base-uncased",
    ) -> None:
        """Initialize converter.

        Args:
            model_path: Path to saved PyTorch model
            output_path: Path to save ONNX model
            model_name: HuggingFace model identifier
        """
        self.model_path = model_path
        self.output_path = output_path or Path("data/models/sentiment_model.onnx")
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def convert(self) -> Path:
        """Convert PyTorch model to ONNX.

        Returns:
            Path to ONNX model
        """
        try:
            from onnxruntime.quantization import QuantType
            from onnxruntime.quantization import quantize_dynamic

            # Load model
            from src.models.train_bert import SentimentModel

            model = SentimentModel(model_name=self.model_name)
            model.load_state_dict(torch.load(self.model_path, map_location="cpu"))
            model.eval()

            # Prepare dummy input
            dummy_input = self.tokenizer(
                "This is a sample text for ONNX conversion",
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=256,
            )

            # Export to ONNX
            torch.onnx.export(
                model,
                (dummy_input["input_ids"], dummy_input["attention_mask"]),
                str(self.output_path),
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

            logger.info(f"ONNX model saved to {self.output_path}")

            # Quantize for optimization
            quantized_path = self.output_path.parent / "sentiment_model_quantized.onnx"
            logger.info("Quantizing model for optimization...")

            quantize_dynamic(
                str(self.output_path),
                str(quantized_path),
                weight_type=QuantType.QUInt8,
            )

            logger.info(f"Quantized ONNX model saved to {quantized_path}")

            return self.output_path

        except ImportError:
            logger.warning("ONNX/ONNX Runtime not installed. Skipping conversion.")
            return self.output_path

    def validate(self) -> bool:
        """Validate ONNX model.

        Returns:
            True if model is valid
        """
        try:
            import onnx

            model = onnx.load(str(self.output_path))
            onnx.checker.check_model(model)
            logger.info("ONNX model validation passed!")
            return True

        except Exception as e:
            logger.error(f"ONNX model validation failed: {e}")
            return False
