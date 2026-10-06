"""Health and diagnostic endpoint."""
from datetime import datetime, timezone
from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.schemas.response import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="API Health Check")
async def health_check() -> HealthResponse:
    """Return backend operational status, version, and model readiness."""
    # Check if model is initialized (we will import the loader check once implemented)
    model_loaded = False
    try:
        from backend.app.ml.model_loader import model_loader
        model_loaded = model_loader.is_loaded()
    except (ImportError, Exception):
        model_loaded = False

    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        model_loaded=model_loaded,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
