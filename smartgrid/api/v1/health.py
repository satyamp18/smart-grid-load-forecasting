from fastapi import APIRouter
from smartgrid.tasks.alert_tasks import check_all_zones
router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@router.get("/celery-test")
def celery_test():

    check_all_zones.delay()

    return {
        "message": "Task Sent Successfully"
    }