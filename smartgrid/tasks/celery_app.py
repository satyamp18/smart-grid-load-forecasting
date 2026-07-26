from celery import Celery
imports=("smartgrid.tasks.alert_task",)

celery = Celery(
    "smartgrid",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    imports=("smartgrid.tasks.alert_tasks",),  # <-- Add this
    beat_schedule={
        "check-grid-load-every-30-seconds": {
            "task": "check_all_zones",
            "schedule": 30.0,
        }
    },
)

celery.autodiscover_tasks(["smartgrid.tasks"])