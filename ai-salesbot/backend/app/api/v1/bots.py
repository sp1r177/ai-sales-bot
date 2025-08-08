from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...api.deps import get_current_user
from ...core.security import get_db
from ...models.bot import Bot as BotModel
from ...models.user import User
from ...schemas.bot import BotCreate, BotRead, BotUpdate

router = APIRouter(prefix="/bots", tags=["bots"])


@router.get("", response_model=list[BotRead])
def list_bots(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    bots = db.query(BotModel).filter(BotModel.owner_id == user.id).all()
    return bots


@router.post("", response_model=BotRead)
def create_bot(payload: BotCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    count = db.query(BotModel).filter(BotModel.owner_id == user.id).count()
    # Check plan limits (latest plan record)
    plan = user.plans[-1] if user.plans else None
    limit = plan.bots_limit if plan else 1
    if count >= limit:
        raise HTTPException(status_code=400, detail="Bots limit reached for your plan")
    bot = BotModel(owner_id=user.id, **payload.model_dump())
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


@router.get("/{bot_id}", response_model=BotRead)
def get_bot(bot_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    bot = db.query(BotModel).filter(BotModel.id == bot_id, BotModel.owner_id == user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot


@router.put("/{bot_id}", response_model=BotRead)
def update_bot(bot_id: int, payload: BotUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    bot = db.query(BotModel).filter(BotModel.id == bot_id, BotModel.owner_id == user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(bot, k, v)
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot


@router.delete("/{bot_id}")
def delete_bot(bot_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    bot = db.query(BotModel).filter(BotModel.id == bot_id, BotModel.owner_id == user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    db.delete(bot)
    db.commit()
    return {"detail": "deleted"}