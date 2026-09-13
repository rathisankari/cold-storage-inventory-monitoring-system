from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureLogCreate(BaseModel):
    storage_unit_id: int
    temperature: float
    humidity: float | None = None
    source: str = "IoT_Sensor"


class TemperatureLogResponse(BaseModel):
    id: int
    storage_unit_id: int
    temperature: float
    humidity: float | None
    recorded_at: datetime
    source: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)