from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from backend.api.deps import ensure_self_or_admin, get_current_user
from backend.config.database import get_db
from backend.models import EcoAction, User
from backend.schemas.action import EcoActionCreate, EcoActionResponse, EcoActionUpdate
from backend.services.gamification import record_eco_action
from backend.utils.editing import ensure_editable
from backend.utils.pagination import apply_pagination
from backend.utils.errors import not_found

router = APIRouter(prefix="/api/actions", tags=["actions"])


@router.get("/{user_id}", response_model=list[EcoActionResponse])
def get_actions(
    user_id: int,
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
    current_user: User = Depends(get_current_user),
) -> list[EcoActionResponse]:
    """Return sustainability actions performed by a user."""
    ensure_self_or_admin(current_user, user_id)
    query = db.query(EcoAction).filter(EcoAction.user_id == user_id).order_by(EcoAction.timestamp.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()


@router.post("", response_model=EcoActionResponse, status_code=201)
def create_action(
    payload: EcoActionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EcoActionResponse:
    """Register a sustainability action."""
    ensure_self_or_admin(current_user, payload.user_id)
    return record_eco_action(db, payload.user_id, payload.action_type)


@router.put("/{action_id}", response_model=EcoActionResponse)
def update_action(
    action_id: int,
    payload: EcoActionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EcoActionResponse:
    """Update a user's eco-action during the edit window."""
    action = db.query(EcoAction).filter(EcoAction.id == action_id).first()
    if not action:
        raise not_found("Action not found")
    ensure_self_or_admin(current_user, action.user_id)
    ensure_editable(action.timestamp, current_user.role.lower() == "admin")
    action.action_type = payload.action_type
    db.commit()
    db.refresh(action)
    return action


@router.delete("/{action_id}", status_code=200)
def delete_action(
    action_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a user's eco-action during the edit window."""
    action = db.query(EcoAction).filter(EcoAction.id == action_id).first()
    if not action:
        raise not_found("Action not found")
    ensure_self_or_admin(current_user, action.user_id)
    ensure_editable(action.timestamp, current_user.role.lower() == "admin")
    db.delete(action)
    db.commit()
