from sqlalchemy.orm import Session
from smartgrid.models.zone import Zone


class ZoneRepository:

    def get_all(self, db: Session):
        return db.query(Zone).all()

    def get_by_id(self, db: Session, zone_id: int):
        return (
            db.query(Zone)
            .filter(Zone.id == zone_id)
            .first()
        )

    def create(self, db: Session, zone: Zone):
        db.add(zone)
        db.commit()
        db.refresh(zone)
        return zone

    def update(self, db: Session, zone_id: int, zone_data):
        zone = self.get_by_id(db, zone_id)

        if not zone:
            return None

        zone.zone_name = zone_data.zone_name
        zone.max_capacity_kw = zone_data.max_capacity_kw

        db.commit()
        db.refresh(zone)

        return zone

    def delete(self, db: Session, zone_id: int):
        zone = self.get_by_id(db, zone_id)

        if not zone:
            return None

        db.delete(zone)
        db.commit()

        return zone