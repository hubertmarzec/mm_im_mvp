from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def describe_healthcheck():
    def will_return_success():
        response = client.get("/api/v1/healthcheck")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert data["service"] == "input-management-api" 


        