from pydantic import BaseModel


class GreenPointsResponse(BaseModel):
    """Schema for returning user point totals."""

    user_id: int
    total_points: int

    class Config:
        from_attributes = True
