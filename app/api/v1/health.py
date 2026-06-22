from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Smart Grid API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }