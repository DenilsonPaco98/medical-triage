"""Benchmark inference latency: PyTorch vs ONNX."""

import logging
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from transformers import AutoTokenizer

logger = logging.getLogger(__name__)


class LatencyBenchmark:
    """Benchmark inference latency for different model formats."""

    def __init__(self, model_name: str = "distilbert-base-uncased") -> None:
        """Initialize benchmark.

        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.test_texts = [
            "This is a sample medical review text for benchmarking.",
            "Great doctor, very professional and caring.",
            "Poor service, would not recommend to anyone.",
        ]

    def benchmark_pytorch(
        self,
        model_path: Path,
        num_iterations: int = 100,
    ) -> dict[str, float]:
        """Benchmark PyTorch model inference.

        Args:
            model_path: Path to model weights
            num_iterations: Number of iterations for averaging

        Returns:
            Benchmark metrics (min, max, mean latency in ms)
        """
        from src.models.train_bert import SentimentModel

        logger.info("Benchmarking PyTorch model...")

        model = SentimentModel(model_name=self.model_name)
        if model_path.exists():
            model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()

        latencies = []

        with torch.no_grad():
            for _ in range(num_iterations):
                for text in self.test_texts:
                    inputs = self.tokenizer(
                        text,
                        return_tensors="pt",
                        padding="max_length",
                        truncation=True,
                        max_length=256,
                    )

                    start = time.time()
                    _ = model(inputs["input_ids"], inputs["attention_mask"])
                    latencies.append((time.time() - start) * 1000)

        latencies = np.array(latencies)
        return {
            "min_ms": float(latencies.min()),
            "max_ms": float(latencies.max()),
            "mean_ms": float(latencies.mean()),
            "std_ms": float(latencies.std()),
            "p95_ms": float(np.percentile(latencies, 95)),
            "p99_ms": float(np.percentile(latencies, 99)),
        }

    def benchmark_onnx(
        self,
        onnx_model_path: Path,
        num_iterations: int = 100,
    ) -> dict[str, float]:
        """Benchmark ONNX model inference.

        Args:
            onnx_model_path: Path to ONNX model
            num_iterations: Number of iterations

        Returns:
            Benchmark metrics (min, max, mean latency in ms)
        """
        try:
            import onnxruntime as ort

            logger.info("Benchmarking ONNX model...")

            session = ort.InferenceSession(str(onnx_model_path))
            latencies = []

            for _ in range(num_iterations):
                for text in self.test_texts:
                    inputs = self.tokenizer(
                        text,
                        return_tensors="np",
                        padding="max_length",
                        truncation=True,
                        max_length=256,
                    )

                    start = time.time()
                    _ = session.run(
                        None,
                        {
                            "input_ids": inputs["input_ids"].astype(np.int64),
                            "attention_mask": inputs["attention_mask"].astype(np.int64),
                        },
                    )
                    latencies.append((time.time() - start) * 1000)

            latencies = np.array(latencies)
            return {
                "min_ms": float(latencies.min()),
                "max_ms": float(latencies.max()),
                "mean_ms": float(latencies.mean()),
                "std_ms": float(latencies.std()),
                "p95_ms": float(np.percentile(latencies, 95)),
                "p99_ms": float(np.percentile(latencies, 99)),
            }

        except ImportError:
            logger.warning("ONNX Runtime not installed. Skipping ONNX benchmark.")
            return {}

    def compare(
        self,
        pytorch_model_path: Path,
        onnx_model_path: Path | None = None,
    ) -> dict[str, Any]:
        """Compare PyTorch vs ONNX latency.

        Args:
            pytorch_model_path: Path to PyTorch model
            onnx_model_path: Path to ONNX model

        Returns:
            Comparison results with speedup factor
        """
        results = {}

        # Benchmark PyTorch
        pytorch_metrics = self.benchmark_pytorch(pytorch_model_path)
        results["pytorch"] = pytorch_metrics

        logger.info(f"PyTorch metrics: {pytorch_metrics}")

        # Benchmark ONNX if available
        if onnx_model_path and onnx_model_path.exists():
            onnx_metrics = self.benchmark_onnx(onnx_model_path)
            results["onnx"] = onnx_metrics

            logger.info(f"ONNX metrics: {onnx_metrics}")

            # Calculate speedup
            speedup = pytorch_metrics["mean_ms"] / onnx_metrics["mean_ms"]
            results["speedup"] = speedup

            logger.info(f"Speedup (ONNX vs PyTorch): {speedup:.2f}x")
            logger.info(
                f"Latency reduction: "
                f"{pytorch_metrics['mean_ms']:.2f}ms → {onnx_metrics['mean_ms']:.2f}ms",
            )

        return results
