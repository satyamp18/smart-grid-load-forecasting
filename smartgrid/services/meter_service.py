from sqlalchemy.orm import Session
from smartgrid.repositories.meter_repository import MeterRepository


class MeterService:

    def __init__(self):
        self.repo = MeterRepository()

    def get_all_meters(self, db: Session):
        return self.repo.get_all(db)

    def create_meter(self, db: Session, meter):
        return self.repo.create(db, meter)