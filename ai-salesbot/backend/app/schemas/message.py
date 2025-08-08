from __future__ import annotations

from pydantic import BaseModel


class MessageCreate(BaseModel):
    text: str


class MessageRead(BaseModel):
    id: int
    sender: str
    text: str

    class Config:
        from_attributes = True