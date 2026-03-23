from datetime import datetime
from pydantic import BaseModel, Field


class EcoActionCreate(BaseModel):
    """Schema for registering an eco-action."""

    user_id: int
    action_type: str = Field(..., max_length=120)


class EcoActionUpdate(BaseModel):
    """Schema for editing a user eco-action within the edit window."""

    action_type: str = Field(..., max_length=120)


class EcoActionResponse(BaseModel):
    """Schema for returning eco-actions."""

    id: int
    user_id: int
    action_type: str
    points_awarded: int
    timestamp: datetime

    class Config:
        from_attributes = True
