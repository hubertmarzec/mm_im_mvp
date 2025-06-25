import re
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from src.main import app
from src.models import Request
from src.services.request_service import RequestService


def pytest_addoption(parser):
    """Add command line options for all tests."""
    parser.addoption("--env", action="store", help="Environment to run E2E tests against: dev, qa, acc, etc.")


@pytest.fixture
def client():
    return TestClient(app)


def create_test_app(mock_request_repository, mock_ocr_service, mock_file_storage, mock_ml_service):
    """Create a test app with mocked dependencies"""
    from src.api.requests_routes import requests_routes
    from src.services.request_service import RequestService

    # Create a new FastAPI app
    test_app = FastAPI(
        title="Input Management API - Test",
        description="API for managing PC input devices - Test Version",
        version="1.0.0",
    )

    # Add CORS middleware
    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Create RequestService with mocked dependencies
    request_service = RequestService(
        mock_request_repository,
        mock_ocr_service,
        mock_file_storage,
        mock_ml_service,
    )

    # Override the dependency function
    def get_test_request_service():
        return request_service

    # Add the routes with overridden dependency
    test_app.dependency_overrides[requests_routes.dependencies[0].dependency] = get_test_request_service

    # Include the routes
    test_app.include_router(requests_routes, prefix="/api/v1", tags=["input"])

    return test_app


@pytest.fixture
def test_client(mock_request_repository, mock_ocr_service, mock_file_storage, mock_ml_service):
    """Test client with mocked dependencies"""
    from src.api.requests_routes import get_request_service

    # Create RequestService with mocked dependencies
    request_service = RequestService(
        mock_request_repository,
        mock_ocr_service,
        mock_file_storage,
        mock_ml_service,
    )

    # Override the dependency function
    def get_test_request_service():
        return request_service

    # Override the dependency in the app
    app.dependency_overrides[get_request_service] = get_test_request_service

    test_client = TestClient(app)

    # Clean up after test
    yield test_client

    # Remove the override
    app.dependency_overrides.clear()


@pytest.fixture
def mock_request_repository():
    """Mock RequestRepository for testing"""
    mock_repo = AsyncMock()

    # Mock create method
    def create_side_effect(request: Request) -> Request:
        # Return the same request (simulating successful creation)
        return request

    mock_repo.create.side_effect = create_side_effect

    # Mock get_by_id method
    def get_by_id_side_effect(request_id: str):
        if request_id == "test-id":
            return Request(
                id="test-id",
                status="pending",
                created_at=datetime(2025, 1, 1, 0, 0, 0),
                updated_at=datetime(2025, 1, 1, 0, 0, 0),
                completed_at=None,
                result=None,
            )
        elif request_id == "invalid-id":
            return None
        else:
            return None

    mock_repo.get_by_id.side_effect = get_by_id_side_effect

    # Mock update method
    mock_repo.update.return_value = True

    # Mock exists method
    mock_repo.exists.return_value = True

    return mock_repo


@pytest.fixture
def mock_ocr_service():
    """Mock OcrService for testing"""
    mock_ocr = AsyncMock()

    # Mock extract_text_from_file method
    mock_result = MagicMock()
    mock_result.json = {"text": "Sample extracted text"}
    mock_ocr.extract_text_from_file.return_value = mock_result

    return mock_ocr


@pytest.fixture
def mock_file_storage():
    """Mock FileStorageService for testing"""
    mock_storage = AsyncMock()

    # Mock save method
    mock_storage.save.return_value = "test-file-path"

    # Mock saveFromDict method
    mock_storage.saveFromDict.return_value = "test-json-file-path"

    return mock_storage


@pytest.fixture
def mock_ml_service():
    """Mock MLService for testing"""
    mock_ml = AsyncMock()

    # Mock call method
    mock_ml.call.return_value = {"classification": "test-category", "confidence": 0.95}

    return mock_ml


def camel_to_snake(name):
    """Convert CamelCase string to snake_case."""
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    return pattern.sub("_", name).lower()


def underscore_to_human(name):
    """Convert underscore_separated string to Human Readable format with only first letter capitalized."""
    return " ".join(name.split("_")).capitalize()


def pytest_itemcollected(item):
    """Change test name display in output."""
    # Replace 'tests/anything/' with empty string
    item._nodeid = re.sub(r"tests/[^/]+/", "", item._nodeid)
    item._nodeid = item._nodeid.replace(".py", "").replace("test_", "")

    # Convert class name from CamelCase to snake_case if pattern matches
    parts = item._nodeid.split("::")
    if len(parts) == 3:
        parts[1] = camel_to_snake(parts[1])
        if parts[1].startswith("test_"):
            parts[1] = parts[1][5:]  # Remove "test_" prefix
        item._nodeid = "::".join(parts)

    # Remove "describe_" prefix in parts[1]
    if parts[1].startswith("describe_"):
        parts[1] = parts[1][9:]

    # Convert the last part (test case name) to human readable format
    if len(parts) > 1:
        parts[-1] = underscore_to_human(parts[-1])

    item._nodeid = "::".join(parts)
