from sqlalchemy.orm import Session

from backend.models import CampusZone
from backend.schemas.zone import CampusZoneCreate
from backend.utils.pagination import apply_pagination


def create_zone(db: Session, payload: CampusZoneCreate) -> CampusZone:
    """Create a campus zone."""
    zone = CampusZone(
        name=payload.name,
        description=payload.description,
        location_coordinates=payload.location_coordinates,
    )
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return zone


def list_zones(db: Session, limit: int | None, offset: int | None) -> list[CampusZone]:
    """Return all campus zones."""
    query = db.query(CampusZone).order_by(CampusZone.name.asc())
    query = apply_pagination(query, limit, offset)
    return query.all()
