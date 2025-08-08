from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin


class Dialog(Base, TimestampMixin):
    __tablename__ = "dialogs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bot_id: Mapped[int] = mapped_column(ForeignKey("bots.id"), index=True)
    buyer_vk_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(16), default="open")  # open|paid|closed
    discount_granted_percent: Mapped[float | None] = mapped_column(nullable=True)

    bot = relationship("Bot", back_populates="dialogs")
    messages = relationship("Message", back_populates="dialog", cascade="all, delete-orphan")