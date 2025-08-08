from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...api.deps import get_current_user
from ...core.security import get_db
from ...models.plan import Plan
from ...models.user import User

router = APIRouter(prefix="/billing", tags=["billing"])


PLAN_LIMITS = {
    "free": {"bots_limit": 1, "dialogs_limit": 5},
    "start": {"bots_limit": 1, "dialogs_limit": 300},
    "pro": {"bots_limit": 3, "dialogs_limit": 1000},
    "premium": {"bots_limit": 5, "dialogs_limit": 3000},
}


@router.post("/subscribe")
def subscribe(plan: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tier = plan.lower()
    limits = PLAN_LIMITS.get(tier)
    if not limits:
        tier = "free"
        limits = PLAN_LIMITS[tier]
    new_plan = Plan(user_id=user.id, tier=tier, **limits)
    db.add(new_plan)
    db.commit()
    return {"detail": f"Switched to {tier}", **limits}