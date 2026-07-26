from datetime import datetime
import asyncio
import logging

from sqlalchemy.orm import Session

from smartgrid.models.alert import Alert
from smartgrid.models.zone import Zone
from smartgrid.repositories.alert_repository import AlertRepository
from smartgrid.services.load_service import LoadService
from smartgrid.websocket.manager import manager

logger = logging.getLogger(__name__)


class AlertService:

    def __init__(self):
        self.repo = AlertRepository()
        self.load_service = LoadService()

    # -----------------------------
    # CRUD
    # -----------------------------

    def get_all_alerts(self, db: Session):
        return self.repo.get_all(db)

    def get_alert_by_id(self, db: Session, alert_id: int):
        return self.repo.get_by_id(db, alert_id)

    def create_alert(self, db: Session, alert: Alert):
        return self.repo.create(db, alert)

    def update_alert_status(
        self,
        db: Session,
        alert_id: int,
        status: str,
    ):
        return self.repo.update_status(
            db,
            alert_id,
            status,
        )

    def delete_alert(
        self,
        db: Session,
        alert_id: int,
    ):
        return self.repo.delete(
            db,
            alert_id,
        )

    # -----------------------------
    # Alert Monitoring
    # -----------------------------

    def check_overload(
        self,
        db: Session,
        zone_id: int,
    ):

        zone = (
            db.query(Zone)
            .filter(Zone.id == zone_id)
            .first()
        )

        if zone is None:
            logger.warning("Zone %s not found.", zone_id)
            return None

        if zone.max_capacity_kw <= 0:
            logger.warning(
                "Invalid max capacity for zone %s",
                zone.zone_name,
            )
            return None

        current_load = self.load_service.calculate_zone_load(
            db,
            zone_id,
        )

        utilization = (
            current_load / zone.max_capacity_kw
        ) * 100

        logger.info(
            "Zone=%s | Load=%.2f | Capacity=%.2f | Utilization=%.2f%%",
            zone.zone_name,
            current_load,
            zone.max_capacity_kw,
            utilization,
        )

        active_alert = self.repo.get_active_alert(
            db,
            zone_id,
     )

        # =====================================================
        # OVERLOAD
        # =====================================================

        if utilization >= 90:

            logger.warning(
                "OVERLOAD detected in %s (%.2f%%)",
                zone.zone_name,
                utilization,
            )

            if active_alert:

                logger.info(
                    "Active alert already exists for %s",
                    zone.zone_name,
                )

                return active_alert

            alert = Alert(
                zone_id=zone_id,
                message=f"{zone.zone_name} exceeded 90% capacity",
                severity="HIGH",
                status="ACTIVE",
                created_at=datetime.utcnow(),
            )

            saved_alert = self.repo.create(
                db,
                alert,
            )

            try:

                asyncio.run(
                    manager.broadcast(
                        {
                            "type": "NEW_ALERT",
                            "id": saved_alert.id,
                            "zone_id": saved_alert.zone_id,
                            "message": saved_alert.message,
                            "severity": saved_alert.severity,
                            "status": saved_alert.status,
                            "created_at": saved_alert.created_at.isoformat(),
                        }
                    )
                )

            except Exception:

                logger.exception(
                    "Failed to broadcast NEW_ALERT"
                )

            logger.info(
                "Alert created for %s",
                zone.zone_name,
            )

            return saved_alert

        # =====================================================
        # NORMAL
        # =====================================================

        if active_alert:

            active_alert = self.repo.update_status(
                db,
                active_alert.id,
                "RESOLVED",
            )

            try:

                asyncio.run(
                    manager.broadcast(
                        {
                            "type": "ALERT_RESOLVED",
                            "id": active_alert.id,
                            "zone_id": active_alert.zone_id,
                            "message": active_alert.message,
                            "severity": active_alert.severity,
                            "status": active_alert.status,
                            "created_at": active_alert.created_at.isoformat(),
                        }
                    )
                )

            except Exception:

                logger.exception(
                    "Failed to broadcast ALERT_RESOLVED"
                )

            logger.info(
                "Zone %s returned to normal (%.2f%%)",
                zone.zone_name,
                utilization,
            )

        else:

            logger.info(
                "Zone %s Normal (%.2f%%)",
                zone.zone_name,
                utilization,
            )

        return None