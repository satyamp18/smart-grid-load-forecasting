import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import smartgrid.models

from smartgrid.api.v1.alert import router as alert_router
from smartgrid.api.v1.analytics import router as analytics_router
from smartgrid.api.v1.dashboard import router as dashboard_router
from smartgrid.api.v1.health import router as health_router
from smartgrid.api.v1.load_report import router as load_report_router
from smartgrid.api.v1.meter import router as meter_router
from smartgrid.api.v1.reading import router as reading_router
from smartgrid.api.v1.zone import router as zone_router
from smartgrid.api.v1.views import router as views_router
from smartgrid.core.config import settings
from smartgrid.core.logging import setup_logging
from smartgrid.db.base import Base
from smartgrid.db.session import engine
from smartgrid.websocket.alert_socket import router as websocket_router

setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    skip = (
        getattr(settings, "SKIP_DB_INIT", False)
        or os.getenv("SKIP_DB_INIT", "false").lower()
        in ("1", "true", "yes")
    )

    if skip:
        logger.info("Skipping database initialization.")
    else:
        try:
            logger.info("Checking database schema...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database ready.")
        except Exception:
            logger.exception("Database initialization failed.")
    yield


app = FastAPI(
    title="Smart Grid Operations Center",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# -------------------------------
# Static Files & Template Views
# -------------------------------

STATIC_DIR = Path(__file__).resolve().parent.parent / "app" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    logger.warning("Static directory does not exist: %s", STATIC_DIR)

# -------------------------------
# CORS
# -------------------------------

frontend_url = getattr(settings, "FRONTEND_URL", None) or os.getenv("FRONTEND_URL", "")

origins = []
if frontend_url:
    origins = [url.strip().rstrip("/") for url in frontend_url.split(",") if url.strip()]

if not origins:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True if "*" not in origins else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# API Routers
# -------------------------------

app.include_router(zone_router, prefix="/api/v1", tags=["Zone"])
app.include_router(meter_router, prefix="/api/v1", tags=["Meter"])
app.include_router(reading_router, prefix="/api/v1", tags=["Reading"])
app.include_router(analytics_router, prefix="/api/v1", tags=["Analytics"])
app.include_router(alert_router, prefix="/api/v1", tags=["Alert"])
app.include_router(load_report_router, prefix="/api/v1", tags=["Load Report"])
app.include_router(health_router, prefix="/api/v1", tags=["Health"])
app.include_router(dashboard_router, prefix="/api/v1", tags=["Dashboard"])

# Template View Routers (/, /zones, /meters, /readings, /analytics, /reports, /alerts)
app.include_router(views_router)

# WebSocket
app.include_router(websocket_router)