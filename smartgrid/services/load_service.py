from sqlalchemy.orm import Session

from smartgrid.models.reading import MeterReading
from smartgrid.models.meter import SmartMeter
from smartgrid.models.zone import Zone


class LoadService:

    def calculate_zone_load(
        self,
        db: Session,
        zone_id: int
    ):

        total_load = (
            db.query(MeterReading.power_kw)
            .join(
                SmartMeter,
                MeterReading.meter_id == SmartMeter.id
            )
            .filter(
                SmartMeter.zone_id == zone_id
            )
            .all()
        )

        return sum(
            load[0] for load in total_load
            if load[0] is not None
        )