from __future__ import annotations

import datetime as dt
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..core.config import get_settings
from ..db.session import SessionLocal
from ..models.user import User


http_bearer = HTTPBearer(auto_error=False)


def _create_token(sub: str, expires_delta: dt.timedelta, token_type: str) -> str:
    settings = get_settings()
    now = dt.datetime.utcnow()
    payload = {
        "sub": sub,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return token


def create_access_token(sub: str) -> str:
    settings = get_settings()
    return _create_token(sub, dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access")


def create_refresh_token(sub: str) -> str:
    settings = get_settings()
    return _create_token(sub, dt.timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS), "refresh")


def decode_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer), db=Depends(get_db)) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    vk_user_id = payload.get("sub")
    if not vk_user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user: User | None = db.query(User).filter(User.vk_user_id == vk_user_id).first()
    if user is None:
        # Auto-provision on first login should create; guard here if missing
        raise HTTPException(status_code=401, detail="User not found")
    return user