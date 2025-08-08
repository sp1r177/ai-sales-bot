from __future__ import annotations

from sqlalchemy import Integer, String, ForeignKey, JSON, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base, TimestampMixin


class Bot(Base, TimestampMixin):
    __tablename__ = "bots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2048))
    characteristics: Mapped[dict] = mapped_column(JSON, default=dict)
    images: Mapped[list] = mapped_column(JSON, default=list)
    price: Mapped[float] = mapped_column(Float, default=0.0)
    discount_percent: Mapped[float] = mapped_column(Float, default=0.0)
    wholesale_price: Mapped[float] = mapped_column(Float, default=0.0)
    pay_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    pay_url_discount: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    bargaining_style: Mapped[str] = mapped_column(String(16), default="standard")  # soft|standard|hard
    faq: Mapped[list] = mapped_column(JSON, default=list)
    model_preset: Mapped[str | None] = mapped_column(String(255), nullable=True)

    owner = relationship("User", back_populates="bots")
    dialogs = relationship("Dialog", back_populates="bot")