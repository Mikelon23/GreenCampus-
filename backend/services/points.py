from sqlalchemy.orm import Session

from backend.models import Badge, GreenPoints, User, UserBadge
from backend.utils.errors import not_found


def get_user_points(db: Session, user_id: int) -> GreenPoints:
    """Return total points for a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")

    points = db.query(GreenPoints).filter(GreenPoints.user_id == user_id).first()
    if not points:
        points = GreenPoints(user_id=user_id, total_points=0)
        db.add(points)
        db.commit()
        db.refresh(points)
    return points


def list_badges(db: Session) -> list[Badge]:
    """Return available badges."""
    return db.query(Badge).order_by(Badge.points_required.asc()).all()


def list_user_badges(db: Session, user_id: int) -> list[dict]:
    """Return badges earned by a specific user."""
    rows = (
        db.query(UserBadge, Badge)
        .join(Badge, Badge.id == UserBadge.badge_id)
        .filter(UserBadge.user_id == user_id)
        .order_by(UserBadge.earned_at.desc())
        .all()
    )
    return [
        {
            "badge_name": badge.badge_name,
            "description": badge.description,
            "points_required": badge.points_required,
            "earned_at": user_badge.earned_at,
        }
        for user_badge, badge in rows
    ]


def list_leaderboard(db: Session) -> list[tuple[int, str, int]]:
    """Return leaderboard data."""
    data = (
        db.query(User.id, User.name, GreenPoints.total_points)
        .join(GreenPoints, GreenPoints.user_id == User.id)
        .order_by(GreenPoints.total_points.desc())
        .all()
    )
    return [(row.id, row.name, row.total_points) for row in data]
