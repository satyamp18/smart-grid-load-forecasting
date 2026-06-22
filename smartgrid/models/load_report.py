from sqlalchemy import *

from smartgrid.db.base import Base


class LoadReport(Base):

    __tablename__ = "load_reports"

    id = Column(Integer, primary_key=True)

    zone_id = Column(
        Integer,
        ForeignKey("zones.id")
    )

    total_load_kw = Column(
    Float,
    nullable=False
    )

    report_time = Column(
    DateTime,
    nullable=False
    )