from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import ensure_self_or_admin, get_current_user
from backend.config.database import get_db
from backend.models import User
from backend.schemas.badge import BadgeResponse, UserBadgeResponse
from backend.services.gamification import ensure_default_badges
from backend.services.points import list_badges, list_user_badges

router = APIRouter(prefix="/api/badges", tags=["badges"])


@router.get("", response_model=list[BadgeResponse])
def get_badges(db: Session = Depends(get_db)) -> list[BadgeResponse]:
    """Return available sustainability badges."""
    ensure_default_badges(db)
    return list_badges(db)


@router.get("/earned/{user_id}", response_model=list[UserBadgeResponse])
def get_user_badges(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[UserBadgeResponse]:
    """Return badges earned by a specific user."""
    ensure_self_or_admin(current_user, user_id)
    return list_user_badges(db, user_id)
