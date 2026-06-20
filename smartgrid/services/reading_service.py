from smartgrid.repositories.reading_repository import ReadingRepository

class ReadingService:

    def __init__(self):
        self.repo = ReadingRepository()

    def create_reading(
        self,
        db,
        reading
    ):
        return self.repo.create(
            db,
            reading
        )