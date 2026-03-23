from datetime import date
from pydantic import BaseModel, Field


class HackathonCreate(BaseModel):
    """Schema for creating hackathons."""

    title: str = Field(..., max_length=200)
    description: str
    start_date: date
    end_date: date
    status: str = Field(..., max_length=50)


class HackathonResponse(HackathonCreate):
    """Schema for returning hackathon data."""

    id: int

    class Config:
        from_attributes = True
