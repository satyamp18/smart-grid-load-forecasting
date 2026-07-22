from sqlalchemy.orm import Session
from smartgrid.models.meter import SmartMeter


class MeterRepository:

    def get_all(self, db: Session):
        return db.query(SmartMeter).all()

    def get_by_id(self, db: Session, meter_id: int):
        return (
            db.query(SmartMeter)
            .filter(SmartMeter.id == meter_id)
            .first()
        )

    def create(self, db: Session, meter: SmartMeter):
        db.add(meter)
        db.commit()
        db.refresh(meter)

        return meter

    def delete(self, db: Session, meter_id: int):

        meter = self.get_by_id(db, meter_id)

        if not meter:
            return None

        db.delete(meter)
        db.commit()

        return meter
    
    def update(self, db: Session, meter_id: int, meter_data):

       meter = self.get_by_id(db, meter_id)

       if not meter:
         return None

       meter.meter_code = meter_data.meter_code
       meter.zone_id = meter_data.zone_id

       db.commit()
       db.refresh(meter)

       return meter