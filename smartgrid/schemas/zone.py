<<<<<<< HEAD
from pydantic import BaseModel, ConfigDict


class ZoneCreate(BaseModel):
    zone_name: str
    max_capacity_kw: float
=======
from pydantic import BaseModel, ConfigDict, Field


class ZoneCreate(BaseModel):
    zone_name: str = Field(..., min_length=3, max_length=50)
    max_capacity_kw: float = Field(..., gt=0)
>>>>>>> cf97e51a24b5e46d23341cee844332d97990216e


class ZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone_name: str
    max_capacity_kw: float