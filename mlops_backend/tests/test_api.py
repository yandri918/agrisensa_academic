import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add project root directory to sys.path to find main.py and other files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "AgriSensa MLOps API"
    assert "docs_url" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in ["healthy", "degraded"]

def test_recommend_crop():
    payload = {
        "n_value": 90.0,
        "p_value": 42.0,
        "k_value": 43.0,
        "temperature": 20.8,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9
    }
    response = client.post("/api/ml/recommend-crop", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "recommended_crop" in data
    assert "crop" in data["recommended_crop"]
    assert "confidence" in data["recommended_crop"]

def test_predict_yield():
    payload = {
        "nitrogen": 120.0,
        "phosphorus": 75.0,
        "potassium": 75.0,
        "temperature": 26.5,
        "rainfall": 1800.0,
        "ph": 6.2
    }
    response = client.post("/api/ml/predict-yield", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "predicted_yield_ton_ha" in data
    assert data["predicted_yield_ton_ha"] >= 0.0

def test_predict_yield_advanced():
    payload = {
        "nitrogen": 120.0,
        "phosphorus": 75.0,
        "potassium": 75.0,
        "temperature": 26.5,
        "rainfall": 1800.0,
        "ph": 6.2
    }
    response = client.post("/api/ml/predict-yield-advanced", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "predicted_yield_ton_ha" in data
    assert "feature_importances" in data
    assert "shap_values" in data

def test_generate_yield_plan():
    payload = {
        "commodity": "padi",
        "target_yield": 6.5
    }
    response = client.post("/api/ml/generate-yield-plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "plan" in data
    assert data["plan"]["commodity_name"] == "Padi"
    assert data["plan"]["target_yield"] == 6.5

def test_calculate_fertilizer_bags():
    payload = {
        "nutrient_needed": "N",
        "nutrient_amount_kg": 46.0,
        "fertilizer_type": "urea"
    }
    response = client.post("/api/ml/calculate-fertilizer-bags", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["required_fertilizer_kg"] == 100.0
    assert data["fertilizer_name"] == "Urea"

def test_predict_success():
    payload = {
        "nitrogen": 120.0,
        "phosphorus": 75.0,
        "potassium": 75.0,
        "temperature": 26.5,
        "rainfall": 1800.0,
        "ph": 6.2
    }
    response = client.post("/api/ml/predict-success", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "status" in data
    assert "probability_of_success" in data

def test_npk_analysis():
    payload = {
        "n_value": 120.0,
        "p_value": 20.0,
        "k_value": 150.0
    }
    response = client.post("/api/analysis/npk", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "analysis" in data
    assert "Nitrogen (N)" in data["analysis"]
    assert "Fosfor (P)" in data["analysis"]
    assert "Kalium (K)" in data["analysis"]
