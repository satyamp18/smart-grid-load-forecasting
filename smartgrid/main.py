from fastapi import FastAPI

import smartgrid.models

from smartgrid.api.v1.health import router as health_router
from smartgrid.core.logging import setup_logging
from smartgrid.db.base import Base
from smartgrid.db.session import engine
import logging

# Logging setup
setup_logging()

# FastAPI App
app = FastAPI(
    title="Smart Grid Operations Center",
    version="1.0.0"
)

# Health Routes
app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)

# Root Route
@app.get("/")
def root():
    return {
        "message": "Smart Grid API Running"
    }


@app.on_event("startup")
def on_startup():
    """Attempt to create DB tables on startup, but don't crash the app if DB is unreachable."""
    # DB initialization can be skipped in development or when DB credentials are
    # not available. Set SKIP_DB_INIT=true in environment to skip automatically.
    import os

    skip = os.getenv("SKIP_DB_INIT", "true").lower() in ("1", "true", "yes")
    if skip:
        logging.getLogger().info("Skipping DB schema creation on startup (SKIP_DB_INIT=%r).", skip)
        return

    try:
        logging.getLogger().info("Ensuring database tables exist...")
        Base.metadata.create_all(bind=engine)
        logging.getLogger().info("Database tables created/verified.")
    except Exception as e:
        # Log the exception but allow the app to start — DB may be temporarily unavailable
        logging.getLogger().exception("Failed to create/verify database tables on startup: %s", e)