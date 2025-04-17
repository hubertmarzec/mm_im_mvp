import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


@pytest.mark.functional
def describe_get_request():
    def will_return_success_with_valid_request_id():
        request_id = "test-id"
        response = client.get(f"/api/v1/request/{request_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["request_id"] == request_id
        assert data["status"] == "pending"
    
    def will_return_error_with_missing_request_id():
        request_id = "invalid-id"
        response = client.get(f"/api/v1/request/{request_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Request not found"


def describe_get_request_list():
    def will_return_success():
        response = client.get("/api/v1/request")
        assert response.status_code == 200
        data = response.json()
        assert data["requests"] is not None
        assert data["total"] is not None    

