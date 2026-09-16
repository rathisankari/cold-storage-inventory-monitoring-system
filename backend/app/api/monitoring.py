from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.alert import Alert
from app.models.storage_unit import StorageUnit
from app.models.temperature_log import TemperatureLog
from app.models.user import User
from app.schemas.temperature_log import TemperatureLogResponse
from app.schemas.monitoring import MonitoringResponse


router = APIRouter(
    prefix="/monitoring",
    tags=["Monitoring"]
)


@router.get("/{storage_unit_id}", response_model=MonitoringResponse)
def get_monitoring(
    storage_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    storage_unit = (
        db.query(StorageUnit)
        .filter(StorageUnit.id == storage_unit_id)
        .first()
    )

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    latest_temperature = (
        db.query(TemperatureLog)
        .filter(
            TemperatureLog.storage_unit_id == storage_unit_id
        )
        .order_by(
            TemperatureLog.recorded_at.desc()
        )
        .first()
    )

    active_alerts = (
        db.query(Alert)
        .filter(
            Alert.storage_unit_id == storage_unit_id,
            Alert.status == "Active"
        )
        .count()
    )

    temperature_status = "No Data"

    if latest_temperature is not None:
        if latest_temperature.temperature < storage_unit.min_temp:
            temperature_status = "Below Range"
        elif latest_temperature.temperature > storage_unit.max_temp:
            temperature_status = "Above Range"
        else:
            temperature_status = "Normal"

    return {
        "storage_unit_id": storage_unit.id,
        "storage_unit_name": storage_unit.name,
        "status": storage_unit.status,
        "min_temp": storage_unit.min_temp,
        "max_temp": storage_unit.max_temp,
        "latest_temperature": (
            {
                "temperature": latest_temperature.temperature,
                "humidity": latest_temperature.humidity,
                "recorded_at": latest_temperature.recorded_at,
                "source": latest_temperature.source,
            }
            if latest_temperature is not None
            else None
        ),
        "temperature_status": temperature_status,
        "active_alerts": active_alerts,
    }


@router.get(
    "/{storage_unit_id}/temperature-history",
    response_model=list[TemperatureLogResponse]
)
def get_temperature_history(
    storage_unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    storage_unit = (
        db.query(StorageUnit)
        .filter(StorageUnit.id == storage_unit_id)
        .first()
    )

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    temperature_logs = (
        db.query(TemperatureLog)
        .filter(
            TemperatureLog.storage_unit_id == storage_unit_id
        )
        .order_by(
            TemperatureLog.recorded_at.desc()
        )
        .limit(20)
        .all()
    )

    return temperature_logs