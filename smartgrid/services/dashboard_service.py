import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from smartgrid.models.alert import Alert
from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading
from smartgrid.models.zone import Zone

logger = logging.getLogger(__name__)


class DashboardService:

    def get_dashboard_summary(self, db: Session):

        total_zones = db.query(Zone).count()

        total_meters = db.query(SmartMeter).count()

        total_readings = db.query(MeterReading).count()

        active_alerts = (
            db.query(Alert)
            .filter(Alert.status == "ACTIVE")
            .count()
        )

        resolved_alerts = (
            db.query(Alert)
            .filter(Alert.status == "RESOLVED")
            .count()
        )

        total_load = (
            db.query(
                func.coalesce(
                    func.sum(MeterReading.power_kw),
                    0.0,
                )
            )
            .scalar()
        )

        total_capacity = (
            db.query(
                func.coalesce(
                    func.sum(Zone.max_capacity_kw),
                    0.0,
                )
            )
            .scalar()
        )

        utilization = 0.0

        if total_capacity > 0:
            utilization = round(
                (total_load / total_capacity) * 100,
                2,
            )

        return {
            "total_zones": total_zones,
            "total_meters": total_meters,
            "total_readings": total_readings,
            "active_alerts": active_alerts,
            "resolved_alerts": resolved_alerts,
            "total_load_kw": round(total_load, 2),
            "overall_utilization": utilization,
        }

    def get_health_status(self, db: Session):

        total_capacity = (
            db.query(
                func.coalesce(
                    func.sum(Zone.max_capacity_kw),
                    0.0,
                )
            )
            .scalar()
        )

        total_load = (
            db.query(
                func.coalesce(
                    func.sum(MeterReading.power_kw),
                    0.0,
                )
            )
            .scalar()
        )

        utilization = 0.0

        if total_capacity > 0:
            utilization = (
                total_load / total_capacity
            ) * 100

        if utilization >= 90:
            health = "Critical"
        elif utilization >= 75:
            health = "Warning"
        else:
            health = "Healthy"

        return {
            "database": "Connected",
            "api": "Running",
            "status": health,
            "zones": db.query(Zone).count(),
            "meters": db.query(SmartMeter).count(),
            "active_alerts": db.query(Alert).filter(
                Alert.status == "ACTIVE"
            ).count(),
            "resolved_alerts": db.query(Alert).filter(
                Alert.status == "RESOLVED"
            ).count(),
            "overall_utilization": round(utilization, 2),
        }