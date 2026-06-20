from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Smart Grid API",
        "timestamp": datetime.utcnow().isoformat()
    }