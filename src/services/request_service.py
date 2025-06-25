import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, UploadFile

from ..input_management.repositories.request_repository.request_repository import RequestRepository
from ..models import Request
from ..schemas.request_schemas import RequestResponse
from ..shared_services.file_storage.file_storage_service import FileStorageService
from ..shared_services.ml_service.ml_service import MLService
from ..shared_services.ocr.ocr_service import OcrService


class RequestService:
    """Service for handling request business logic"""

    def __init__(
        self,
        request_repository: RequestRepository,
        ocr_service: OcrService,
        file_storage: FileStorageService,
        ml_service: MLService,
    ):
        """
        Initialize RequestService with dependencies

        Args:
            request_repository: Repository for request persistence
            ocr_service: Service for OCR processing
            file_storage: Service for file storage operations
            ml_service: Service for ML model calls
        """
        self.request_repository = request_repository
        self.ocr_service = ocr_service
        self.file_storage = file_storage
        self.ml_service = ml_service

    def _validate_file(self, file: UploadFile) -> None:
        """
        Validate uploaded file for classification

        Args:
            file: The uploaded file to validate

        Raises:
            HTTPException: If file validation fails
        """
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/tiff"):
            raise HTTPException(status_code=400, detail="Only TIFF images are supported")

        # Validate file size (optional - adjust as needed)
        if file.size and file.size > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=400, detail="File size exceeds maximum allowed size of 10MB")

    async def start_classification(self, file: UploadFile) -> RequestResponse:
        """
        Start classification process for a TIFF image

        Args:
            file: The uploaded TIFF file

        Returns:
            RequestResponse with request details

        Raises:
            HTTPException: If file validation fails or processing errors occur
        """
        # Validate file
        self._validate_file(file)

        # Generate unique request ID
        request_id = str(uuid.uuid4())
        now = datetime.now()
        request = None

        try:
            # 1. Create initial Request entity with initial status and persist
            request = Request(
                id=request_id,
                status="processing",
                created_at=now,
                updated_at=now,
            )
            request = await self.request_repository.create(request)

            # 2. OCR uploaded file
            request.update_status("ocr_processing")
            await self.request_repository.update(request)

            ocr_result = await self.ocr_service.extract_text_from_file(file)

            # 3. Update status of Request entity
            request.update_status("ml_processing")
            await self.request_repository.update(request)

            # 4. Call ML model
            ml_result = await self.ml_service.call(ocr_result.json)

            # 5. Update status of Request entity
            request.update_status("storing_results")
            await self.request_repository.update(request)

            # 6. Store uploaded file, OCR result, result from ML Model with FileStorage
            file_path = await self.file_storage.save(file, f"uploads/{request_id}", file.filename)

            ocr_result_path = await self.file_storage.saveFromDict(ocr_result.json, f"results/{request_id}", f"{request_id}_ocr_result.json")

            ml_result_path = await self.file_storage.saveFromDict(ml_result, f"results/{request_id}", f"{request_id}_ml_result.json")

            # 7. Update request entity status
            request.file_path = file_path
            request.ocr_result_path = ocr_result_path
            request.ml_result_path = ml_result_path
            request.complete({"classification": ml_result, "ocr_text": ocr_result.json})

            await self.request_repository.update(request)

            # 8. Return request entity
            return RequestResponse(
                request_id=request.id,
                status=request.status,
                created_at=request.created_at,
                completed_at=request.completed_at,
                result=request.result,
            )

        except Exception as e:
            # Handle errors and update request status
            if request:
                request.fail(str(e))
                await self.request_repository.update(request)

            raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")

    async def get_request(self, request_id: str) -> Optional[RequestResponse]:
        """
        Get request details by ID

        Args:
            request_id: The unique request identifier

        Returns:
            RequestResponse if found, None otherwise
        """
        request = await self.request_repository.get_by_id(request_id)
        if not request:
            return None

        return RequestResponse(
            request_id=request.id,
            status=request.status,
            created_at=request.created_at,
            completed_at=request.completed_at,
            result=request.result,
        )
