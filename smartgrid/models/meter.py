from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from smartgrid.db.base import Base

class SmartMeter(Base):

    __tablename__ = "smart_meters"

    id = Column(Integer, primary_key=True)

    meter_code = Column(
        String,
        unique=True
    )

    zone_id = Column(
        Integer,
        ForeignKey("zones.id")
    )

    zone = relationship(
        "Zone",
        back_populates="meters"
    )

    readings = relationship(
        "MeterReading",
        back_populates="meter"
    )