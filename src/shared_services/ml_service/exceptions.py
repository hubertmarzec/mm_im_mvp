class MLServiceError(Exception):
    """
    Generic exception for ML service-related errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        details: Additional error details
    """

    # Error codes
    CALL_ERROR = "CALL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    INVALID_INPUT = "INVALID_INPUT"
    TIMEOUT = "TIMEOUT"
    UNAUTHORIZED = "UNAUTHORIZED"

    def __init__(self, message: str, error_code: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        return f"MLServiceError[{self.error_code}]: {self.message}"

    def to_dict(self) -> dict:
        """Convert exception to dictionary format."""
        return {"error_code": self.error_code, "message": self.message, "details": self.details}
