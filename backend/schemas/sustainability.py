from datetime import datetime
from pydantic import BaseModel


class SustainabilityScoreResponse(BaseModel):
    """Schema for returning sustainability indicators."""

    zone_id: int
    sustainability_score: float
    energy_efficiency_index: float
    carbon_index: float
    calculated_at: datetime

    class Config:
        from_attributes = True
