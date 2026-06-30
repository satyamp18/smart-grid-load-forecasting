from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.services.alert_service import AlertService

router = APIRouter()

service = AlertService()


@router.get("/alerts")
def get_all_alerts(
    db: Session = Depends(get_db),
):

    return service.get_all_alerts(db)


@router.get("/alerts/{alert_id}")
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