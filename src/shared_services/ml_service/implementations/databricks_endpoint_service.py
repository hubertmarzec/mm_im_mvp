import time
from typing import Any

from ..exceptions import MLServiceError
from ..ml_service import MLService


class DatabricksEndpointService(MLService):
    """
    Mock implementation of the MLService using a Databricks endpoint.
    """

    def __init__(self, endpoint_url: str = "https://mock-databricks-endpoint.com/api/v1/model/invoke"):
        self.endpoint_url = endpoint_url

    async def call(self, data: Any) -> Any:
        """
        Call the Databricks endpoint with the provided data.

        Args:
            data: Input data for the ML model

        Returns:
            Any: Mocked output from the ML model

        Raises:
            MLServiceError: When the call fails or the model is unavailable
        """
        start_time = time.time()

        # Simulate input validation
        if data is None:
            raise MLServiceError("Input data cannot be None", MLServiceError.INVALID_INPUT)

        try:
            # Simulate processing delay
            await self._mock_delay()

            # Mocked response
            response = {"endpoint_url": self.endpoint_url, "input": data, "output": f"Mocked prediction for input: {data}", "latency_ms": int((time.time() - start_time) * 1000), "status": "success"}
            return response
        except Exception as e:
            raise MLServiceError(f"Failed to call endpoint: {str(e)}", MLServiceError.CALL_ERROR, {"original_error": str(e)}) from e

    async def _mock_delay(self):
        # Simulate async delay (e.g., network latency)
        import asyncio

        await asyncio.sleep(0.01)
