from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.models.meter import SmartMeter
from smartgrid.schemas.meter import MeterCreate, MeterResponse
from smartgrid.services.meter_service import MeterService

router = APIRouter()

service = MeterService()


<<<<<<< HEAD
@router.get("/meters", response_model=list[MeterResponse])
=======
@router.get(
    "/meters",
    response_model=list[MeterResponse],
    summary="Get All Meters",
    description="Returns all smart meters."
)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
def get_all_meters(db: Session = Depends(get_db)):
    return service.get_all_meters(db)


<<<<<<< HEAD
@router.get("/meters/{meter_id}", response_model=MeterResponse)
def get_meter(meter_id: int, db: Session = Depends(get_db)):

=======
@router.get(
    "/meters/{meter_id}",
    response_model=MeterResponse,
    summary="Get Meter",
    description="Returns a smart meter by ID."
)
def get_meter(
    meter_id: int,
    db: Session = Depends(get_db),
):
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
    meter = service.get_meter(db, meter_id)

    if meter is None:
        raise HTTPException(
            status_code=404,
            detail="Meter not found"
        )

    return meter


<<<<<<< HEAD
@router.post("/meters", response_model=MeterResponse)
=======
@router.post(
    "/meters",
    response_model=MeterResponse,
    summary="Create Meter",
    description="Creates a new smart meter."
)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
def create_meter(
    meter: MeterCreate,
    db: Session = Depends(get_db),
):
<<<<<<< HEAD

=======
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
    new_meter = SmartMeter(
        meter_code=meter.meter_code,
        zone_id=meter.zone_id,
    )

    return service.create_meter(db, new_meter)


<<<<<<< HEAD
@router.delete("/meters/{meter_id}")
=======
@router.delete(
    "/meters/{meter_id}",
    summary="Delete Meter",
    description="Deletes a smart meter."
)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
def delete_meter(
    meter_id: int,
    db: Session = Depends(get_db),
):
<<<<<<< HEAD

    deleted = service.delete_meter(
        db,
        meter_id,
    )
=======
    deleted = service.delete_meter(db, meter_id)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e

    if deleted is None:
        raise HTTPException(
            status_code=404,
<<<<<<< HEAD
            detail="Meter not found",
=======
            detail="Meter not found"
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
        )

    return {
        "message": "Meter deleted successfully"
    }