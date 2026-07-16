from sqlalchemy.orm import Session

from smartgrid.models.reading import MeterReading
from smartgrid.repositories.reading_repository import ReadingRepository
<<<<<<< HEAD

=======
import logging

logger = logging.getLogger(__name__)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e

class ReadingService:

    def __init__(self):
        self.repo = ReadingRepository()

    def get_all_readings(self, db: Session):
        return self.repo.get_all(db)

    def get_reading(self, db: Session, reading_id: int):
        return self.repo.get_by_id(db, reading_id)

    def create_reading(self, db: Session, reading: MeterReading):

        reading.power_kw = (
            reading.voltage * reading.current
        ) / 1000

        return self.repo.create(db, reading)

    def delete_reading(self, db: Session, reading_id: int):
        return self.repo.delete(db, reading_id)