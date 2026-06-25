from sqlalchemy.orm import Session

from smartgrid.models.alert import Alert


class AlertRepository:

    def get_all(self, db: Session):
        return db.query(Alert).all()

    def get_by_id(self, db: Session, alert_id: int):
        return (
            db.query(Alert)
            .filter(Alert.id == alert_id)
            .first()
        )

    def create(self, db: Session, alert: Alert):
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    def delete(self, db: Session, alert_id: int):

        alert = self.get_by_id(db, alert_id)

        if not alert:
            return None

        db.delete(alert)
        db.commit()

        return alert