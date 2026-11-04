"""Tests for API endpoints."""

from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_invalid_input():
    """Test prediction with invalid input."""
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
