from __future__ import annotations

from pydantic import BaseModel


class LoginRequest(BaseModel):
    vk_user_id: str


class TokenPair(BaseModel):
    access: str
    refresh: str