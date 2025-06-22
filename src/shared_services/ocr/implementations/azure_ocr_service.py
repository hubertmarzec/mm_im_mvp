import time

from fastapi import UploadFile

from ..exceptions import OcrError
from ..ocr_result import OcrMetadata, OcrResult
from ..ocr_service import OcrService


class AzureOcrService(OcrService):
    """
    Implementation of the OCR service using Azure Cognitive Services.
    """

    async def extract_text_from_file(self, file: UploadFile) -> OcrResult:
        """
        Extract text from an uploaded file using Azure Cognitive Services.

        Args:
            file: FastAPI UploadFile object containing the document

        Returns:
            OcrResult object containing extracted text and metadata

        Raises:
            OcrError: When there are issues with the file or processing fails
        """
        start_time = time.time()

        # Validate file
        if not file.filename:
            raise OcrError("No filename provided", OcrError.MISSING_FILENAME)

        if not file.content_type:
            raise OcrError("No content type provided", OcrError.MISSING_CONTENT_TYPE)

        # Check if file type is supported
        supported_types = ["image/jpeg", "image/png", "image/tiff", "application/pdf"]
        if file.content_type not in supported_types:
            raise OcrError(f"Unsupported file type: {file.content_type}", OcrError.UNSUPPORTED_FILE_TYPE, {"supported_types": supported_types})

        try:
            # Read file content
            content = await file.read()
            file_size = len(content)

            # Mock Azure OCR processing
            processing_time = int((time.time() - start_time) * 1000)

            # Mock Azure Read API response (v4.0+)
            json_response = {
                "status": "succeeded",
                "createdDateTime": "2023-01-01T00:00:00Z",
                "lastUpdatedDateTime": "2023-01-01T00:00:01Z",
                "analyzeResult": {
                    "version": "4.0.0",
                    "readResults": [
                        {
                            "page": 1,
                            "angle": 0.0,
                            "width": 800,
                            "height": 600,
                            "unit": "pixel",
                            "lines": [
                                {
                                    "boundingBox": [0, 0, 100, 0, 100, 50, 0, 50],
                                    "text": "Sample text region",
                                    "words": [
                                        {"boundingBox": [0, 0, 50, 0, 50, 50, 0, 50], "text": "Sample", "confidence": 0.99},
                                        {"boundingBox": [60, 0, 100, 0, 100, 50, 60, 50], "text": "text", "confidence": 0.98},
                                        {"boundingBox": [110, 0, 180, 0, 180, 50, 110, 50], "text": "region", "confidence": 0.97},
                                    ],
                                }
                            ],
                        }
                    ],
                },
            }

            # Create metadata using strict class
            metadata = OcrMetadata(engine="azure_cognitive_services", engine_version="4.0", processing_time_ms=processing_time, filename=file.filename, file_size_bytes=file_size)

            return OcrResult(json=json_response, metadata=metadata)

        except OcrError:
            raise
        except Exception as e:
            raise OcrError(f"Failed to process file: {str(e)}", OcrError.PROCESSING_ERROR, {"original_error": str(e)}) from e
