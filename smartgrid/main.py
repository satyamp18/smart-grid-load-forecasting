from fastapi import FastAPI

import smartgrid.models

from smartgrid.api.v1.zone import router as zone_router
from smartgrid.api.v1.health import router as health_router
from smartgrid.core.logging import setup_logging
from smartgrid.db.base import Base
from smartgrid.db.session import engine
from smartgrid.core.config import settings
from smartgrid.api.v1.meter import router as meter_router
from smartgrid.api.v1.reading import router as reading_router
from smartgrid.api.v1.analytics import router as analytics_router
from smartgrid.api.v1.alert import router as alert_router
from smartgrid.api.v1.load_report import (
    router as load_report_router,
)
import logging
# from smartgrid.api.v1.dashboard import router as dashboard_router


# module logger
logger = logging.getLogger(__name__)

# Logging setup
setup_logging()

# FastAPI App
app = FastAPI(
    title="Smart Grid Operations Center",
    version="1.0.0"
)

# Health Routes
app.include_router(
    zone_router,
    prefix="/api/v1",
    tags=["Zone"]
)

app.include_router(
    meter_router,
    prefix="/api/v1",
    tags=["Meter"]
)
app.include_router(
    reading_router,
    prefix="/api/v1",
    tags=["Reading"],
)
app.include_router(
    analytics_router,
    prefix="/api/v1",
    tags=["Analytics"],
)
app.include_router(
    alert_router,
    prefix="/api/v1",
    tags=["Alert"],
)
app.include_router(
    load_report_router,
    prefix="/api/v1",
    tags=["Load Report"],
)
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)
# app.include_router(
#     dashboard_router,
#     prefix="/api/v1",
#     tags=["Dashboard"]
# )

# Root Route
@app.get("/")
def root():
    return {
        "message": "Smart Grid API Running"
    }


@app.on_event("startup")
async def on_startup():
    """Attempt to create DB tables on startup, but don't crash the app if DB is unreachable."""
    # DB initialization can be skipped in development or when DB credentials are
    # not available. Set SKIP_DB_INIT=true in environment to skip automatically.
    import os
    # Prefer an explicit setting if provided by pydantic settings, else fallback to env var
    if hasattr(settings, "SKIP_DB_INIT"):
        skip = bool(getattr(settings, "SKIP_DB_INIT"))
    else:
        skip = os.getenv("SKIP_DB_INIT", "true").lower() in ("1", "true", "yes")

    if skip:
        logger.info("Skipping DB schema creation on startup (SKIP_DB_INIT=%r).", skip)
        return

    try:
        logger.info("Ensuring database tables exist...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified.")
    except Exception as e:
        # Log the exception but allow the app to start — DB may be temporarily unavailable
        logger.exception("Failed to create/verify database tables on startup: %s", e)