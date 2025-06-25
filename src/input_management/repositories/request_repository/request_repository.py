from abc import ABC, abstractmethod
from typing import Optional

from src.models import Request


class RequestRepository(ABC):
    """
    Interface for request repository operations.
    """

    @abstractmethod
    async def create(self, request: Request) -> Request:
        """
        Create a new request record.

        Args:
            request: Request entity to create

        Returns:
            Request: The created request entity

        Raises:
            RequestRepositoryError: When database operation fails
        """
        pass

    @abstractmethod
    async def get_by_id(self, request_id: str) -> Optional[Request]:
        """
        Retrieve a request by its ID.

        Args:
            request_id: The ID of the request to retrieve

        Returns:
            Request | None: The request entity or None if not found

        Raises:
            RequestRepositoryError: When database operation fails
        """
        pass

    @abstractmethod
    async def update(self, request: Request) -> bool:
        """
        Update an existing request.

        Args:
            request: Request entity to update

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
