from datetime import datetime

from pydantic import BaseModel


class LatestTemperature(BaseModel):
    temperature: float
    humidity: float
    recorded_at: datetime
    source: str


class MonitoringResponse(BaseModel):
    storage_unit_id: int
    storage_unit_name: str
    status: str
    min_temp: float
    max_temp: float

    latest_temperature: LatestTemperature | None
    temperature_status: str

    active_alerts: int