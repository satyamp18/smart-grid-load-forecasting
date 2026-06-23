from datetime import datetime

from sqlalchemy.orm import Session

from smartgrid.models.alert import Alert
from smartgrid.models.zone import Zone
from smartgrid.repositories.alert_repository import AlertRepository
from smartgrid.services.load_service import LoadService


class AlertService:

    def __init__(self):
        self.repo = AlertRepository()
        self.load_service = LoadService()

    # -----------------------------
    # CRUD Operations
    # -----------------------------

    def get_all_alerts(self, db: Session):
        return self.repo.get_all(db)

    def get_alert_by_id(self, db: Session, alert_id: int):
        return self.repo.get_by_id(db, alert_id)

    def create_alert(self, db: Session, alert: Alert):
        return self.repo.create(db, alert)

    def delete_alert(self, db: Session, alert_id: int):
        return self.repo.delete(db, alert_id)

    # -----------------------------
    # Business Logic
    # -----------------------------

    def check_overload(
        self,
        db: Session,
        zone_id: int,
    ):

        zone = (
            db.query(Zone)
            .filter(Zone.id == zone_id)
            .first()
        )

        if not zone:
            return None

        current_load = self.load_service.calculate_zone_load(
            db,
            zone_id,
        )

        utilization = (
            current_load / zone.max_capacity_kw
        ) * 100

        if utilization >= 90:

            alert = Alert(
                zone_id=zone_id,
                message=f"{zone.zone_name} exceeded 90% capacity",
                severity="HIGH",
                created_at=datetime.utcnow(),
            )

            return self.repo.create(db, alert)

        return None