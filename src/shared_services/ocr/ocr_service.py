from abc import ABC, abstractmethod


class OcrService(ABC):
    """
    Simple interface for OCR (Optical Character Recognition) services.
    """

    @abstractmethod
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from a file.

        Args:
            file_path: Path to the document file

        Returns:
            Extracted text as string
        """
        pass
