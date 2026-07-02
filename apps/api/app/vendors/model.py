from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    gst_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    