from pydantic import BaseModel, ConfigDict


class MeterCreate(BaseModel):
    meter_code: str
    zone_id: int


class MeterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meter_code: str
    zone_id: int