from sqlalchemy.orm import Session

from backend.models import User
from backend.schemas.user import UserCreate
from backend.utils.errors import bad_request
from backend.utils.security import hash_password
from backend.utils.pagination import apply_pagination


def create_user(db: Session, payload: UserCreate) -> User:
    """Create a user with hashed password."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise bad_request("Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        role=payload.role,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, limit: int | None, offset: int | None) -> list[User]:
    """Return a list of users with optional pagination."""
    query = db.query(User).order_by(User.created_at.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()
