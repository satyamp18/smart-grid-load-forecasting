from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from smartgrid.db.base import Base

class Zone(Base):

    __tablename__ = "zones"

    id = Column(Integer, primary_key=True)

    zone_name = Column(
        String,
        unique=True,
        nullable=False
    )

    max_capacity_kw = Column(
    Float,
    nullable=False
    )

    meters = relationship(
        "SmartMeter",
        back_populates="zone"
    )