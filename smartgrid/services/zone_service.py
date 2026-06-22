from sqlalchemy.orm import Session
from smartgrid.repositories.zone_repository import ZoneRepository


class ZoneService:

    def __init__(self):
        self.repo = ZoneRepository()

    def get_all_zones(self, db: Session):
        return self.repo.get_all(db)

    def get_zone(self, db: Session, zone_id: int):
        return self.repo.get_by_id(db, zone_id)