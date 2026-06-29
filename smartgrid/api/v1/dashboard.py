from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.schemas.dashboard import DashboardResponse
from smartgrid.services.dashboard_service import DashboardService

router = APIRouter()

service = DashboardService()


@router.get(
    "/dashboard/summary",
    response_model=DashboardResponse,
    summary="Dashboard Summary",
    description="Returns overall Smart Grid statistics."
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    return service.get_dashboard_summary(db)

@router.get(
    "/dashboard/health",
    summary="Dashboard Health",
    description="Returns Smart Grid system health."
)
def get_dashboard_health(
    db: Session = Depends(get_db),
):
    return service.get_health_status(db)