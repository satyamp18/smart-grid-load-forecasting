from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Index
)

from sqlalchemy.orm import relationship

from smartgrid.db.base import Base

class MeterReading(Base):

    __tablename__ = "meter_readings"

    id = Column(Integer, primary_key=True)

    meter_id = Column(
        Integer,
        ForeignKey("smart_meters.id")
    )
    voltage = Column(
    Float,
    nullable=False
    )

    current = Column(
    Float,
    nullable=False
    )

    power_kw = Column(
    Float,
    nullable=False
    )

    timestamp = Column(
    DateTime,
    nullable=False
    )

    meter = relationship(
        "SmartMeter",
        back_populates="readings"
    )

    __table_args__ = (
        Index(
            "idx_reading_timestamp",
            "timestamp"
        ),
    )