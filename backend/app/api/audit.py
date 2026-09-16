from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_roles
from app.models.audit_log import AuditLog
from app.models.user import User


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get("/")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("Admin")
    )
):
    audit_logs = (
        db.query(AuditLog)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return audit_logs