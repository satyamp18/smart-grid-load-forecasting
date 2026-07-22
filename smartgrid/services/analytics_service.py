from sqlalchemy.orm import Session

from smartgrid.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self):
        self.repo = AnalyticsRepository()

    def get_zone_current_load(self, db: Session, zone_id: int):
        return self.repo.get_current_load(db, zone_id)

    def get_peak_load(self, db: Session, zone_id: int):
        return self.repo.get_peak_load(db, zone_id)

    def get_average_load(self, db: Session, zone_id: int):
        return self.repo.get_average_load(db, zone_id)

    def get_zone_history(self, db: Session, zone_id: int):
        return self.repo.get_history(db, zone_id)