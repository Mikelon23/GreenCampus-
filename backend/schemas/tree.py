from datetime import datetime
from pydantic import BaseModel, Field


class TreePlantingCreate(BaseModel):
    """Schema for registering tree planting."""

    user_id: int
    zone_id: int
    tree_species: str = Field(..., max_length=120)


class TreePlantingUpdate(BaseModel):
    """Schema for editing a tree planting record within the edit window."""

    zone_id: int
    tree_species: str = Field(..., max_length=120)


class TreePlantingResponse(BaseModel):
    """Schema for returning tree planting data."""

    id: int
    user_id: int
    zone_id: int
    tree_species: str
    planting_date: datetime

    class Config:
        from_attributes = True
