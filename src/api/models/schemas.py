from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RequestResponse(BaseModel):
    request_id: str
    status: str = Field(..., description="Status of request (pending, completed, failed)")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None

class RequestList(BaseModel):
    requests: list[RequestResponse]
    total: int
