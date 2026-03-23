from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from backend.config.database import get_db
from backend.models import User
from backend.utils.errors import unauthorized, forbidden
from backend.utils.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Resolve the current user from the JWT token."""
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
    except JWTError:
        raise unauthorized("Invalid authentication token")
    if not subject:
        raise unauthorized("Invalid authentication token")
    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise unauthorized("User not found")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    """Ensure the current user has admin role."""
    if user.role.lower() != "admin":
        raise forbidden("Admin access required")
    return user


def ensure_self_or_admin(current_user: User, target_user_id: int) -> User:
    """Allow access to a personal resource only to its owner or an admin."""
    if current_user.role.lower() == "admin" or current_user.id == target_user_id:
        return current_user
    raise forbidden("You do not have access to this resource")
