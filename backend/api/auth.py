from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.models import User
from backend.schemas.auth import AuthLogin, AuthRegister, AuthResponse
from backend.schemas.user import UserResponse
from backend.services.users import create_user
from backend.utils.errors import unauthorized
from backend.utils.security import create_access_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(payload: AuthRegister, db: Session = Depends(get_db)) -> AuthResponse:
    """Register a new user and return an access token."""
    user = create_user(db, payload)
    token = create_access_token(subject=user.email)
    return AuthResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: AuthLogin, db: Session = Depends(get_db)) -> AuthResponse:
    """Authenticate a user and return an access token."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise unauthorized("Invalid credentials")
    token = create_access_token(subject=user.email)
    return AuthResponse(access_token=token, user=UserResponse.model_validate(user))
