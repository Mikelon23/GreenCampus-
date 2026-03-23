from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import require_admin
from backend.config.database import get_db
from backend.schemas.hackathon import HackathonCreate, HackathonResponse
from backend.services.hackathons import create_hackathon, list_hackathons

router = APIRouter(prefix="/api/hackathons", tags=["hackathons"])


@router.get("", response_model=list[HackathonResponse])
def get_hackathons(
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[HackathonResponse]:
    """Return available sustainability hackathons."""
    return list_hackathons(db, limit, offset)


@router.post("", response_model=HackathonResponse, status_code=201, dependencies=[Depends(require_admin)])
def create_hackathon_endpoint(
    payload: HackathonCreate, db: Session = Depends(get_db)
) -> HackathonResponse:
    """Create a new hackathon event (admin only)."""
    return create_hackathon(db, payload)
