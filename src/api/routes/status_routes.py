from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/healthcheck")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "input-management-api"
    }

@router.get("/version")
async def version():
    return {
        "version": "1.0.0",
        "api_version": "v1"
    }
