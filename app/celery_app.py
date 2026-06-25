from celery import Celery

app = Celery(
    "smart_grid_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
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
    "monitor-database-zones-every-30-seconds": {
        "task": "app.tasks.monitor_all_zones_task",
        "schedule": 30.0
    }
}
