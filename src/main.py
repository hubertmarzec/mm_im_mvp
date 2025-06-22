from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.requests_routes import requests_routes
from .api.status_routes import status_routes

app = FastAPI(
    title="Input Management API",
    description="API for managing PC input devices",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Status routes - no auth required
app.include_router(status_routes, prefix="/api/v1", tags=["status"])

# Request routes - require authentication
app.include_router(requests_routes, prefix="/api/v1", tags=["input"])
