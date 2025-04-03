import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

class TestRequestRoutes:
    def test_get_request_list(self):
        response = client.get("/api/v1/request")
        assert response.status_code == 200
        data = response.json()
        assert "requests" in data
        assert "total" in data
        assert isinstance(data["requests"], list)
        assert data["total"] == len(data["requests"])

class TestGetRequest:
    def test_will_return_success_with_valid_request_id(self):
        request_id = "test-id"
        response = client.get(f"/api/v1/request/{request_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["request_id"] == request_id
        assert data["status"] == "pending"
        assert "created_at" in data 

    def test_will_return_error_with_missing_request_id(self):
        request_id = "invalid-id"
        response = client.get(f"/api/v1/request/{request_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Request not found"