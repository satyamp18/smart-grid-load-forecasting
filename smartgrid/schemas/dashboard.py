from pydantic import BaseModel


class DashboardResponse(BaseModel):

    total_zones: int
    total_meters: int
    total_readings: int

    active_alerts: int
    resolved_alerts: int

    total_load_kw: float
    overall_utilization: float