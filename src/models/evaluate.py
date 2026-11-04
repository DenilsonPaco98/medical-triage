"""Model evaluation utilities."""

import logging

from sklearn.metrics import classification_report  # type: ignore[import-untyped]
from sklearn.metrics import confusion_matrix  # type: ignore[import-untyped]
from sklearn.metrics import f1_score  # type: ignore[import-untyped]
from sklearn.metrics import precision_score  # type: ignore[import-untyped]
from sklearn.metrics import recall_score  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Evaluate model performance on test set."""

    @staticmethod
    def calculate_metrics(
        y_true: list[int],
        y_pred: list[int],
        target_names: list[str] | None = None,
    ) -> dict[str, float]:
        """Calculate evaluation metrics.

        Args:
            y_true: True labels
            y_pred: Predicted labels
            target_names: Names of target classes

        Returns:
            Dictionary of metrics
        """
        accuracy = sum(y_t == y_p for y_t, y_p in zip(y_true, y_pred, strict=False)) / len(y_true)
        precision = precision_score(y_true, y_pred, average="weighted", zero_division=0)
        recall = recall_score(y_true, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

        # Per-class metrics
        if target_names:
            report = classification_report(
                y_true,
                y_pred,
                target_names=target_names,
                output_dict=True,
                zero_division=0,
            )
            for class_name in target_names:
                if class_name in report:
                    metrics[f"{class_name}_f1"] = report[class_name]["f1-score"]
                    metrics[f"{class_name}_precision"] = report[class_name]["precision"]
                    metrics[f"{class_name}_recall"] = report[class_name]["recall"]

        return metrics

    @staticmethod
    def get_confusion_matrix(y_true: list[int], y_pred: list[int]) -> list[list[int]]:
        """Get confusion matrix.

        Args:
            y_true: True labels
            y_pred: Predicted labels

        Returns:
            Confusion matrix
        """
        cm = confusion_matrix(y_true, y_pred)
        return cm.tolist()  # type: ignore[no-any-return]
