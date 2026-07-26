from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    zone_id: int
    message: str
    severity: str


class AlertUpdate(BaseModel):
    status: str


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone_id: int
    message: str
    severity: str
    status: str
    created_at: datetime