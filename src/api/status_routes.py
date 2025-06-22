from datetime import datetime

from fastapi import APIRouter

status_routes = APIRouter()


@status_routes.get("/healthcheck")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "input-management-api",
    }
