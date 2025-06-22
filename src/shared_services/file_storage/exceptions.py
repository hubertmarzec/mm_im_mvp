class FileStorageError(Exception):
    """
    Generic exception for file storage-related errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        details: Additional error details
    """

    # Error codes
    UPLOAD_ERROR = "UPLOAD_ERROR"
    DOWNLOAD_ERROR = "DOWNLOAD_ERROR"
    DELETE_ERROR = "DELETE_ERROR"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    MISSING_FILENAME = "MISSING_FILENAME"
    MISSING_CONTENT_TYPE = "MISSING_CONTENT_TYPE"
    INVALID_PATH = "INVALID_PATH"
    STORAGE_QUOTA_EXCEEDED = "STORAGE_QUOTA_EXCEEDED"
    PERMISSION_DENIED = "PERMISSION_DENIED"

    def __init__(self, message: str, error_code: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        return f"FileStorageError[{self.error_code}]: {self.message}"

    def to_dict(self) -> dict:
        """Convert exception to dictionary format."""
        return {"error_code": self.error_code, "message": self.message, "details": self.details}
