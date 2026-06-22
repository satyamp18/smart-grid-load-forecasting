from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ReadingCreate(BaseModel):
    meter_id: int
    voltage: float = Field(..., gt=0)
    current: float = Field(..., gt=0)
    power_kw: float = Field(..., gt=0)
    timestamp: datetime


class ReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meter_id: int
    voltage: float
    current: float
    power_kw: float
    timestamp: datetime