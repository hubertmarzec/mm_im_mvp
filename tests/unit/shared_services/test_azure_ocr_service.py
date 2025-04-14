import pytest
from src.shared_services.implementations.azure_ocr_service import AzureOcrService


def test_extract_text_from_file():
    # Arrange
    service = AzureOcrService()
    file_path = "dummy_path.pdf"
    
    # Act
    result = service.extract_text_from_file(file_path)
    
    # Assert
    assert result == "azure ocr;)" 