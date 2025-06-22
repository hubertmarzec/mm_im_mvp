import time
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import UploadFile

from ..exceptions import FileStorageError
from ..file_storage_service import FileStorageService


class DatabricksVolumeService(FileStorageService):
    """
    Mock implementation of the file storage service using Databricks Volume.
    """

    def __init__(self, workspace_url: str = "https://mock-workspace.cloud.databricks.com", volume_path: str = "/Volumes/default/default"):
        """
        Initialize the Databricks Volume service.

        Args:
            workspace_url: Databricks workspace URL
            volume_path: Path to the volume in Databricks
        """
        self.workspace_url = workspace_url
        self.volume_path = volume_path
        self._mock_storage: dict[str, dict[str, Any]] = {}

    async def save(self, file: UploadFile, path: str) -> str:
        """
        Save a file to Databricks Volume.

        Args:
            file: FastAPI UploadFile object containing the file
            path: Destination path in the volume

        Returns:
            str: File ID for the saved file

        Raises:
            FileStorageError: When there are issues with the file or save operation fails
        """
        start_time = time.time()

        # Validate file
        if not file.filename:
            raise FileStorageError("No filename provided", FileStorageError.MISSING_FILENAME)

        if not file.content_type:
            raise FileStorageError("No content type provided", FileStorageError.MISSING_CONTENT_TYPE)

        # Validate path
        if not path or path.startswith("/"):
            raise FileStorageError("Invalid path provided", FileStorageError.INVALID_PATH, {"path": path})

        try:
            # Read file content
            content = await file.read()
            file_size = len(content)

            # Generate unique file ID
            file_id = str(uuid.uuid4())

            # Create full path
            full_path = f"{self.volume_path}/{path.lstrip('/')}"

            # Mock save to Databricks Volume
            save_time = time.time() - start_time

            # Store file metadata and content in mock storage
            self._mock_storage[file_id] = {
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": file_size,
                "path": full_path,
                "save_time": save_time,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "content": content,
                "workspace_url": self.workspace_url,
            }

            return file_id

        except FileStorageError:
            raise
        except Exception as e:
            raise FileStorageError(f"Failed to save file: {str(e)}", FileStorageError.UPLOAD_ERROR, {"original_error": str(e)}) from e
