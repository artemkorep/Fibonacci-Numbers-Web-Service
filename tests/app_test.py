from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_valid_input():
    response = client.get("/fibonacci?n=10")
    assert response.status_code == 200
    assert response.json() == {"n": 10, "result": 55}

def test_missing_parameter():
    response = client.get("/fibonacci")
    assert response.status_code == 400
    assert "required" in response.json()["error"].lower()

def test_negative_number():
    response = client.get("/fibonacci?n=-5")
    assert response.status_code == 400
    assert "non-negative" in response.json()["error"].lower()

def test_non_integer():
    response = client.get("/fibonacci?n=abc")
    assert response.status_code == 400
    assert "integer" in response.json()["error"].lower()