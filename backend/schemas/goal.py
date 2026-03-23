from datetime import date

from pydantic import BaseModel, Field


class CampusGoalCreate(BaseModel):
    """Schema for creating or updating campus goals."""

    title: str = Field(..., max_length=200)
    description: str
    target_energy: int = Field(..., ge=1)
    reward_points: int = Field(default=0, ge=0)
    start_date: date
    end_date: date
    status: str = Field(default="active", max_length=30)


class CampusGoalResponse(CampusGoalCreate):
    """Schema for returning campus goals."""

    id: int
    current_energy: int

    class Config:
        from_attributes = True
