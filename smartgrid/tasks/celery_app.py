import os
from celery import Celery
from smartgrid.core.config import settings

redis_url = getattr(settings, "REDIS_URL", None) or os.getenv("REDIS_URL") or "redis://localhost:6379/0"

celery = Celery(
    "smartgrid",
    broker=redis_url,
    backend=redis_url,
    include=["smartgrid.tasks.alert_tasks"],
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    imports=("smartgrid.tasks.alert_tasks",),
    beat_schedule={
        "check-grid-load-every-30-seconds": {
            "task": "check_all_zones",
            "schedule": 30.0,
        }
    },
)

celery.autodiscover_tasks(["smartgrid.tasks"])