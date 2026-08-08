from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class StorageUnit(Base):
    __tablename__ = "storage_units"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    facility_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    unit_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    min_temp: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    max_temp: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_service_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )