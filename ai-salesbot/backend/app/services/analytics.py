from __future__ import annotations

from sqlalchemy.orm import Session
from ..models.dialog import Dialog


def get_overview(db: Session) -> dict:
    total_dialogs = db.query(Dialog).count()
    paid_dialogs = db.query(Dialog).filter(Dialog.status == "paid").count()
    conversion = (paid_dialogs / total_dialogs) * 100 if total_dialogs else 0.0
    avg_discount = db.query(Dialog).filter(Dialog.discount_granted_percent.isnot(None)).all()
    if avg_discount:
        avg = sum(d.discount_granted_percent or 0 for d in avg_discount) / len(avg_discount)
    else:
        avg = 0.0
    return {
        "total_dialogs": total_dialogs,
        "paid_dialogs": paid_dialogs,
        "conversion_percent": round(conversion, 2),
        "avg_discount_percent": round(avg, 2),
    }