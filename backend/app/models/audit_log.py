from datetime import datetime

from sqlalchemy import DateTime, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    resource_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    old_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    new_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )