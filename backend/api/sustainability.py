from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.schemas.sustainability import SustainabilityScoreResponse
from backend.services.sustainability import calculate_daily_scores

router = APIRouter(prefix="/api/sustainability", tags=["sustainability"])


@router.get("", response_model=list[SustainabilityScoreResponse])
def get_sustainability(db: Session = Depends(get_db)) -> list[SustainabilityScoreResponse]:
    """Return sustainability indicators for campus zones."""
    return calculate_daily_scores(db)
