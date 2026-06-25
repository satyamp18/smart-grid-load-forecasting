from sqlalchemy.orm import Session

from smartgrid.models.load_report import LoadReport


class LoadReportRepository:

    def get_all(self, db: Session):
        return db.query(LoadReport).all()

    def get_by_id(self, db: Session, report_id: int):
        return (
            db.query(LoadReport)
            .filter(LoadReport.id == report_id)
            .first()
        )

    def create(self, db: Session, report: LoadReport):
        db.add(report)
        db.commit()
        db.refresh(report)

        return report