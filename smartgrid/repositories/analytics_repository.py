from sqlalchemy import func
from sqlalchemy.orm import Session

from smartgrid.models.meter import SmartMeter
from smartgrid.models.reading import MeterReading


class AnalyticsRepository:

    def get_current_load(self, db: Session, zone_id: int):
        return (
            db.query(func.sum(MeterReading.power_kw))
            .join(SmartMeter, MeterReading.meter_id == SmartMeter.id)
            .filter(SmartMeter.zone_id == zone_id)
            .scalar()
        ) or 0

    def get_peak_load(self, db: Session, zone_id: int):
        return (
            db.query(func.max(MeterReading.power_kw))
            .join(SmartMeter, MeterReading.meter_id == SmartMeter.id)
            .filter(SmartMeter.zone_id == zone_id)
            .scalar()
        ) or 0

    def get_average_load(self, db: Session, zone_id: int):
        return (
            db.query(func.avg(MeterReading.power_kw))
            .join(SmartMeter, MeterReading.meter_id == SmartMeter.id)
            .filter(SmartMeter.zone_id == zone_id)
            .scalar()
        ) or 0

    def get_history(self, db: Session, zone_id: int):
        return (
            db.query(MeterReading)
            .join(SmartMeter, MeterReading.meter_id == SmartMeter.id)
            .filter(SmartMeter.zone_id == zone_id)
            .order_by(MeterReading.timestamp.desc())
            .all()
        )