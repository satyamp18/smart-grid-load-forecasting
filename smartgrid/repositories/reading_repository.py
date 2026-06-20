from sqlalchemy.orm import Session
from smartgrid.models.reading import MeterReading

class ReadingRepository:

    def create(
        self,
        db: Session,
        reading: MeterReading
    ):
        db.add(reading)
        db.commit()
        db.refresh(reading)

        return reading