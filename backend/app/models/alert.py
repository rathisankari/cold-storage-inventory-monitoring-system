from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    storage_unit_id: Mapped[int] = mapped_column(
        nullable=False
    )

    alert_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Active"
    )

    acknowledged_by: Mapped[int | None] = mapped_column(
        nullable=True
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )