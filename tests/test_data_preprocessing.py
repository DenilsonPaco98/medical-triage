"""Tests for data preprocessing."""

import pandas as pd

from src.data.preprocessing import DataPreprocessor


def test_data_cleaner_remove_duplicates():
    """Test duplicate removal."""
    preprocessor = DataPreprocessor()

    df = pd.DataFrame({
        "text": ["Hello", "Hello", "World"],
        "sentiment": ["positive", "positive", "negative"],
    })

    cleaned = preprocessor.clean(df)
    assert len(cleaned) == 2


def test_data_cleaner_remove_invalid_sentiment():
    """Test removal of invalid sentiment labels."""
    preprocessor = DataPreprocessor()

    df = pd.DataFrame({
        "text": ["Hello", "World", "Test"],
        "sentiment": ["positive", "invalid", "negative"],
    })

    cleaned = preprocessor.clean(df)
    assert len(cleaned) == 2
