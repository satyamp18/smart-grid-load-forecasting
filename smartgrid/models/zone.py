from sqlalchemy import Column, Integer, String, Float
from smartgrid.db.base import Base

class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity_kw = Column(Float, nullable=False)