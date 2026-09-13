from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TemperatureLog(Base):
    __tablename__ = "temperature_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    storage_unit_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    humidity: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    recorded_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.utcnow,
    nullable=False
    )

    source: Mapped[str | None] = mapped_column(
        String(50),
        default="IoT_Sensor",
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=datetime.utcnow,
    nullable=False
    )