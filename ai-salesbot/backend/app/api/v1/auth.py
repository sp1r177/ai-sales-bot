from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...core.security import create_access_token, create_refresh_token, decode_token
from ...db.session import SessionLocal
from ...models.plan import Plan
from ...models.user import User
from ...schemas.auth import LoginRequest, TokenPair

router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=TokenPair)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    # MVP: authenticate by vk_user_id without signature
    user = db.query(User).filter(User.vk_user_id == req.vk_user_id).first()
    if user is None:
        user = User(vk_user_id=req.vk_user_id, role="owner")
        db.add(user)
        db.commit()
        db.refresh(user)
        # provision default Free plan
        plan = Plan(user_id=user.id, tier="free", bots_limit=1, dialogs_limit=5)
        db.add(plan)
        db.commit()

    access = create_access_token(user.vk_user_id)
    refresh = create_refresh_token(user.vk_user_id)
    return TokenPair(access=access, refresh=refresh)


@router.post("/refresh", response_model=TokenPair)
def refresh(token: TokenPair):
    payload = decode_token(token.refresh)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    sub = payload.get("sub")
    access = create_access_token(sub)
    refresh_new = create_refresh_token(sub)
    return TokenPair(access=access, refresh=refresh_new)