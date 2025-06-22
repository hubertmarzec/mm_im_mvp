from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from ..schemas.request_schemas import RequestResponse
from ..services.request_service import RequestService

requests_routes = APIRouter()


def get_request_service() -> RequestService:
    """Dependency injection for RequestService"""
    return RequestService()


@requests_routes.post("/request", response_model=RequestResponse, status_code=202)
async def create_request(file: Annotated[UploadFile, File(description="TIFF image file to process")], request_service: Annotated[RequestService, Depends(get_request_service)]):
    """
    Create a new request for processing a TIFF image

    Args:
        file: The TIFF image file to process
        request_service: Injected RequestService dependency

    Returns:
        RequestResponse with request details and 202 status code
    """
    return await request_service.create_request(file)


@requests_routes.get("/request/{request_id}", response_model=RequestResponse)
async def get_request(request_id: str, request_service: Annotated[RequestService, Depends(get_request_service)]):
    """
    Get request details by ID

    Args:
        request_id: The unique request identifier
        request_service: Injected RequestService dependency

    Returns:
        RequestResponse with request details
    """
    request = await request_service.get_request(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    return request
