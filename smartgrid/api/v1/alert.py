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


@router.post(
    "/alerts/check/{zone_id}",
    status_code=202,
)
def trigger_overload_check(
    zone_id: int,
):
    """
    Triggers an asynchronous overload check task for a specific zone using Celery.
    Returns the task ID to track execution status.
    """
    task = service.check_overload_async(zone_id)
    return {
        "task_id": task.id,
        "status": "Task dispatched to Celery worker",
        "zone_id": zone_id
    }