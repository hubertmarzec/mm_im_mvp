import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

class TestStatusRoutes:
    def test_healthcheck(self):
        response = client.get("/api/v1/healthcheck")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert data["service"] == "input-management-api"

class TestRequestRoutes:
    def test_get_request_list(self):
        response = client.get("/api/v1/request")
        assert response.status_code == 200
        data = response.json()
        assert "requests" in data
        assert "total" in data
        assert isinstance(data["requests"], list)
        assert data["total"] == len(data["requests"])

    def test_get_request_by_id(self):
        request_id = "test-id"
        response = client.get(f"/api/v1/request/{request_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["request_id"] == request_id
        assert data["status"] == "pending"
        assert "created_at" in data 