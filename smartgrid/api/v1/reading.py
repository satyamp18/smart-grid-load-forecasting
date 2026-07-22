from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.models.reading import MeterReading
from smartgrid.schemas.reading import (
    ReadingCreate,
    ReadingUpdate,
    ReadingResponse,
)
from smartgrid.services.reading_service import ReadingService

router = APIRouter()

service = ReadingService()


@router.get(
    "/readings",
    response_model=list[ReadingResponse],
)
def get_all_readings(
    db: Session = Depends(get_db),
):
    return service.get_all_readings(db)


@router.get(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
)
def get_reading(
    reading_id: int,
    db: Session = Depends(get_db),
):

    reading = service.get_reading(
        db,
        reading_id,
    )

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="Reading not found",
        )

    return reading


@router.post(
    "/readings",
    response_model=ReadingResponse,
)
def create_reading(
    reading: ReadingCreate,
    db: Session = Depends(get_db),
):

    new_reading = MeterReading(
        meter_id=reading.meter_id,
        voltage=reading.voltage,
        current=reading.current,
        timestamp=reading.timestamp,
    )

    return service.create_reading(
        db,
        new_reading,
    )

@router.put(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
)
def update_reading(
    reading_id: int,
    reading: ReadingUpdate,
    db: Session = Depends(get_db),
):

    updated = service.update_reading(
        db,
        reading_id,
        reading,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Reading not found",
        )

    return updated


@router.delete("/readings/{reading_id}")
def delete_reading(
    reading_id: int,
    db: Session = Depends(get_db),
):

    deleted = service.delete_reading(
        db,
        reading_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Reading not found",
        )

    return {
        "message": "Reading deleted successfully"
    }