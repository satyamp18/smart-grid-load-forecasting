from pydantic import BaseModel, ConfigDict


class ZoneCreate(BaseModel):
    zone_name: str
    max_capacity_kw: float


class ZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone_name: str
    max_capacity_kw: float