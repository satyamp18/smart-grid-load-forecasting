from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.services.analytics_service import AnalyticsService

router = APIRouter()

service = AnalyticsService()


@router.get("/analytics/current-load/{zone_id}")
def get_current_load(
    zone_id: int,
    db: Session = Depends(get_db),
):

    load = service.get_zone_current_load(
        db,
        zone_id,
    )

    return {
        "zone_id": zone_id,
        "current_load_kw": load,
    }


@router.get("/analytics/peak-load/{zone_id}")
def get_peak_load(
    zone_id: int,
    db: Session = Depends(get_db),
):

    peak = service.get_peak_load(
        db,
        zone_id,
    )

    return {
        "zone_id": zone_id,
        "peak_load_kw": peak,
    }


@router.get("/analytics/average-load/{zone_id}")
def get_average_load(
    zone_id: int,
    db: Session = Depends(get_db),
):

    average = service.get_average_load(
        db,
        zone_id,
    )

    return {
        "zone_id": zone_id,
        "average_load_kw": average,
    }


@router.get("/analytics/history/{zone_id}")
def get_history(
    zone_id: int,
    db: Session = Depends(get_db),
):

    history = service.get_zone_history(
        db,
        zone_id,
    )

    return history