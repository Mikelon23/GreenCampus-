from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.leaderboard import LeaderboardEntry
from backend.services.points import list_leaderboard

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)) -> list[LeaderboardEntry]:
    """Return the sustainability leaderboard."""
    data = list_leaderboard(db)
    return [LeaderboardEntry(user_id=row[0], name=row[1], total_points=row[2]) for row in data]
