from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin


class Plan(Base, TimestampMixin):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    tier: Mapped[str] = mapped_column(String(16), default="free")  # free|start|pro|business
    bots_limit: Mapped[int] = mapped_column(default=1)
    dialogs_limit: Mapped[int] = mapped_column(default=5)

    user = relationship("User", back_populates="plans")