from celery import Celery
from smartgrid.core.config import settings

app = Celery(
    "smart_grid_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"]
)

app.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=True,
    result_expires=3600,
    broker_connection_retry_on_startup=True
)

app.conf.beat_schedule = {
    "run-periodic-analytics-every-30-seconds": {
        "task": "app.tasks.run_periodic_analytics_task",
        "schedule": 30.0
    },
    "generate-load-reports-every-2-minutes": {
        "task": "app.tasks.generate_load_reports_all_zones_task",
        "schedule": 120.0
    },
    "check-alerts-every-2-minutes": {
        "task": "app.tasks.check_overload_all_zones_task",
        "schedule": 120.0
    }
}
