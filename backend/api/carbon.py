from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import ensure_self_or_admin, get_current_user
from backend.config.database import get_db
from backend.models import CarbonFootprint
from backend.models import User
from backend.schemas.carbon import CarbonFootprintCreate, CarbonFootprintResponse, CarbonFootprintUpdate
from backend.services.carbon import create_carbon_record, list_carbon_records
from backend.utils.editing import ensure_editable
from backend.utils.errors import not_found

router = APIRouter(prefix="/api/carbon", tags=["carbon"])


@router.get("/{user_id}", response_model=list[CarbonFootprintResponse])
def get_carbon(
    user_id: int,
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
    current_user: User = Depends(get_current_user),
) -> list[CarbonFootprintResponse]:
    """Return carbon footprint records for a user."""
    ensure_self_or_admin(current_user, user_id)
    return list_carbon_records(db, user_id, limit, offset)


@router.post("", response_model=CarbonFootprintResponse, status_code=201)
def create_carbon(
    payload: CarbonFootprintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CarbonFootprintResponse:
    """Register a carbon footprint activity."""
    ensure_self_or_admin(current_user, payload.user_id)
    return create_carbon_record(db, payload)


@router.put("/{record_id}", response_model=CarbonFootprintResponse)
def update_carbon(
    record_id: int,
    payload: CarbonFootprintUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CarbonFootprintResponse:
    """Update a personal carbon entry during the edit window."""
    record = db.query(CarbonFootprint).filter(CarbonFootprint.id == record_id).first()
    if not record:
        raise not_found("Carbon record not found")
    ensure_self_or_admin(current_user, record.user_id)
    ensure_editable(record.recorded_at, current_user.role.lower() == "admin")
    record.activity_type = payload.activity_type
    record.carbon_emission_estimate = payload.carbon_emission_estimate
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=200)
def delete_carbon(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a personal carbon entry during the edit window."""
    record = db.query(CarbonFootprint).filter(CarbonFootprint.id == record_id).first()
    if not record:
        raise not_found("Carbon record not found")
    ensure_self_or_admin(current_user, record.user_id)
    ensure_editable(record.recorded_at, current_user.role.lower() == "admin")
    db.delete(record)
    db.commit()
