from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entries."""

    user_id: int
    name: str
    total_points: int
