from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile

from ..exceptions import OcrError
from ..implementations.azure_ocr_service import AzureOcrService
from ..ocr_result import OcrResult


@pytest.mark.unit
@pytest.mark.asyncio
async def test_extract_text_from_file():
    # Arrange
    service = AzureOcrService()

    # Create a mock UploadFile
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read.return_value = b"mock file content"

    # Act
    result = await service.extract_text_from_file(mock_file)

    # Assert
    assert isinstance(result, OcrResult)
    # Check top-level Azure Read API fields
    assert result.json["status"] == "succeeded"
    assert "analyzeResult" in result.json
    analyze_result = result.json["analyzeResult"]
    assert analyze_result["version"] == "4.0.0"
    assert "readResults" in analyze_result
    read_results = analyze_result["readResults"]
    assert isinstance(read_results, list)
    assert len(read_results) == 1
    page = read_results[0]
    assert page["page"] == 1
    assert "lines" in page
    lines = page["lines"]
    assert isinstance(lines, list)
    assert len(lines) == 1
    line = lines[0]
    assert line["text"] == "Sample text region"
    assert "words" in line
    words = line["words"]
    assert [w["text"] for w in words] == ["Sample", "text", "region"]
    assert words[0]["confidence"] == 0.99
    assert words[1]["confidence"] == 0.98
    assert words[2]["confidence"] == 0.97
    # Metadata checks
    assert result.metadata.engine == "azure_cognitive_services"
    assert result.metadata.engine_version == "4.0"
    assert result.metadata.filename == "test.pdf"
    assert result.metadata.file_size_bytes == 17  # length of "mock file content"
    assert result.metadata.processing_time_ms >= 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_extract_text_from_file_missing_filename():
    # Arrange
    service = AzureOcrService()

    # Create a mock UploadFile without filename
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = None
    mock_file.content_type = "application/pdf"

    # Act & Assert
    with pytest.raises(OcrError) as exc_info:
        await service.extract_text_from_file(mock_file)

    assert exc_info.value.error_code == OcrError.MISSING_FILENAME
    assert "No filename provided" in exc_info.value.message


@pytest.mark.unit
@pytest.mark.asyncio
async def test_extract_text_from_file_unsupported_type():
    # Arrange
    service = AzureOcrService()

    # Create a mock UploadFile with unsupported type
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.txt"
    mock_file.content_type = "text/plain"

    # Act & Assert
    with pytest.raises(OcrError) as exc_info:
        await service.extract_text_from_file(mock_file)

    assert exc_info.value.error_code == OcrError.UNSUPPORTED_FILE_TYPE
    assert "Unsupported file type" in exc_info.value.message
    assert "supported_types" in exc_info.value.details


@pytest.mark.unit
def test_ocr_exception_structure():
    # Test the new OcrError structure
    exception = OcrError("Test error message", OcrError.PROCESSING_ERROR, {"test_detail": "value"})

    assert exception.message == "Test error message"
    assert exception.error_code == OcrError.PROCESSING_ERROR
    assert exception.details == {"test_detail": "value"}
    assert str(exception) == "OcrError[PROCESSING_ERROR]: Test error message"

    # Test to_dict method
    exception_dict = exception.to_dict()
    assert exception_dict["error_code"] == OcrError.PROCESSING_ERROR
    assert exception_dict["message"] == "Test error message"
    assert exception_dict["details"] == {"test_detail": "value"}
