from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class Request:
    """
    Domain entity representing a classification request.
    """

    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[dict[str, Any]] = None
    file_path: Optional[str] = None
    ocr_result_path: Optional[str] = None
    ml_result_path: Optional[str] = None

    def update_status(self, status: str) -> None:
        """Update the status of the request"""
        self.status = status
        self.updated_at = datetime.now()

    def complete(self, result: dict[str, Any]) -> None:
        """Mark the request as completed with results"""
        self.status = "completed"
        self.result = result
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

    def fail(self, error_message: str) -> None:
        """Mark the request as failed"""
        self.status = "failed"
        self.result = {"error": error_message}
        self.updated_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """Convert entity to dictionary for persistence"""
        return {
            "id": self.id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "result": self.result,
            "file_path": self.file_path,
            "ocr_result_path": self.ocr_result_path,
            "ml_result_path": self.ml_result_path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Request":
        """Create entity from dictionary"""
        return cls(
            id=data["id"],
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            completed_at=data.get("completed_at"),
            result=data.get("result"),
            file_path=data.get("file_path"),
            ocr_result_path=data.get("ocr_result_path"),
            ml_result_path=data.get("ml_result_path"),
        )
