import pytest

from ..exceptions import MLServiceError
from ..implementations.databricks_endpoint_service import DatabricksEndpointService


class TestDatabricksEndpointService:
    """Test cases for DatabricksEndpointService."""

    @pytest.fixture
    def ml_service(self):
        """Create a DatabricksEndpointService instance for testing."""
        return DatabricksEndpointService()

    @pytest.fixture
    def custom_endpoint_service(self):
        """Create a DatabricksEndpointService with custom endpoint URL."""
        return DatabricksEndpointService("https://custom-endpoint.com/api/v1/model/invoke")

    @pytest.mark.asyncio
    async def test_call_success(self, ml_service):
        """Test successful ML model call."""
        test_data = {"text": "sample input", "model": "test-model"}
        result = await ml_service.call(test_data)

        assert result is not None
        assert result["status"] == "success"
        assert result["input"] == test_data
        assert "Mocked prediction for input:" in result["output"]
        assert "latency_ms" in result
        assert result["latency_ms"] >= 0
        assert result["endpoint_url"] == "https://mock-databricks-endpoint.com/api/v1/model/invoke"

    @pytest.mark.asyncio
    async def test_call_with_string_input(self, ml_service):
        """Test ML model call with string input."""
        test_data = "simple string input"
        result = await ml_service.call(test_data)

        assert result["input"] == test_data
        assert "Mocked prediction for input: simple string input" in result["output"]

    @pytest.mark.asyncio
    async def test_call_with_list_input(self, ml_service):
        """Test ML model call with list input."""
        test_data = [1, 2, 3, "test"]
        result = await ml_service.call(test_data)

        assert result["input"] == test_data
        assert "Mocked prediction for input:" in result["output"]

    @pytest.mark.asyncio
    async def test_call_with_none_input(self, ml_service):
        """Test ML model call with None input."""
        with pytest.raises(MLServiceError) as exc_info:
            await ml_service.call(None)

        assert exc_info.value.error_code == MLServiceError.INVALID_INPUT
        assert "Input data cannot be None" in exc_info.value.message

    @pytest.mark.asyncio
    async def test_call_with_custom_endpoint(self, custom_endpoint_service):
        """Test ML model call with custom endpoint URL."""
        test_data = {"custom": "data"}
        result = await custom_endpoint_service.call(test_data)

        assert result["endpoint_url"] == "https://custom-endpoint.com/api/v1/model/invoke"
        assert result["input"] == test_data

    @pytest.mark.asyncio
    async def test_call_latency_measurement(self, ml_service):
        """Test that latency is properly measured."""
        test_data = "test"
        result = await ml_service.call(test_data)

        # Should have some latency due to the mock delay
        assert result["latency_ms"] > 0
        assert isinstance(result["latency_ms"], int)

    @pytest.mark.asyncio
    async def test_call_response_structure(self, ml_service):
        """Test that response has the expected structure."""
        test_data = {"key": "value"}
        result = await ml_service.call(test_data)

        expected_keys = ["endpoint_url", "input", "output", "latency_ms", "status"]
        for key in expected_keys:
            assert key in result

    @pytest.mark.asyncio
    async def test_call_with_empty_dict(self, ml_service):
        """Test ML model call with empty dictionary."""
        test_data = {}
        result = await ml_service.call(test_data)

        assert result["input"] == test_data
        assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_call_with_zero_value(self, ml_service):
        """Test ML model call with zero value."""
        test_data = 0
        result = await ml_service.call(test_data)

        assert result["input"] == test_data
        assert "Mocked prediction for input: 0" in result["output"]

    @pytest.mark.asyncio
    async def test_call_with_boolean_value(self, ml_service):
        """Test ML model call with boolean value."""
        test_data = True
        result = await ml_service.call(test_data)

        assert result["input"] == test_data
        assert "Mocked prediction for input: True" in result["output"]
