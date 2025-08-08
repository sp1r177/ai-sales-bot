from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class DialogStartRequest(BaseModel):
    bot_id: int
    buyer_vk_id: Optional[str] = None


class DialogRead(BaseModel):
    id: int
    bot_id: int
    buyer_vk_id: Optional[str]
    status: str
    discount_granted_percent: Optional[float]

    class Config:
        from_attributes = True