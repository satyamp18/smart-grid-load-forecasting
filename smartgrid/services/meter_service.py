from smartgrid.repositories.meter_repository import MeterRepository

class MeterService:

    def __init__(self):
        self.repo = MeterRepository()

    def get_all_meters(self, db):
        return self.repo.get_all(db)