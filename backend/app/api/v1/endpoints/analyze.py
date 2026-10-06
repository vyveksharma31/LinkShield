"""URL Analysis API endpoint."""
import time
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from backend.app.schemas.request import AnalyzeRequest
from backend.app.schemas.response import AnalysisResponse
from backend.app.core.logging import logger

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze URL for Phishing & Malicious Indicators",
    description="Performs multi-signal defensive static analysis on a target URL string.",
)
async def analyze_url(payload: AnalyzeRequest) -> AnalysisResponse:
    """Analyze a submitted URL using LinkShield's detection engine."""
    start_time = time.perf_counter()
    logger.info("Received URL analysis request: %s", payload.url)

    try:
        # Import engine coordinator
        from backend.app.engine.analyzer import analyze_url_pipeline
        response = await analyze_url_pipeline(payload.url)
        return response
    except ValueError as val_err:
        logger.warning("Validation error analyzing URL '%s': %s", payload.url, str(val_err))
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(val_err),
        )
    except Exception as exc:
        logger.error("Internal engine error analyzing URL '%s': %s", payload.url, str(exc), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while executing the security analysis engine.",
        )
