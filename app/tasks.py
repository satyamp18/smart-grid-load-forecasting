import os
from celery.utils.log import get_task_logger
from app.celery_app import app
from app.analytics import generate_formatted_reports

from smartgrid.db.session import SessionLocal
from smartgrid.services.load_service import LoadService
from smartgrid.services.alert_service import AlertService
from smartgrid.models.zone import Zone

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

@app.task(name="app.tasks.generate_load_report_task")
def generate_load_report_task(zone_id: int):
    logger.info(f"Starting load report generation for zone {zone_id}...")
    db = SessionLocal()
    try:
        load_service = LoadService()
        report = load_service.generate_load_report(db, zone_id)
        logger.info(f"Successfully generated load report {report.id} for zone {zone_id}. Total load: {report.total_load_kw} kW.")
    except Exception as e:
        logger.error(f"Failed to generate load report for zone {zone_id}: {e}")
    finally:
        db.close()

@app.task(name="app.tasks.check_zone_overload_task")
def check_zone_overload_task(zone_id: int):
    logger.info(f"Starting overload check for zone {zone_id}...")
    db = SessionLocal()
    try:
        alert_service = AlertService()
        alert = alert_service.check_overload(db, zone_id)
        if alert:
            logger.warn(f"🚨 [OVERLOAD ALERT DETECTED] Zone {zone_id}: {alert.message} (Severity: {alert.severity})")
        else:
            logger.info(f"✅ Zone {zone_id} is operating within safe capacity limits.")
    except Exception as e:
        logger.error(f"Failed to run overload check for zone {zone_id}: {e}")
    finally:
        db.close()

@app.task(name="app.tasks.generate_load_reports_all_zones_task")
def generate_load_reports_all_zones_task():
    logger.info("Periodic cron: Dispatching load report generation tasks for all registered zones...")
    db = SessionLocal()
    try:
        zones = db.query(Zone).all()
        logger.info(f"Found {len(zones)} zones in database for load report generation.")
        for zone in zones:
            generate_load_report_task.delay(zone.id)
    except Exception as e:
        logger.error(f"Failed to fetch zones for load report generation: {e}")
    finally:
        db.close()

@app.task(name="app.tasks.check_overload_all_zones_task")
def check_overload_all_zones_task():
    logger.info("Periodic cron: Dispatching overload check tasks for all registered zones...")
    db = SessionLocal()
    try:
        zones = db.query(Zone).all()
        logger.info(f"Found {len(zones)} zones in database for overload checks.")
        for zone in zones:
            check_zone_overload_task.delay(zone.id)
    except Exception as e:
        logger.error(f"Failed to fetch zones for overload checks: {e}")
    finally:
        db.close()
