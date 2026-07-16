from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from smartgrid.models.load_report import LoadReport
from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading
<<<<<<< HEAD

=======
import logging

logger = logging.getLogger(__name__)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e

class LoadService:

    def calculate_zone_load(
        self,
        db: Session,
        zone_id: int,
    ):

        total_load = (
            db.query(
                func.sum(MeterReading.power_kw)
            )
            .join(
                SmartMeter,
                MeterReading.meter_id == SmartMeter.id,
            )
            .filter(
                SmartMeter.zone_id == zone_id
            )
            .scalar()
        )

        if total_load is None:
            total_load = 0

        return total_load

    def generate_load_report(
        self,
        db: Session,
        zone_id: int,
    ):

        total_load = self.calculate_zone_load(
            db,
            zone_id,
        )

        report = LoadReport(
            zone_id=zone_id,
            total_load_kw=total_load,
            report_time=datetime.utcnow(),
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return report