"""API v1 router composition."""
from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, analyze

api_v1_router = APIRouter()

api_v1_router.include_router(health.router, tags=["Diagnostics"])
api_v1_router.include_router(analyze.router, tags=["Detection Engine"])
