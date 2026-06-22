from sqlalchemy.orm import Session
from smartgrid.repositories.reading_repository import ReadingRepository


class ReadingService:

    def __init__(self):
        self.repo = ReadingRepository()

    def create_reading(self, db: Session, reading):
        return self.repo.create(db, reading)

    def get_all_readings(self, db: Session):
        return self.repo.get_all(db)