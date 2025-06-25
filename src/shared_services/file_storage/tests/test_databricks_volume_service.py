from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile

from ..exceptions import FileStorageError
from ..implementations.databricks_volume_service import DatabricksVolumeService


class TestDatabricksVolumeService:
    """Test cases for DatabricksVolumeService."""

    @pytest.fixture
    def storage_service(self):
        """Create a DatabricksVolumeService instance for testing."""
        return DatabricksVolumeService()

    @pytest.fixture
    def sample_file(self):
        """Create a sample file for testing."""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "test.txt"
        mock_file.content_type = "text/plain"
        mock_file.read.return_value = b"Test file content"
        return mock_file

    @pytest.fixture
    def sample_dict(self):
        """Create a sample dictionary for testing."""
        return {"key": "value", "number": 42, "nested": {"data": "test"}}

    @pytest.mark.asyncio
    async def test_save_file_success(self, storage_service, sample_file):
        """Test successful file save."""
        file_id = await storage_service.save(sample_file, "test/path", "test.txt")

        assert file_id is not None
        assert len(file_id) > 0

    @pytest.mark.asyncio
    async def test_save_file_missing_filename(self, storage_service):
        """Test save with missing filename."""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "test.txt"
        mock_file.content_type = "text/plain"
        mock_file.read.return_value = b"content"

        with pytest.raises(FileStorageError) as exc_info:
            await storage_service.save(mock_file, "test/path", "")

        assert exc_info.value.error_code == FileStorageError.MISSING_FILENAME

    @pytest.mark.asyncio
    async def test_save_file_missing_content_type(self, storage_service):
        """Test save with missing content type."""
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "test.txt"
        mock_file.content_type = ""
        mock_file.read.return_value = b"content"

        with pytest.raises(FileStorageError) as exc_info:
            await storage_service.save(mock_file, "test/path", "test.txt")

        assert exc_info.value.error_code == FileStorageError.MISSING_CONTENT_TYPE

    @pytest.mark.asyncio
    async def test_save_file_invalid_path(self, storage_service, sample_file):
        """Test save with invalid path."""
        with pytest.raises(FileStorageError) as exc_info:
            await storage_service.save(sample_file, "/invalid/path", "test.txt")

        assert exc_info.value.error_code == FileStorageError.INVALID_PATH

    @pytest.mark.asyncio
    async def test_save_file_stores_metadata(self, storage_service, sample_file):
        """Test that file metadata is properly stored."""
        file_id = await storage_service.save(sample_file, "test/path", "test.txt")

        # Access internal storage to verify metadata
        file_data = storage_service._mock_storage[file_id]

        assert file_data["filename"] == "test.txt"
        assert file_data["content_type"] == "text/plain"
        assert file_data["file_size"] == 17  # "Test file content" length
        assert "test/path" in file_data["path"]
        assert "save_time" in file_data
        assert "created_at" in file_data
        assert "content" in file_data

    @pytest.mark.asyncio
    async def test_saveFromDict_success(self, storage_service, sample_dict):
        """Test successful dictionary save as JSON."""
        file_id = await storage_service.saveFromDict(sample_dict, "test/path", "test.json")

        assert file_id is not None
        assert len(file_id) > 0

    @pytest.mark.asyncio
    async def test_saveFromDict_missing_filename(self, storage_service, sample_dict):
        """Test saveFromDict with missing filename."""
        with pytest.raises(FileStorageError) as exc_info:
            await storage_service.saveFromDict(sample_dict, "test/path", "")

        assert exc_info.value.error_code == FileStorageError.MISSING_FILENAME

    @pytest.mark.asyncio
    async def test_saveFromDict_invalid_path(self, storage_service, sample_dict):
        """Test saveFromDict with invalid path."""
        with pytest.raises(FileStorageError) as exc_info:
            await storage_service.saveFromDict(sample_dict, "/invalid/path", "test.json")

        assert exc_info.value.error_code == FileStorageError.INVALID_PATH

    @pytest.mark.asyncio
    async def test_saveFromDict_stores_metadata(self, storage_service, sample_dict):
        """Test that dictionary metadata is properly stored."""
        file_id = await storage_service.saveFromDict(sample_dict, "test/path", "test.json")

        # Access internal storage to verify metadata
        file_data = storage_service._mock_storage[file_id]

        assert file_data["filename"] == "test.json"
        assert file_data["content_type"] == "application/json"
        assert file_data["file_size"] > 0
        assert "test/path" in file_data["path"]
        assert "save_time" in file_data
        assert "created_at" in file_data
        assert "content" in file_data

        # Verify content is valid JSON
        import json

        content = file_data["content"].decode("utf-8")
        parsed_content = json.loads(content)
        assert parsed_content == sample_dict
