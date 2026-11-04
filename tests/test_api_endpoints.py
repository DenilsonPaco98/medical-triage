"""Tests para endpoints da API FastAPI."""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


class TestHealthEndpoint:
    """Testes para endpoint /health."""

    def test_health_returns_200(self):
        """Health endpoint deve retornar 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestPredictEndpoint:
    """Testes para endpoint /predict."""

    def test_predict_single_text(self):
        """Deve fazer predicao para texto individual."""
        payload = {"text": "Great doctor! Very professional."}
        response = client.post("/predict", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "confidence" in data
        assert data["prediction"] in [0, 1, 2]  # 3 classes
        assert 0 <= data["confidence"] <= 1

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
        assert "predictions" in data
        assert len(data["predictions"]) == 3


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
