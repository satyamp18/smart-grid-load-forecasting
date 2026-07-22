from sqlalchemy.orm import Session

from smartgrid.models.reading import MeterReading


class ReadingRepository:

    def get_all(self, db: Session):
        return db.query(MeterReading).all()

    def get_by_id(self, db: Session, reading_id: int):
        return (
            db.query(MeterReading)
            .filter(MeterReading.id == reading_id)
            .first()
        )

    def create(self, db: Session, reading: MeterReading):
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading

    def update(
        self,
        db: Session,
        reading_id: int,
        reading_data,
    ):
        reading = self.get_by_id(db, reading_id)

        if not reading:
            return None

        reading.meter_id = reading_data.meter_id
        reading.voltage = reading_data.voltage
        reading.current = reading_data.current
        reading.timestamp = reading_data.timestamp
        reading.power_kw = (
            reading.voltage * reading.current
        ) / 1000

        db.commit()
        db.refresh(reading)

        return reading

    def delete(self, db: Session, reading_id: int):

        reading = self.get_by_id(db, reading_id)

        if not reading:
            return None

        db.delete(reading)
        db.commit()

        return reading