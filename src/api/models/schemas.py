from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InputResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MouseMoveRequest(BaseModel):
    x: int = Field(..., ge=0, le=65535, description="X coordinate")
    y: int = Field(..., ge=0, le=65535, description="Y coordinate")

class MouseClickRequest(BaseModel):
    button: int = Field(..., ge=1, le=3, description="Mouse button (1-left, 2-middle, 3-right)")
    double_click: bool = Field(default=False, description="Perform double click")

class KeyboardRequest(BaseModel):
    key_code: int = Field(..., ge=0, le=255, description="Key code")
    pressed: bool = Field(default=True, description="Key press state")
    modifiers: Optional[list[str]] = Field(default=None, description="Key modifiers (ctrl, alt, shift)")

class RequestCreate(BaseModel):
    type: str = Field(..., description="Type of request (mouse_move, mouse_click, keyboard_key)")
    params: dict = Field(..., description="Parameters for the request")

class RequestResponse(BaseModel):
    request_id: str
    status: str = Field(..., description="Status of request (pending, completed, failed)")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None

class RequestList(BaseModel):
    requests: list[RequestResponse]
    total: int
