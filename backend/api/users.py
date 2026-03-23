from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import require_admin
from backend.config.database import get_db
from backend.models import User
from backend.schemas.user import UserCreate, UserResponse
from backend.services.users import create_user, list_users
from backend.utils.errors import not_found

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[UserResponse]:
    """Return a list of users."""
    return list_users(db, limit, offset)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    """Return a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")
    return user


@router.post("", response_model=UserResponse, status_code=201)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """Create a new user."""
    return create_user(db, payload)


@router.delete("/{user_id}", status_code=200, dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a user account (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")
    db.delete(user)
    db.commit()
