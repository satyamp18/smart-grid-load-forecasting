import logging

from smartgrid.tasks.celery_app import celery
from smartgrid.db.session import SessionLocal
from smartgrid.models.zone import Zone
from smartgrid.services.alert_service import AlertService

logger = logging.getLogger(__name__)


@celery.task(name="check_all_zones")
def check_all_zones():

    logger.info("=" * 60)
    logger.info("Starting Smart Grid Background Monitoring")
    logger.info("=" * 60)

    db = SessionLocal()

    try:

        alert_service = AlertService()

        zones = (
            db.query(Zone)
            .order_by(Zone.id)
            .all()
        )

        logger.info("Found %d zones", len(zones))

        if not zones:
            logger.warning("No zones found.")
            return "No Zones"

        total_alerts = 0

        for zone in zones:

            logger.info("-" * 50)
            logger.info(
                "Checking Zone: %s",
                zone.zone_name,
            )

            try:

                alert = alert_service.check_overload(
                    db,
                    zone.id,
                )

                if alert:

                    total_alerts += 1

                    logger.warning(
                        "ACTIVE ALERT -> %s",
                        alert.message,
                    )

                else:

                    logger.info(
                        "%s is operating normally.",
                        zone.zone_name,
                    )

            except Exception:

                logger.exception(
                    "Error while checking zone %s",
                    zone.zone_name,
                )

        logger.info("=" * 60)
        logger.info(
            "Monitoring Completed | Active Alerts Created: %d",
            total_alerts,
        )
        logger.info("=" * 60)

        return "Completed"

    except Exception:

        logger.exception(
            "Background Monitoring Failed"
        )

        return "Failed"

    finally:

        db.close()