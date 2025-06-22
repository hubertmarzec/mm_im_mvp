from abc import ABC, abstractmethod

from fastapi import UploadFile


class FileStorageService(ABC):
    """
    Interface for file storage services.
    """

    @abstractmethod
    async def save(self, file: UploadFile, path: str) -> str:
        """
        Save a file to storage.

        Args:
            file: FastAPI UploadFile object containing the file
            path: Destination path in storage

        Returns:
            str: URL or identifier of the saved file

        Raises:
            FileStorageError: When there are issues with the file or save operation fails
        """
        pass
