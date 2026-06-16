from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Smart Grid Operations Center",
    version="1.0.0"
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)


@app.get("/")
def root():
    return {
        "message": "Smart Grid API Running"
    }