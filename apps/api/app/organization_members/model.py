from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )