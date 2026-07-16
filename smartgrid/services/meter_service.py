from sqlalchemy.orm import Session
from smartgrid.repositories.meter_repository import MeterRepository
<<<<<<< HEAD

=======
import logging

logger = logging.getLogger(__name__)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e

class MeterService:

    def __init__(self):
        self.repo = MeterRepository()

    def get_all_meters(self, db: Session):
        return self.repo.get_all(db)

    def get_meter(self, db: Session, meter_id: int):
        return self.repo.get_by_id(db, meter_id)

    def create_meter(self, db: Session, meter):
        return self.repo.create(db, meter)

    def delete_meter(self, db: Session, meter_id: int):
        return self.repo.delete(db, meter_id)