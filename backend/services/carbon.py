from sqlalchemy.orm import Session

from backend.models import CarbonFootprint, User
from backend.schemas.carbon import CarbonFootprintCreate
from backend.utils.errors import not_found
from backend.utils.pagination import apply_pagination


def create_carbon_record(db: Session, payload: CarbonFootprintCreate) -> CarbonFootprint:
    """Create and persist a carbon footprint record."""
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise not_found("User not found")

    record = CarbonFootprint(
        user_id=payload.user_id,
        activity_type=payload.activity_type,
        carbon_emission_estimate=payload.carbon_emission_estimate,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_carbon_records(
    db: Session, user_id: int, limit: int | None, offset: int | None
) -> list[CarbonFootprint]:
    """Return carbon footprint records for a user."""
    query = db.query(CarbonFootprint).filter(CarbonFootprint.user_id == user_id)
    query = query.order_by(CarbonFootprint.recorded_at.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()
