from datetime import datetime
from pydantic import BaseModel, Field


class CarbonFootprintCreate(BaseModel):
    """Schema for registering carbon footprint activity."""

    user_id: int
    activity_type: str = Field(..., max_length=120)
    carbon_emission_estimate: float


class CarbonFootprintUpdate(BaseModel):
    """Schema for editing a user carbon record within the edit window."""

    activity_type: str = Field(..., max_length=120)
    carbon_emission_estimate: float


class CarbonFootprintResponse(BaseModel):
    """Schema for returning carbon footprint data."""

    id: int
    user_id: int
    activity_type: str
    carbon_emission_estimate: float
    recorded_at: datetime

    class Config:
        from_attributes = True
