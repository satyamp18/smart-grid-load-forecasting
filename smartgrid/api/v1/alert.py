from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.models.alert import Alert
from smartgrid.schemas.alert import (
    AlertCreate,
    AlertUpdate,
    AlertResponse,
)
from smartgrid.services.alert_service import AlertService

router = APIRouter()

service = AlertService()


# -----------------------------
# Get All Alerts
# -----------------------------
@router.get(
    "/alerts",
    response_model=list[AlertResponse],
)
def get_all_alerts(
    db: Session = Depends(get_db),
):
    return service.get_all_alerts(db)


# -----------------------------
# Get Alert By ID
# -----------------------------
@router.get(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = service.get_alert_by_id(
        db,
        alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# -----------------------------
# Create Alert
# -----------------------------
@router.post(
    "/alerts",
    response_model=AlertResponse,
    status_code=201,
)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
):

    new_alert = Alert(
        zone_id=alert.zone_id,
        message=alert.message,
        severity=alert.severity,
        status="ACTIVE",
        created_at=datetime.utcnow(),
    )

    return service.create_alert(
        db,
        new_alert,
    )


# -----------------------------
# Update Alert Status
# -----------------------------
@router.patch(
    "/alerts/{alert_id}",
    response_model=AlertResponse,
)
def update_alert_status(
    alert_id: int,
    alert: AlertUpdate,
    db: Session = Depends(get_db),
):

    updated = service.update_alert_status(
        db,
        alert_id,
        alert.status,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return updated


# -----------------------------
# Delete Alert
# -----------------------------
@router.delete("/alerts/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):

    deleted = service.delete_alert(
        db,
        alert_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return {
        "message": "Alert deleted successfully"
    }