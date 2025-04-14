from ..ocr_service import OcrService


class AzureOcrService(OcrService):
    """
    Mock implementation of the OCR service using Azure Cognitive Services.
    """
    
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Mock implementation of text extraction from a file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Static string as a mock response
        """
        
        # Return static string as a mock response
        return "azure ocr;)" 