from dataclasses import dataclass
from typing import Any


@dataclass
class OcrMetadata:
    """
    Strict metadata structure for OCR processing results.
    """

    engine: str
    engine_version: str
    processing_time_ms: int
    filename: str
    file_size_bytes: int

    def to_dict(self) -> dict:
        """Convert metadata to dictionary format."""
        return {"engine": self.engine, "engine_version": self.engine_version, "processing_time_ms": self.processing_time_ms, "filename": self.filename, "file_size_bytes": self.file_size_bytes}


@dataclass
class OcrResult:
    """
    Data Transfer Object for OCR processing results.

    Attributes:
        json: Raw response from the OCR engine (generic format)
        metadata: Processing metadata with strict structure
    """

    json: dict[str, Any]
    metadata: OcrMetadata
