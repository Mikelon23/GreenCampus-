from datetime import datetime
from pydantic import BaseModel, Field


class SensorDataCreate(BaseModel):
    """Schema for creating sensor data."""

    zone_id: int
    temperature: float
    humidity: float
    co2_level: float = Field(..., alias="co2_level")
    energy_usage: float


class SensorDataResponse(BaseModel):
    """Schema for returning sensor data."""

    id: int
    zone_id: int
    temperature: float
    humidity: float
    co2_level: float
    energy_usage: float
    timestamp: datetime

    class Config:
        from_attributes = True
