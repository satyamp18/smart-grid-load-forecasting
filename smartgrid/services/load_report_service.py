from sqlalchemy.orm import Session

from smartgrid.models.load_report import LoadReport
from smartgrid.repositories.load_report_repository import (
    LoadReportRepository,
)
<<<<<<< HEAD
=======
import logging

logger = logging.getLogger(__name__)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e


class LoadReportService:

    def __init__(self):
        self.repo = LoadReportRepository()

    # -----------------------------
    # CRUD Operations
    # -----------------------------

    def get_all_reports(
        self,
        db: Session,
    ):
        return self.repo.get_all(db)

    def get_report_by_id(
        self,
        db: Session,
        report_id: int,
    ):
        return self.repo.get_by_id(
            db,
            report_id,
        )

    def create_report(
        self,
        db: Session,
        report: LoadReport,
    ):
        return self.repo.create(
            db,
            report,
        )