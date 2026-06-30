from sqlalchemy import *

from smartgrid.db.base import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    zone_id = Column(
        Integer,
        ForeignKey("zones.id")
    )

    message = Column(
    String,
    nullable=False
    )

    severity = Column(
    String,
    nullable=False
    )

    created_at = Column(
    DateTime,
    nullable=False
    )