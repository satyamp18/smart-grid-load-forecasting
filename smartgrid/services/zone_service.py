from smartgrid.repositories.zone_repository import ZoneRepository

class ZoneService:

    def __init__(self):
        self.repo = ZoneRepository()

    def get_all_zones(self, db):
        return self.repo.get_all(db)