from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routes import requests_routes, status_routes
from .dependencies.auth import verify_api_key

app = FastAPI(
    title="Input Management API",
    description="API for managing PC input devices",
    version="1.0.0"
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
app.include_router(
    status_routes.router,
    prefix="/api/v1",
    tags=["status"]
)

# Request routes - require authentication
app.include_router(
    requests_routes.router,
    prefix="/api/v1",
    tags=["input"],
    # dependencies=[Depends(verify_api_key)]
)

@app.on_event("startup")
async def startup_event():
    # Tu można dodać inicjalizację zasobów
    pass

@app.on_event("shutdown")
async def shutdown_event():
    # Tu można dodać czyszczenie zasobów
    pass
