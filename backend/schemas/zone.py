from pydantic import BaseModel, Field


class CampusZoneBase(BaseModel):
    """Shared fields for campus zones."""

    name: str = Field(..., max_length=120)
    description: str | None = None
    location_coordinates: str | None = None


class CampusZoneCreate(CampusZoneBase):
    """Schema for creating a campus zone."""


class CampusZoneResponse(CampusZoneBase):
    """Schema for returning campus zone data."""

    id: int

    class Config:
        from_attributes = True
