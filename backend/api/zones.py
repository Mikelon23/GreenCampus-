from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import require_admin
from backend.config.database import get_db
from backend.schemas.zone import CampusZoneCreate, CampusZoneResponse
from backend.services.zones import create_zone, list_zones

router = APIRouter(prefix="/api/zones", tags=["zones"])


@router.get("", response_model=list[CampusZoneResponse])
def get_zones(
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[CampusZoneResponse]:
    """Return campus zones."""
    return list_zones(db, limit, offset)


@router.post("", response_model=CampusZoneResponse, status_code=201, dependencies=[Depends(require_admin)])
def create_zone_endpoint(
    payload: CampusZoneCreate, db: Session = Depends(get_db)
) -> CampusZoneResponse:
    """Create a campus zone (admin only)."""
    return create_zone(db, payload)
