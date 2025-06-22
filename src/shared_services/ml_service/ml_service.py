from abc import ABC, abstractmethod
from typing import Any


class MLService(ABC):
    """
    Interface for ML (Machine Learning) services.
    """

    @abstractmethod
    async def call(self, data: Any) -> Any:
        """
        Call the ML model with the provided data.

        Args:
            data: Input data for the ML model

        Returns:
            Any: Output from the ML model

        Raises:
            MLServiceError: When the call fails or the model is unavailable
        """
        pass
