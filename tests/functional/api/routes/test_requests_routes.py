import io

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.mark.functional
def describe_create_request():
    def will_return_202_with_valid_tiff_file():
        # Create a mock TIFF file
        tiff_content = b"fake tiff content"
        files = {"file": ("test.tiff", io.BytesIO(tiff_content), "image/tiff")}

        response = client.post("/api/v1/request", files=files)
        assert response.status_code == 202
        data = response.json()
        assert "request_id" in data
        assert data["status"] == "pending"
        assert "created_at" in data

    def will_return_400_with_invalid_file_type():
        # Create a mock non-TIFF file
        files = {"file": ("test.txt", io.BytesIO(b"text content"), "text/plain")}

        response = client.post("/api/v1/request", files=files)
        assert response.status_code == 400
        assert "Only TIFF images are supported" in response.json()["detail"]

    def will_return_400_with_missing_file():
        response = client.post("/api/v1/request")
        assert response.status_code == 422  # Validation error


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
