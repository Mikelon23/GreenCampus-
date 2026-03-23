from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import ensure_self_or_admin, get_current_user
from backend.config.database import get_db
from backend.models import User
from backend.schemas.points import GreenPointsResponse
from backend.services.points import get_user_points

router = APIRouter(prefix="/api/points", tags=["points"])


@router.get("/{user_id}", response_model=GreenPointsResponse)
def get_points(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GreenPointsResponse:
    """Return the total green points of a user."""
    ensure_self_or_admin(current_user, user_id)
    return get_user_points(db, user_id)
