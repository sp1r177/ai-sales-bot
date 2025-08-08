from __future__ import annotations

import os

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ...api.deps import get_current_user
from ...core.security import get_db
from ...models.bot import Bot
from ...models.user import User
from ...services.storage import LocalStorage

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/image")
def upload_image(
    bot_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    bot = db.query(Bot).filter(Bot.id == bot_id, Bot.owner_id == user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    storage = LocalStorage()
    filename, _ = storage.save_image(file)
    images = bot.images or []
    images.append(filename)
    bot.images = images
    db.add(bot)
    db.commit()
    return {"filename": filename, "url": f"/api/media/{filename}"}