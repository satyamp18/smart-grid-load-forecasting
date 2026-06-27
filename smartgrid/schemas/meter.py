from pydantic import BaseModel, ConfigDict, Field


class MeterCreate(BaseModel):
    meter_code: str = Field(..., min_length=3)
    zone_id: int = Field(..., gt=0)


class MeterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meter_code: str
    zone_id: int