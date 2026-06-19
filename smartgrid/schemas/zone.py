from pydantic import BaseModel


class ZoneCreate(BaseModel):
    name: str
    capacity_kw: float


class ZoneResponse(BaseModel):
    id: int
    name: str
    capacity_kw: float

    class Config:
        from_attributes = True