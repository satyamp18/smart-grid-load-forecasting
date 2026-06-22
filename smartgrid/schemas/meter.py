from pydantic import BaseModel, Field, ConfigDict


class MeterCreate(BaseModel):
    meter_code: str = Field(..., min_length=3, max_length=50)
    zone_id: int


class MeterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meter_code: str
    zone_id: int