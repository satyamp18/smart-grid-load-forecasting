from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoadReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    zone_id: int
    total_load_kw: float
    report_time: datetime