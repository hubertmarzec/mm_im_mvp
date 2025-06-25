from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from ..input_management.repositories.request_repository.implementations.mongodb_request_repository import MongoDBRequestRepository
from ..schemas.request_schemas import RequestResponse
from ..services.request_service import RequestService
from ..shared_services.file_storage.implementations.databricks_volume_service import DatabricksVolumeService
from ..shared_services.ml_service.implementations.databricks_endpoint_service import DatabricksEndpointService
from ..shared_services.ocr.implementations.azure_ocr_service import AzureOcrService

requests_routes = APIRouter()


def get_request_repository() -> MongoDBRequestRepository:
    """Dependency injection for RequestRepository"""
    # In a real implementation, you would get these from environment variables
    connection_string = "mongodb://localhost:27017"
    database_name = "email_classification"
    return MongoDBRequestRepository(connection_string, database_name)


def get_ocr_service() -> AzureOcrService:
    """Dependency injection for OcrService"""
    return AzureOcrService()


def get_file_storage() -> DatabricksVolumeService:
    """Dependency injection for FileStorageService"""
    # In a real implementation, you would get these from environment variables
    workspace_url = "https://your-workspace.cloud.databricks.com"
    volume_path = "/Volumes/main/default"
    return DatabricksVolumeService(workspace_url, volume_path)


def get_ml_service() -> DatabricksEndpointService:
    """Dependency injection for MLService"""
    # In a real implementation, you would get this from environment variables
    endpoint_url = "https://your-workspace.cloud.databricks.com/api/2.0/serving-endpoints/your-endpoint/invocations"
    return DatabricksEndpointService(endpoint_url)


def get_request_service(
    request_repository: Annotated[MongoDBRequestRepository, Depends(get_request_repository)],
    ocr_service: Annotated[AzureOcrService, Depends(get_ocr_service)],
    file_storage: Annotated[DatabricksVolumeService, Depends(get_file_storage)],
    ml_service: Annotated[DatabricksEndpointService, Depends(get_ml_service)],
) -> RequestService:
    """Dependency injection for RequestService"""
    return RequestService(request_repository, ocr_service, file_storage, ml_service)


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
    return await request_service.start_classification(file)


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
