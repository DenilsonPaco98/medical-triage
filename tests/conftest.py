"""Test configuration and fixtures."""

import pytest


@pytest.fixture
def sample_texts() -> list[str]:
    """Sample texts for testing."""
    return [
        "Excelente médico, muito atencioso!",
        "Atendimento péssimo, não recomendo.",
        "Serviço mediano, nada especial.",
    ]


@pytest.fixture
def sample_dataframe():
    """Sample dataframe for testing."""
    import pandas as pd

    return pd.DataFrame({
        "text": [
            "Excelente médico, muito atencioso!",
            "Atendimento péssimo, não recomendo.",
            "Serviço mediano, nada especial.",
        ],
        "sentiment": ["positive", "negative", "neutral"],
    })
