from datetime import datetime

from pydantic import BaseModel, Field


class TeamCreate(BaseModel):
    """Schema for creating a team."""

    team_name: str = Field(..., max_length=120)
    hackathon_id: int


class TeamJoin(BaseModel):
    """Schema for joining a team."""

    user_id: int


class TeamUpdate(BaseModel):
    """Schema for editing a team within the allowed edit window."""

    team_name: str = Field(..., max_length=120)
    hackathon_id: int


class TeamResponse(TeamCreate):
    """Schema for returning team data."""

    id: int
    created_at: datetime
    created_by_user_id: int | None = None
    member_count: int = 0
    is_member: bool = False

    class Config:
        from_attributes = True
