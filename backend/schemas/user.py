from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Shared fields for user schemas."""

    name: str = Field(..., max_length=120)
    email: str
    role: str = Field(..., max_length=30)


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    """Schema for returning user data.

    Uses plain ``str`` for email rather than ``EmailStr`` so that Pydantic v2
    does not re-validate the value during response serialization (which can
    raise a ResponseValidationError for valid but non-standard addresses).
    """

    id: int
    name: str
    email: str  # str not EmailStr - avoid serialization validation
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
