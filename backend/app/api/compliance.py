from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.alert import Alert
from app.models.inventory import Inventory
from app.models.temperature_log import TemperatureLog
from app.models.user import User

router = APIRouter(
    prefix="/compliance-report",
    tags=["Compliance Report"]
)


def calculate_inventory_status(inventory: Inventory) -> str:
    if inventory.status == "Compromised":
        return "Compromised"

    if inventory.quantity <= 0:
        return "Depleted"

    if inventory.expiration_date <= date.today():
        return "Expired"

    return "Good"


@router.get("/")
def get_compliance_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Admin"))
):
    temperature_logs = db.query(TemperatureLog).all()
    alerts = db.query(Alert).all()
    inventory_items = db.query(Inventory).all()

    temperatures = [
        log.temperature
        for log in temperature_logs
    ]

    average_temperature = (
        sum(temperatures) / len(temperatures)
        if temperatures
        else 0
    )

    minimum_temperature = (
        min(temperatures)
        if temperatures
        else 0
    )

    maximum_temperature = (
        max(temperatures)
        if temperatures
        else 0
    )

    total_alerts = len(alerts)

    active_alerts = sum(
        1 for alert in alerts
        if alert.status == "Active"
    )

    acknowledged_alerts = sum(
        1 for alert in alerts
        if alert.status == "Acknowledged"
    )

    resolved_alerts = sum(
        1 for alert in alerts
        if alert.status == "Resolved"
    )

    inventory_summary = {
        "total_items": len(inventory_items),
        "total_quantity": sum(
            item.quantity for item in inventory_items
        ),
        "good": 0,
        "compromised": 0,
        "expired": 0,
        "depleted": 0,
        "used": 0
    }

    for item in inventory_items:
        status = calculate_inventory_status(item)

        if status == "Good":
            inventory_summary["good"] += 1

        elif status == "Compromised":
            inventory_summary["compromised"] += 1

        elif status == "Expired":
            inventory_summary["expired"] += 1

        elif status == "Depleted":
            inventory_summary["depleted"] += 1

        elif status == "Used":
            inventory_summary["used"] += 1

    return {
        "report_date": date.today(),
        "temperature_summary": {
            "total_readings": len(temperature_logs),
            "average_temperature": round(
                average_temperature,
                2
            ),
            "minimum_temperature": minimum_temperature,
            "maximum_temperature": maximum_temperature
        },
        "alert_summary": {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "acknowledged_alerts": acknowledged_alerts,
            "resolved_alerts": resolved_alerts
        },
        "inventory_summary": inventory_summary
    }