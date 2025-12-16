import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_success():
    response = client.post("/activities/Basketball%20Team/signup?email=tester@example.com")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

def test_signup_duplicate():
    # Sign up once
    client.post("/activities/Drama%20Society/signup?email=dupe@example.com")
    # Try duplicate
    response = client.post("/activities/Drama%20Society/signup?email=dupe@example.com")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
