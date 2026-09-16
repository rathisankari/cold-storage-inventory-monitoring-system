from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    old_values: dict | None = None,
    new_values: dict | None = None,
    ip_address: str | None = None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log