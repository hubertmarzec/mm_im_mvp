class OcrError(Exception):
    """
    Generic exception for OCR-related errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        details: Additional error details
    """

    # Error codes
    PROCESSING_ERROR = "PROCESSING_ERROR"
    FILE_ERROR = "FILE_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    MISSING_FILENAME = "MISSING_FILENAME"
    MISSING_CONTENT_TYPE = "MISSING_CONTENT_TYPE"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"

    def __init__(self, message: str, error_code: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        return f"OcrError[{self.error_code}]: {self.message}"

    def to_dict(self) -> dict:
        """Convert exception to dictionary format."""
        return {"error_code": self.error_code, "message": self.message, "details": self.details}
