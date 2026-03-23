from pydantic import BaseModel, Field

from backend.schemas.user import UserResponse


class AuthRegister(BaseModel):
    """Schema for registering a user."""

    name: str = Field(..., max_length=120)
    email: str
    password: str = Field(..., min_length=8)
    role: str = Field(..., max_length=30)


class AuthLogin(BaseModel):
    """Schema for logging in a user."""

    email: str
    password: str = Field(..., min_length=8)


class AuthResponse(BaseModel):
    """Schema for returning auth tokens and user data."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse | None = None
