from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dialog_id: Mapped[int] = mapped_column(ForeignKey("dialogs.id"), index=True)
    sender: Mapped[str] = mapped_column(String(16))  # user|bot|buyer
    text: Mapped[str] = mapped_column(String(8192))
    is_llm: Mapped[bool] = mapped_column(Boolean, default=False)

    dialog = relationship("Dialog", back_populates="messages")