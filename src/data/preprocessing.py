"""Data preprocessing and cleaning utilities."""

import logging

import pandas as pd  # type: ignore[import-untyped]
from sklearn.model_selection import train_test_split  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Handle data preprocessing and cleaning."""

    def __init__(self, random_state: int = 42) -> None:
        """Initialize preprocessor.

        Args:
            random_state: Random state for reproducibility
        """
        self.random_state = random_state

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataset by removing duplicates and handling missing values.

        Args:
            df: Input dataframe

        Returns:
            Cleaned dataframe
        """
        logger.info(f"Starting data cleaning. Initial rows: {len(df)}")

        # Remove rows with missing values in critical columns
        df = df.dropna(subset=["text", "sentiment"])

        # Remove duplicates based on text
        initial_len = len(df)
        df = df.drop_duplicates(subset=["text"], keep="first")
        removed = initial_len - len(df)
        logger.info(f"Removed {removed} duplicate rows based on text")

        # Remove leading/trailing whitespace
        if "text" in df.columns:
            df["text"] = df["text"].str.strip()

        # Convert sentiment to lowercase and validate
        if "sentiment" in df.columns:
            df["sentiment"] = df["sentiment"].str.lower()
            valid_sentiments = {"positive", "negative", "neutral"}
            invalid_rows = ~df["sentiment"].isin(valid_sentiments)
            removed = invalid_rows.sum()
            if removed > 0:
                logger.warning(f"Removing {removed} rows with invalid sentiment values")
                df = df[~invalid_rows]

        logger.info(f"Cleaning complete. Final rows: {len(df)}")
        return df.reset_index(drop=True)

    def split_data(
        self,
        df: pd.DataFrame,
        test_size: float = 0.2,
        val_size: float = 0.1,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Split data into train, validation, and test sets.

        Args:
            df: Input dataframe
            test_size: Proportion for test set
            val_size: Proportion for validation set (from remaining)

        Returns:
            Tuple of (train_df, val_df, test_df)
        """
        logger.info(
            f"Splitting data: test_size={test_size}, val_size={val_size}",
        )

        # First split: train+val vs test
        train_val_df, test_df = train_test_split(
            df,
            test_size=test_size,
            random_state=self.random_state,
            stratify=df["sentiment"],
        )

        # Second split: train vs val
        val_split_size = val_size / (1 - test_size)
        train_df, val_df = train_test_split(
            train_val_df,
            test_size=val_split_size,
            random_state=self.random_state,
            stratify=train_val_df["sentiment"],
        )

        logger.info(
            f"Split complete - Train: {len(train_df)} "
            f"({100*len(train_df)/len(df):.1f}%), "
            f"Val: {len(val_df)} ({100*len(val_df)/len(df):.1f}%), "
            f"Test: {len(test_df)} ({100*len(test_df)/len(df):.1f}%)",
        )

        return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)

    def preprocess_text(self, text: str) -> str:
        """Apply basic text preprocessing.

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        # Remove extra whitespace
        text = " ".join(text.split())

        # Convert to lowercase
        text = text.lower()

        return text
