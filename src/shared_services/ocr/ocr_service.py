from abc import ABC, abstractmethod

from fastapi import UploadFile

from .ocr_result import OcrResult


class OcrService(ABC):
    """
    Interface for OCR (Optical Character Recognition) services.
    """

    @abstractmethod
    async def extract_text_from_file(self, file: UploadFile) -> OcrResult:
        """
        Extract text from an uploaded file.

        Args:
            file: FastAPI UploadFile object containing the document

        Returns:
            OcrResult object containing extracted text and metadata

        Raises:
            OcrError: When there are issues with the file or processing fails
        """
        pass
