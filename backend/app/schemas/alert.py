from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    id: int
    storage_unit_id: int
    alert_type: str
    severity: str
    message: str
    status: str
    acknowledged_by: int | None
    acknowledged_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)