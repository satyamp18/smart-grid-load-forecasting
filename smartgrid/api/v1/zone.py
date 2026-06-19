from fastapi import APIRouter

router = APIRouter()

@router.get("/zones")
def get_zones():
    return {"message": "Zone API Working"}