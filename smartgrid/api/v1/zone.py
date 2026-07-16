from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.models.zone import Zone
from smartgrid.schemas.zone import ZoneCreate, ZoneResponse
from smartgrid.services.zone_service import ZoneService

router = APIRouter()

service = ZoneService()


@router.get("/zones", response_model=list[ZoneResponse])
def get_all_zones(db: Session = Depends(get_db)):
    return service.get_all_zones(db)


@router.get("/zones/{zone_id}", response_model=ZoneResponse)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    zone = service.get_zone(db, zone_id)

    if zone is None:
        raise HTTPException(
            status_code=404,
            detail="Zone not found"
        )

    return zone


<<<<<<< HEAD
@router.post("/zones", response_model=ZoneResponse)
=======
@router.post(
    "/zones",
    response_model=ZoneResponse,
    summary="Create Zone",
    description="Creates a new smart grid zone."
)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
def create_zone(
    zone: ZoneCreate,
    db: Session = Depends(get_db),
):
    new_zone = Zone(
        zone_name=zone.zone_name,
        max_capacity_kw=zone.max_capacity_kw,
    )

    return service.create_zone(db, new_zone)


@router.put("/zones/{zone_id}", response_model=ZoneResponse)
def update_zone(
    zone_id: int,
    zone: ZoneCreate,
    db: Session = Depends(get_db),
):
    updated_zone = service.update_zone(
        db,
        zone_id,
        zone,
    )

    if updated_zone is None:
        raise HTTPException(
            status_code=404,
            detail="Zone not found"
        )

    return updated_zone


@router.delete("/zones/{zone_id}")
def delete_zone(
    zone_id: int,
    db: Session = Depends(get_db),
):
    deleted_zone = service.delete_zone(
        db,
        zone_id,
    )

    if deleted_zone is None:
        raise HTTPException(
            status_code=404,
            detail="Zone not found"
        )

    return {
        "message": "Zone deleted successfully"
    }