from datetime import datetime

from pydantic import BaseModel

from backend.schemas.goal import CampusGoalResponse


class EcoEnergyResponse(BaseModel):
    """Schema for collectible energy state."""

    id: int
    owner_user_id: int
    source_type: str
    source_ref_id: int | None = None
    amount: int
    status: str
    available_at: datetime
    expires_at: datetime
    collected_at: datetime | None = None

    class Config:
        from_attributes = True


class UserTreeResponse(BaseModel):
    """Schema for the user tree shown in the eco game."""

    user_id: int
    species: str
    nickname: str
    stage: str
    growth_points: int
    total_energy_contributed: int

    class Config:
        from_attributes = True


class ForestFriendResponse(BaseModel):
    """Schema for social forest cards."""

    user_id: int
    name: str
    tree_stage: str
    available_energy: int
    current_streak: int


class SocialEnergyResponse(EcoEnergyResponse):
    """Schema for social energy interactions in the forest feed."""

    owner_name: str


class EcoverseOverviewResponse(BaseModel):
    """Schema for the eco game home screen."""

    user_id: int
    current_streak: int
    best_streak: int
    available_energy_total: int
    collectable_energy: list[EcoEnergyResponse]
    tree: UserTreeResponse
    campus_goals: list[CampusGoalResponse]
    social_forest: list[ForestFriendResponse]
    social_energy: list[SocialEnergyResponse]
