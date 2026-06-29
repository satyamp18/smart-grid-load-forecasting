from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_zones: int
    total_meters: int
    total_readings: int
    total_alerts: int
    total_load_kw: float