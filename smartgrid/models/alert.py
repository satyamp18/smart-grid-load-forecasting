from sqlalchemy import *

from app.db.base import Base

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    zone_id = Column(
        Integer,
        ForeignKey("zones.id")
    )

    message = Column(String)

    severity = Column(String)

    created_at = Column(DateTime)