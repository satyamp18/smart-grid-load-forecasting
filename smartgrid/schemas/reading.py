from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReadingCreate(BaseModel):
    meter_id: int
    voltage: float
    current: float
    timestamp: datetime


class ReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meter_id: int
    voltage: float
    current: float
    power_kw: float
    timestamp: datetime