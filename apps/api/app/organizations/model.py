from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )