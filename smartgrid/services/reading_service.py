from sqlalchemy.orm import Session

from smartgrid.models.reading import MeterReading
from smartgrid.repositories.reading_repository import ReadingRepository


class ReadingService:

    def __init__(self):
        self.repo = ReadingRepository()

    def get_all_readings(self, db: Session):
        return self.repo.get_all(db)

    def get_reading(self, db: Session, reading_id: int):
        return self.repo.get_by_id(db, reading_id)

    def create_reading(
        self,
        db: Session,
        meter_id: int,
        voltage: float,
        current: float,
        timestamp,
    ):

        # Power calculation
        power_kw = (voltage * current) / 1000

        reading = MeterReading(
            meter_id=meter_id,
            voltage=voltage,
            current=current,
            power_kw=power_kw,
            timestamp=timestamp,
        )

        return self.repo.create(db, reading)

    def delete_reading(
        self,
        db: Session,
        reading_id: int,
    ):
        return self.repo.delete(db, reading_id)