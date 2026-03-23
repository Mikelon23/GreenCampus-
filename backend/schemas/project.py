from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Schema for submitting a project."""

    team_id: int
    title: str = Field(..., max_length=200)
    description: str


class ProjectUpdate(BaseModel):
    """Schema for editing a project within the allowed edit window."""

    team_id: int
    title: str = Field(..., max_length=200)
    description: str


class ProjectResponse(BaseModel):
    """Schema for returning project data."""

    id: int
    team_id: int
    title: str
    description: str
    created_by_user_id: int | None = None
    submission_date: datetime
    impact_score: float | None = None
    file_url: str | None = None

    class Config:
        from_attributes = True
