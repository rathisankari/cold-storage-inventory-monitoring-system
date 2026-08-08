from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StorageUnitCreate(BaseModel):
    name: str
    facility_id: str
    unit_type: str
    min_temp: float
    max_temp: float
    status: str = "Active"
    last_service_date: datetime | None = None
class StorageUnitUpdate(BaseModel):
    name: str
    facility_id: str
    unit_type: str
    min_temp: float
    max_temp: float
    status: str
    last_service_date: datetime | None = None


class StorageUnitResponse(BaseModel):
    id: int
    name: str
    facility_id: str
    unit_type: str
    min_temp: float
    max_temp: float
    status: str
    last_service_date: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)