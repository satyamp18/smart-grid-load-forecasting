from sqlalchemy import func
from sqlalchemy.orm import Session

from smartgrid.models.zone import Zone
from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading
from smartgrid.models.alert import Alert
import logging

logger = logging.getLogger(__name__)


class DashboardService:

    def get_dashboard_summary(self, db: Session):

        total_zones = db.query(Zone).count()

        total_meters = db.query(SmartMeter).count()

        total_readings = db.query(MeterReading).count()

        total_alerts = db.query(Alert).count()

        total_load = (
            db.query(func.sum(MeterReading.power_kw))
            .scalar()
        )

        return {
            "total_zones": total_zones,
            "total_meters": total_meters,
            "total_readings": total_readings,
            "total_alerts": total_alerts,
            "total_load_kw": total_load or 0.0,
        }
    
    def get_health_status(self, db: Session):

     return {
        "database": "Connected",
        "api": "Running",
        "zones": db.query(Zone).count(),
        "meters": db.query(SmartMeter).count(),
        "status": "Healthy"
    }