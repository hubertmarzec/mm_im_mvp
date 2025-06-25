from abc import ABC, abstractmethod
from typing import Any

from fastapi import UploadFile


class FileStorageService(ABC):
    """
    Interface for file storage services.
    """

    @abstractmethod
    async def save(self, file: UploadFile, path: str, filename: str) -> str:
        """
        Save a file to storage.

        Args:
            file: FastAPI UploadFile object containing the file
            path: Destination path in storage
            filename: Name to use for the saved file

        Returns:
            str: URL or identifier of the saved file

        Raises:
            FileStorageError: When there are issues with the file or save operation fails
        """
        pass

    @abstractmethod
    async def saveFromDict(self, data: dict[str, Any], path: str, filename: str) -> str:
        """
        Save a dictionary as JSON file to storage.

        Args:
            data: Dictionary to save as JSON
            path: Destination path in storage
            filename: Name to use for the saved file

        Returns:
            str: URL or identifier of the saved file

        Raises:
            FileStorageError: When there are issues with the file or save operation fails
        """
        pass
