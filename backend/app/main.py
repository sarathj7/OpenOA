from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers.auth import router as auth_router
from .routers.analysis import router as analysis_router
from .routers.geospatial import router as geospatial_router
from .routers.metrics import router as metrics_router
from .routers.turbines import router as turbines_router


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(title="OpenOA Wind Farm Analytics API", version="0.1.0")

    # ------------------------------------------------------------------
    # FIXED CORS CONFIGURATION
    # ------------------------------------------------------------------
    # Instead of relying on environment variables (which are failing on Render),
    # we explicitly allow all origins for this test deployment.
    # This guarantees frontend login will work.

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],        # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],        # Allow all HTTP methods
        allow_headers=["*"],        # Allow all headers
    )

    # Include API routers
    app.include_router(metrics_router, prefix=settings.api_v1_prefix)
    app.include_router(turbines_router, prefix=settings.api_v1_prefix)
    app.include_router(analysis_router, prefix=settings.api_v1_prefix)
    app.include_router(geospatial_router, prefix=settings.api_v1_prefix)
    app.include_router(auth_router, prefix=settings.api_v1_prefix)

    @app.get("/health", tags=["system"])
    async def health_check():
        return {
            "status": "ok",
            "message": "CORS is globally enabled (test mode)"
        }

    return app


app = create_app()
