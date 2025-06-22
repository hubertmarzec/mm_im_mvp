from abc import ABC, abstractmethod
from typing import Any


class RequestRepository(ABC):
    """
    Interface for request repository operations.
    """

    @abstractmethod
    async def create(self, request_data: dict[str, Any]) -> str:
        """
        Create a new request record.

        Args:
            request_data: Dictionary containing request data

        Returns:
            str: The ID of the created request

        Raises:
            RequestRepositoryError: When database operation fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, request_id: str) -> dict[str, Any] | None:
        """
        Retrieve a request by its ID.

        Args:
            request_id: The ID of the request to retrieve

        Returns:
            dict[str, Any] | None: The request data or None if not found

        Raises:
            RequestRepositoryError: When database operation fails
        """
        pass

    @abstractmethod
    async def update(self, request_id: str, update_data: dict[str, Any]) -> bool:
        """
        Update an existing request.

        Args:
            request_id: The ID of the request to update
            update_data: Dictionary containing fields to update

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            RequestRepositoryError: When database operation fails
        """
        pass

    @abstractmethod
    async def exists(self, request_id: str) -> bool:
        """
        Check if a request exists.

        Args:
            request_id: The ID of the request to check

        Returns:
            bool: True if request exists, False otherwise

        Raises:
            RequestRepositoryError: When database operation fails
        """
        pass
