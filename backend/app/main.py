"""LinkShield FastAPI Application Entrypoint."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context for pre-warming models and resources."""
    logger.info("Initializing %s v%s in %s mode...", settings.PROJECT_NAME, settings.VERSION, settings.ENVIRONMENT)

    # Attempt to load ML model in memory at startup
    try:
        from backend.app.ml.model_loader import get_model_loader
        loader = get_model_loader()
        if loader.is_loaded:
            logger.info("Machine learning model initialized successfully.")
        else:
            logger.warning("ML model could not be loaded on startup. Heuristic engine active.")
    except Exception as exc:
        logger.warning("ML model could not be loaded on startup (%s). Heuristic engine active.", str(exc))

    yield

    logger.info("Shutting down %s...", settings.PROJECT_NAME)


app = FastAPI(
    title=f"{settings.PROJECT_NAME} — Phishing URL Detection & Risk Analysis",
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Request Size Limit Middleware (Anti-DoS / Payload Limit: 64 KB)
MAX_REQUEST_BYTES = 64 * 1024


@app.middleware("http")
async def limit_request_size_middleware(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > MAX_REQUEST_BYTES:
        return JSONResponse(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            content={"detail": "Payload too large. LinkShield limits requests to 64KB."},
        )
    return await call_next(request)


# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Ensure raw tracebacks are never exposed to clients."""
    logger.error("Unhandled server exception at %s: %s", request.url.path, str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred during security analysis. Please verify your request or consult logs.",
        },
    )


# Root information endpoint
@app.get("/", tags=["Root"])
async def root_info() -> dict:
    """Return top-level API metadata and documentation links."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "status": "online",
        "documentation": "/docs",
        "health_check": f"{settings.API_V1_STR}/health",
    }


# Register versioned API routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR)
