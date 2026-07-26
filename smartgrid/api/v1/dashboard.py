from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from smartgrid.db.dependencies import get_db
from smartgrid.schemas.dashboard import DashboardResponse
from smartgrid.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

service = DashboardService()


@router.get(
    "/summary",
    response_model=DashboardResponse,
    summary="Dashboard Summary",
    description="Returns Smart Grid dashboard statistics.",
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):
    return service.get_dashboard_summary(db)


@router.get(
    "/health",
    summary="System Health",
    description="Returns Smart Grid system health.",
)
def get_dashboard_health(
    db: Session = Depends(get_db),
):
    return service.get_health_status(db)