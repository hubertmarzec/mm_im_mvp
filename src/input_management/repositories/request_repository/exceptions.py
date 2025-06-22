class RequestRepositoryError(Exception):
    """
    Generic exception for request repository-related errors.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code
        details: Additional error details
    """

    # Error codes
    CREATE_ERROR = "CREATE_ERROR"
    READ_ERROR = "READ_ERROR"
    UPDATE_ERROR = "UPDATE_ERROR"
    DELETE_ERROR = "DELETE_ERROR"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"

    def __init__(self, message: str, error_code: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        return f"RequestRepositoryError[{self.error_code}]: {self.message}"

    def to_dict(self) -> dict:
        """Convert exception to dictionary format."""
        return {"error_code": self.error_code, "message": self.message, "details": self.details}
