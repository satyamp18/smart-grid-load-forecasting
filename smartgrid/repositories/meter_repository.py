from sqlalchemy.orm import Session
from smartgrid.models.meter import SmartMeter

class MeterRepository:

    def get_all(self, db: Session):
        return db.query(SmartMeter).all()

    def create(
        self,
        db: Session,
        meter: SmartMeter
    ):
        db.add(meter)
        db.commit()
        db.refresh(meter)

        return meter