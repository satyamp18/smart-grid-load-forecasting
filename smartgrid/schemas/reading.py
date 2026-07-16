from datetime import datetime

<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict


class ReadingCreate(BaseModel):
    meter_id: int
    voltage: float
    current: float
=======
from pydantic import BaseModel, ConfigDict, Field


class ReadingCreate(BaseModel):
    meter_id: int = Field(..., gt=0)
    voltage: float = Field(..., gt=0)
    current: float = Field(..., gt=0)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e
    timestamp: datetime


class ReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meter_id: int
    voltage: float
    current: float
    power_kw: float
    timestamp: datetime