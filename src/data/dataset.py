"""Dataset preparation and loading from Kaggle."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class DatasetPreparation:
    """Handle dataset download and preparation from Kaggle."""

    def __init__(self, dataset_name: str = "d7c7b0c7/medical-reviews", output_dir: Path | None = None) -> None:
        """Initialize dataset preparation.

        Args:
            dataset_name: Kaggle dataset identifier
            output_dir: Output directory for raw data
        """
        self.dataset_name = dataset_name
        self.output_dir = output_dir or Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare(self, force: bool = False) -> Path:
        """Prepare dataset by downloading from Kaggle if needed.

        Args:
            force: Force re-download of dataset

        Returns:
            Path to the dataset CSV file
        """
        output_path = self.output_dir / "medical_reviews.csv"

        if output_path.exists() and not force:
            logger.info(f"Dataset already exists at {output_path}")
            return output_path

        try:
            logger.info(f"Downloading dataset {self.dataset_name} from Kaggle...")
            import kagglehub

            path = kagglehub.dataset_download(self.dataset_name)
            logger.info(f"Downloaded to {path}")

            # Find and copy CSV file
            for csv_file in Path(path).glob("*.csv"):
                logger.info(f"Found CSV file: {csv_file}")
                df = pd.read_csv(csv_file)
                df.to_csv(output_path, index=False)
                logger.info(f"Dataset saved to {output_path}")
                return output_path

            raise FileNotFoundError("No CSV file found in downloaded dataset")

        except ImportError:
            logger.warning("kagglehub not installed. Creating sample dataset...")
            return self._create_sample_dataset(output_path)
        except Exception as e:
            logger.error(f"Error downloading dataset: {e}")
            return self._create_sample_dataset(output_path)

    def _create_sample_dataset(self, output_path: Path) -> Path:
        """Create a sample dataset for development/testing.

        Args:
            output_path: Path to save sample dataset

        Returns:
            Path to the sample dataset
        """
        logger.info("Creating sample dataset for development...")

        sample_data = {
            "text": [
                "Excelente médico, muito atencioso e dedicado!",
                "Atendimento péssimo, não recomendo a ninguém.",
                "O médico é OK, nada de especial.",
                "Profissional competente e simpático.",
                "Tive uma experiência horrível nesta clínica.",
                "Muito bom, voltaria com certeza!",
                "Serviço mediano, poderia melhorar.",
                "Adorei o atendimento, voltaria sempre!",
                "Não gostei, muito caro para o serviço.",
                "Excelente profissional, recomendo!",
            ],
            "sentiment": [
                "positive",
                "negative",
                "neutral",
                "positive",
                "negative",
                "positive",
                "neutral",
                "positive",
                "negative",
                "positive",
            ],
            "rating": [5, 1, 3, 4, 1, 5, 3, 5, 2, 5],
        }

        df = pd.DataFrame(sample_data)
        df.to_csv(output_path, index=False)
        logger.info(f"Sample dataset created at {output_path}")
        return output_path


def prepare_dataset(dataset_name: str = "d7c7b0c7/medical-reviews", force: bool = False) -> Path:
    """Convenience function to prepare dataset.

    Args:
        dataset_name: Kaggle dataset identifier
        force: Force re-download

    Returns:
        Path to prepared dataset
    """
    prep = DatasetPreparation(dataset_name=dataset_name)
    return prep.prepare(force=force)
