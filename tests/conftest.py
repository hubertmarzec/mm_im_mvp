import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import re

@pytest.fixture
def client():
    return TestClient(app)

def camel_to_snake(name):
    """Convert CamelCase string to snake_case."""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()

def pytest_itemcollected(item):
    """Change test name display in output."""
    # Replace 'tests/anything/' with empty string
    item._nodeid = re.sub(r'tests/[^/]+/', '', item._nodeid)
    item._nodeid = item._nodeid.replace(".py", "").replace("test_", "")
    
    # Convert class name from CamelCase to snake_case if pattern matches
    parts = item._nodeid.split("::")
    if len(parts) == 3:
        parts[1] = camel_to_snake(parts[1])
        if parts[1].startswith("test_"):
            parts[1] = parts[1][5:]  # Remove "test_" prefix
        item._nodeid = "::".join(parts)
    