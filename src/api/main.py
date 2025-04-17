from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import requests_routes, status_routes
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: inicjalizacja zasobów
    yield
    # Shutdown: czyszczenie zasobów
    pass

app = FastAPI(
    title="Input Management API",
    description="API for managing PC input devices",
    version="1.0.0",
    lifespan=lifespan
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
