from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.models.load_report import LoadReport
from smartgrid.schemas.load_report import (
    LoadReportCreate,
    LoadReportResponse,
)
from smartgrid.services.load_report_service import (
    LoadReportService,
)

router = APIRouter()

service = LoadReportService()


@router.get(
    "/load-reports",
    response_model=list[LoadReportResponse],
)
def get_all_reports(
    db: Session = Depends(get_db),
):
    return service.get_all_reports(db)


@router.get(
    "/load-reports/{report_id}",
    response_model=LoadReportResponse,
)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
):

    report = service.get_report_by_id(
        db,
        report_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Load report not found",
        )

    return report


@router.post(
    "/load-reports",
    response_model=LoadReportResponse,
)
def create_report(
    report: LoadReportCreate,
    db: Session = Depends(get_db),
):

    new_report = LoadReport(
        zone_id=report.zone_id,
        total_load_kw=report.total_load_kw,
        report_time=report.report_time,
    )

    return service.create_report(
        db,
        new_report,
    )


from smartgrid.services.load_service import LoadService

load_service = LoadService()


@router.post(
    "/load-reports/trigger/{zone_id}",
    status_code=202,
)
def trigger_load_report(
    zone_id: int,
):
    """
    Triggers an asynchronous load report generation task for a specific zone using Celery.
    Returns the task ID to track execution status.
    """
    task = load_service.generate_load_report_async(zone_id)
    return {
        "task_id": task.id,
        "status": "Task dispatched to Celery worker",
        "zone_id": zone_id
    }