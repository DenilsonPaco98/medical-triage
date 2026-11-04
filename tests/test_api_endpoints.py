"""Tests para endpoints da API FastAPI."""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


class FakePredictor:
    """Deterministic predictor for API endpoint tests."""

    def predict(self, text: str) -> dict[str, object]:
        return {
            "text": text,
            "sentiment": "positive",
            "confidence": 0.9,
            "scores": {"negative": 0.02, "neutral": 0.08, "positive": 0.9},
        }

    def predict_batch(self, texts: list[str]) -> list[dict[str, object]]:
        return [self.predict(text) for text in texts]


@pytest.fixture(autouse=True)
def mock_predictor(monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid model downloads and inference during API tests."""
    monkeypatch.setattr("src.api.routes.get_predictor", lambda: FakePredictor())


class TestHealthEndpoint:
    """Testes para endpoint /health."""

    def test_health_returns_200(self):
        """Health endpoint deve retornar 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "version": "0.2.0"}


class TestPredictEndpoint:
    """Testes para endpoint /predict."""

    def test_predict_single_text(self):
        """Deve fazer predicao para texto individual."""
        payload = {"text": "Great doctor! Very professional."}
        response = client.post("/predict", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == payload["text"]
        assert data["sentiment"] == "positive"
        assert "confidence" in data
        assert 0 <= data["confidence"] <= 1
        assert set(data["scores"]) == {"negative", "neutral", "positive"}

    def test_predict_empty_text_raises_error(self):
        """Deve retornar erro para texto vazio."""
        payload = {"text": ""}
        response = client.post("/predict", json=payload)

        assert response.status_code in [400, 422]

    def test_predict_batch_multiple_texts(self):
        """Deve fazer predicao para multiplos textos."""
        payload = {
            "texts": [
                "Excellent service!",
                "Average experience.",
                "Terrible treatment!"
            ]
        }
        response = client.post("/predict-batch", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(item["sentiment"] == "positive" for item in data)


class TestMetricsEndpoint:
    """Testes para endpoint /metrics."""

    def test_metrics_endpoint_available(self):
        """Metrics endpoint deve estar disponivel."""
        response = client.get("/metrics")
        assert response.status_code == 200
        # Prometheus format
        assert "HELP" in response.text or "TYPE" in response.text or len(response.text) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
