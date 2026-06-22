from datetime import datetime

from sqlalchemy.orm import Session

from smartgrid.models.alert import Alert
from smartgrid.models.zone import Zone
from smartgrid.services.load_service import LoadService


class AlertService:

    def __init__(self):
        self.load_service = LoadService()

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

            db.add(alert)
            db.commit()
            db.refresh(alert)

            return alert

        return None