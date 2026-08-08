from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class InventoryCreate(BaseModel):
    storage_unit_id: int
    vaccine_name: str
    vaccine_code: str
    lot_number: str
    quantity: int
    expiration_date: date
    status: str = "Good"
class InventoryUpdate(BaseModel):
    storage_unit_id: int
    vaccine_name: str
    vaccine_code: str
    lot_number: str
    quantity: int
    expiration_date: date
    status: str


class InventoryResponse(BaseModel):
    id: int
    storage_unit_id: int
    vaccine_name: str
    vaccine_code: str
    lot_number: str
    quantity: int
    expiration_date: date
    received_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)