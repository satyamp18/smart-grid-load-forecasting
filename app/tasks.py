import os
from celery.utils.log import get_task_logger
from app.celery_app import app
from app.analytics import generate_formatted_reports

logger = get_task_logger(__name__)

@app.task(name="app.tasks.run_periodic_analytics_task")
def run_periodic_analytics_task():
    logger.info("Starting automated background analytics and overload detection task...")
    csv_path = os.path.join("data", "sample_meter_data.csv")
    try:
        generate_formatted_reports(csv_path)
        logger.info("Automated background analytics task completed successfully.")
    except Exception as e:
        logger.error(f"Automated background analytics task failed: {e}")
