from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    storage_unit_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    vaccine_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    vaccine_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    lot_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    expiration_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    received_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Good",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )