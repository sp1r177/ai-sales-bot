from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class BotBase(BaseModel):
    name: str
    description: str
    characteristics: dict = Field(default_factory=dict)
    images: list[str] = Field(default_factory=list)
    price: float = 0.0
    discount_percent: float = 0.0
    wholesale_price: float = 0.0
    pay_url: Optional[str] = None
    pay_url_discount: Optional[str] = None
    bargaining_style: str = "standard"
    faq: list[str] = Field(default_factory=list)
    model_preset: Optional[str] = None


class BotCreate(BotBase):
    pass


class BotUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    characteristics: Optional[dict] = None
    images: Optional[list[str]] = None
    price: Optional[float] = None
    discount_percent: Optional[float] = None
    wholesale_price: Optional[float] = None
    pay_url: Optional[str] = None
    pay_url_discount: Optional[str] = None
    bargaining_style: Optional[str] = None
    faq: Optional[list[str]] = None
    model_preset: Optional[str] = None


class BotRead(BotBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True