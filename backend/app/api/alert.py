from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.alert import Alert
from app.models.user import User
from app.schemas.alert import AlertResponse
from app.services.audit_service import create_audit_log


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/", response_model=list[AlertResponse])
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    alerts = (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )

    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


@router.put("/{alert_id}/acknowledge", response_model=AlertResponse)
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin", "Storage Operator")
    )
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    if alert.status == "Acknowledged":
        raise HTTPException(
            status_code=400,
            detail="Alert is already acknowledged"
        )

    if alert.status == "Resolved":
        raise HTTPException(
            status_code=400,
            detail="Resolved alert cannot be acknowledged"
        )

    old_status = alert.status

    alert.status = "Acknowledged"
    alert.acknowledged_by = current_user.id
    alert.acknowledged_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="ACKNOWLEDGE_ALERT",
        resource_type="Alert",
        resource_id=str(alert.id),
        old_values={
            "status": old_status
        },
        new_values={
            "status": "Acknowledged"
        }
    )

    return alert