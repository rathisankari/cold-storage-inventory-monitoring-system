from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import require_roles
from app.models.alert import Alert
from app.models.storage_unit import StorageUnit
from app.models.temperature_log import TemperatureLog
from app.models.user import User
from app.schemas.temperature_log import (
    TemperatureLogCreate,
    TemperatureLogResponse,
)
from app.services.notification_service import send_critical_alert_email

router = APIRouter(
    prefix="/temperature-logs",
    tags=["Temperature Logs"]
)


@router.post("/", response_model=TemperatureLogResponse)
def create_temperature_log(
    temperature_log: TemperatureLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    storage_unit = (
        db.query(StorageUnit)
        .filter(StorageUnit.id == temperature_log.storage_unit_id)
        .first()
    )

    if storage_unit is None:
        raise HTTPException(
            status_code=404,
            detail="Storage unit not found"
        )

    new_temperature_log = TemperatureLog(
        storage_unit_id=temperature_log.storage_unit_id,
        temperature=temperature_log.temperature,
        humidity=temperature_log.humidity,
        source=temperature_log.source,
    )

    db.add(new_temperature_log)

    temperature_breach = (
        temperature_log.temperature < storage_unit.min_temp
        or temperature_log.temperature > storage_unit.max_temp
    )

    new_alert = None

    if temperature_breach:
        active_alert = (
            db.query(Alert)
            .filter(
                Alert.storage_unit_id == storage_unit.id,
                Alert.alert_type == "Temperature_Breach",
                Alert.status == "Active",
            )
            .first()
        )

        if active_alert is None:
            if temperature_log.temperature < storage_unit.min_temp:
                message = (
                    f"Temperature {temperature_log.temperature}°C is below "
                    f"the minimum allowed temperature of "
                    f"{storage_unit.min_temp}°C."
                )
            else:
                message = (
                    f"Temperature {temperature_log.temperature}°C is above "
                    f"the maximum allowed temperature of "
                    f"{storage_unit.max_temp}°C."
                )

            alert = Alert(
                storage_unit_id=storage_unit.id,
                alert_type="Temperature_Breach",
                severity="High",
                message=message,
                status="Active",
            )

            db.add(alert)
            new_alert = alert

    else:
        active_alert = (
            db.query(Alert)
            .filter(
                Alert.storage_unit_id == storage_unit.id,
                Alert.alert_type == "Temperature_Breach",
                Alert.status == "Active",
            )
            .first()
        )

        if active_alert is not None:
            active_alert.status = "Resolved"

    db.commit()
    db.refresh(new_temperature_log)

    if new_alert is not None:
        send_critical_alert_email(
            recipient_email=settings.NOTIFICATION_EMAIL,
            storage_unit_id=storage_unit.id,
            temperature=temperature_log.temperature,
            message=new_alert.message,
        )

    return new_temperature_log


@router.get("/", response_model=list[TemperatureLogResponse])
def get_temperature_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    temperature_logs = (
        db.query(TemperatureLog)
        .order_by(TemperatureLog.recorded_at.desc())
        .all()
    )

    return temperature_logs