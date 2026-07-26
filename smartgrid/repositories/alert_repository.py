from sqlalchemy.orm import Session

from smartgrid.models.alert import Alert


class AlertRepository:

    # -----------------------------
    # Read Operations
    # -----------------------------

    def get_all(self, db: Session):
        return (
            db.query(Alert)
            .order_by(Alert.created_at.desc())
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        alert_id: int,
    ):
        return (
            db.query(Alert)
            .filter(Alert.id == alert_id)
            .first()
        )

    def get_active_alert(
        self,
        db: Session,
        zone_id: int,
    ):
        return (
            db.query(Alert)
            .filter(
                Alert.zone_id == zone_id,
                Alert.status == "ACTIVE",
            )
            .first()
        )

    # -----------------------------
    # Create
    # -----------------------------

    def create(
        self,
        db: Session,
        alert: Alert,
    ):
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    # -----------------------------
    # Update
    # -----------------------------

    def update_status(
        self,
        db: Session,
        alert_id: int,
        status: str,
    ):
        alert = self.get_by_id(
            db,
            alert_id,
        )

        if alert is None:
            return None

        alert.status = status

        db.commit()
        db.refresh(alert)

        return alert

    # -----------------------------
    # Delete
    # -----------------------------

    def delete(
        self,
        db: Session,
        alert_id: int,
    ):

        alert = self.get_by_id(
            db,
            alert_id,
        )

        if alert is None:
            return None

        db.delete(alert)
        db.commit()

        return alert