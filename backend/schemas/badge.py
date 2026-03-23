from datetime import datetime

from pydantic import BaseModel


class BadgeResponse(BaseModel):
    """Schema for returning badge definitions."""

    badge_name: str
    description: str
    points_required: int

    class Config:
        from_attributes = True


class UserBadgeResponse(BadgeResponse):
    """Schema for returning badges earned by a user."""

    earned_at: datetime
