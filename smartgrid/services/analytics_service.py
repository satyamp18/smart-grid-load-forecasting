from sqlalchemy import func
from sqlalchemy.orm import Session

from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading


class AnalyticsService:

    def get_zone_current_load(
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
                MeterReading.meter_id == SmartMeter.id
            )
            .filter(
                SmartMeter.zone_id == zone_id
            )
            .scalar()
        )

        return total_load or 0

    def get_peak_load(
        self,
        db: Session,
        zone_id: int,
    ):

        peak_load = (
            db.query(
                func.max(MeterReading.power_kw)
            )
            .join(
                SmartMeter,
                MeterReading.meter_id == SmartMeter.id
            )
            .filter(
                SmartMeter.zone_id == zone_id
            )
            .scalar()
        )

        return peak_load or 0

    def get_average_load(
        self,
        db: Session,
        zone_id: int,
    ):

        average_load = (
            db.query(
                func.avg(MeterReading.power_kw)
            )
            .join(
                SmartMeter,
                MeterReading.meter_id == SmartMeter.id
            )
            .filter(
                SmartMeter.zone_id == zone_id
            )
            .scalar()
        )

        return average_load or 0

    def get_zone_history(
        self,
        db: Session,
        zone_id: int,
    ):

        history = (
            db.query(MeterReading)
            .join(
                SmartMeter,
                MeterReading.meter_id == SmartMeter.id
            )
            .filter(
                SmartMeter.zone_id == zone_id
            )
            .order_by(
                MeterReading.timestamp.desc()
            )
            .all()
        )

        return history