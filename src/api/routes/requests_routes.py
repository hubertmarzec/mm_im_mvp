from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    RequestCreate,
    RequestResponse,
    RequestList
)
from typing import Dict
from datetime import datetime
import uuid

router = APIRouter()

    
@router.get("/request/{request_id}", response_model=RequestResponse)
async def get_request(request_id: str):
    
    return RequestResponse(
        request_id=request_id,
        status="pending",
        result=None
    )

@router.get("/request", response_model=RequestList)
async def list_requests():
    requests = list(requests_store.values())
    return RequestList(
        requests=requests,
        total=len(requests)
    )
