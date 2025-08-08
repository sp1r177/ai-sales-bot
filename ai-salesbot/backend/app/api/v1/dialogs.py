from __future__ import annotations

import calendar
import datetime as dt

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...api.deps import get_current_user
from ...core.security import get_db
from ...models.bot import Bot
from ...models.dialog import Dialog
from ...models.message import Message
from ...models.user import User
from ...schemas.dialog import DialogRead, DialogStartRequest
from ...schemas.message import MessageCreate, MessageRead
from ...services.faq import format_faq_bullets
from ...services.llm.factory import get_llm_provider

router = APIRouter(prefix="/dialogs", tags=["dialogs"])


def _build_messages(bot: Bot, user_text: str) -> list[dict]:
    faq_text = format_faq_bullets(bot.faq or [])
    system = (
        f"Ты продающий чат-бот. Товар: {bot.name}. Описание: {bot.description}.\n"
        f"Характеристики: {bot.characteristics}.\n"
        f"Стиль торга: {bot.bargaining_style} (держись этого стиля).\n"
        f"Цены: базовая {bot.price}, скидка до {bot.discount_percent}%, опт {bot.wholesale_price}.\n"
        f"Правило: никогда не давай скидку ниже {bot.discount_percent}%.\n"
        + (f"FAQ/Возражения:\n{faq_text}\n" if faq_text else "")
    )
    assistant = "Следуй правилам торга и не превышай максимальную скидку. Будь вежлив и краток."
    return [
        {"role": "system", "content": system},
        {"role": "assistant", "content": assistant},
        {"role": "user", "content": user_text},
    ]


@router.post("/start", response_model=DialogRead)
def start_dialog(payload: DialogStartRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    bot = db.query(Bot).filter(Bot.id == payload.bot_id, Bot.owner_id == user.id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # enforce monthly dialog limits based on user's latest plan
    plan = user.plans[-1] if user.plans else None
    dialogs_limit = plan.dialogs_limit if plan else 5
    now = dt.datetime.utcnow()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    count = (
        db.query(Dialog)
        .filter(Dialog.bot_id.in_([b.id for b in user.bots]))
        .filter(Dialog.created_at >= first_day)
        .count()
    )
    if count >= dialogs_limit:
        raise HTTPException(status_code=400, detail="Dialogs limit reached for this month")

    dialog = Dialog(bot_id=bot.id, buyer_vk_id=payload.buyer_vk_id, status="open")
    db.add(dialog)
    db.commit()
    db.refresh(dialog)
    return dialog


@router.post("/{dialog_id}/message", response_model=MessageRead)
def post_message(dialog_id: int, payload: MessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dialog = (
        db.query(Dialog)
        .join(Bot, Dialog.bot_id == Bot.id)
        .filter(Dialog.id == dialog_id, Bot.owner_id == user.id)
        .first()
    )
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")

    # save user message
    m_user = Message(dialog_id=dialog.id, sender="buyer", text=payload.text, is_llm=False)
    db.add(m_user)

    bot = db.query(Bot).filter(Bot.id == dialog.bot_id).first()
    provider = get_llm_provider()
    messages = _build_messages(bot, payload.text)
    reply_text = provider.generate(messages)

    m_bot = Message(dialog_id=dialog.id, sender="bot", text=reply_text, is_llm=True)
    db.add(m_bot)
    db.commit()
    db.refresh(m_bot)
    return m_bot


@router.get("/{dialog_id}", response_model=list[MessageRead])
def get_dialog(dialog_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    dialog = (
        db.query(Dialog)
        .join(Bot, Dialog.bot_id == Bot.id)
        .filter(Dialog.id == dialog_id, Bot.owner_id == user.id)
        .first()
    )
    if not dialog:
        raise HTTPException(status_code=404, detail="Dialog not found")
    messages = db.query(Message).filter(Message.dialog_id == dialog.id).order_by(Message.created_at.asc()).all()
    return messages