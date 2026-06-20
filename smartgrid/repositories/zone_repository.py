from sqlalchemy.orm import Session
from smartgrid.models.zone import Zone

class ZoneRepository:

    def get_all(self, db: Session):
        return db.query(Zone).all()

    def get_by_id(self, db: Session, zone_id: int):
        return db.query(Zone).filter(
            Zone.id == zone_id
        ).first()