from datetime import datetime

from sqlalchemy.orm import Session

from backend.models import Badge, EcoAction, GreenPoints, User, UserBadge
from backend.services.ecoverse import create_energy_drop, grant_daily_streak_bonus, update_daily_streak
from backend.utils.errors import not_found

DEFAULT_ACTION_POINTS = {
    "cycling to campus": 60,
    "walking to campus": 50,
    "using public transport": 40,
    "reusing water bottle": 20,
    "recycling paper": 30,
    "composting food waste": 35,
    "reducing energy at home": 45,
    "submit a greenhack project": 50,
    "join tree-planting campaign": 40,
    "public transport commute": 45,
    "refill station visit": 20,
    "waste sorting": 35,
    "lab energy shutdown": 40,
}

DEFAULT_BADGES = [
    {"badge_name": "Eco Starter", "description": "Earn first 50 points", "points_required": 50},
    {"badge_name": "Green Contributor", "description": "Earn 200 points", "points_required": 200},
    {"badge_name": "Sustainability Champion", "description": "Earn 500 points", "points_required": 500},
    {
        "badge_name": "Innovation Leader",
        "description": "Submit a GreenHack project",
        "points_required": 0,
    },
]


def _normalize_action(action_type: str) -> str:
    """Normalize action type strings to match point rules."""
    return action_type.strip().lower()


def ensure_default_badges(db: Session) -> None:
    """Ensure the default badge definitions exist."""
    existing = {badge.badge_name for badge in db.query(Badge).all()}
    for badge_data in DEFAULT_BADGES:
        if badge_data["badge_name"] in existing:
            continue
        badge = Badge(**badge_data)
        db.add(badge)
    db.commit()


def record_eco_action(db: Session, user_id: int, action_type: str) -> EcoAction:
    """Record an eco-action, assign points, and update badges."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")

    ensure_default_badges(db)

    normalized = _normalize_action(action_type)
    points = DEFAULT_ACTION_POINTS.get(normalized, 0)
    action = EcoAction(user_id=user_id, action_type=action_type, points_awarded=points)
    db.add(action)

    points_record = db.query(GreenPoints).filter(GreenPoints.user_id == user_id).first()
    if not points_record:
        points_record = GreenPoints(user_id=user_id, total_points=0, last_updated=datetime.utcnow())
        db.add(points_record)

    points_record.total_points += points
    points_record.last_updated = datetime.utcnow()

    _evaluate_badges(db, user_id, points_record.total_points)

    db.commit()
    db.refresh(action)

    energy_amount = max(10, round(points * 0.8)) if points > 0 else 10
    create_energy_drop(db, user_id, energy_amount, "eco-action", action.id)
    streak = update_daily_streak(db, user_id)
    grant_daily_streak_bonus(db, user_id, streak)
    return action


def _evaluate_badges(db: Session, user_id: int, total_points: int) -> None:
    """Grant badges based on points thresholds."""
    earned_badge_ids = {
        user_badge.badge_id
        for user_badge in db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
    }
    for badge in db.query(Badge).all():
        if badge.badge_name == "Innovation Leader":
            continue
        if total_points >= badge.points_required and badge.id not in earned_badge_ids:
            db.add(UserBadge(user_id=user_id, badge_id=badge.id, earned_at=datetime.utcnow()))


def award_innovation_badge(db: Session, user_id: int) -> None:
    """Award the Innovation Leader badge when a project is submitted."""
    ensure_default_badges(db)
    badge = db.query(Badge).filter(Badge.badge_name == "Innovation Leader").first()
    if not badge:
        return
    existing = (
        db.query(UserBadge)
        .filter(UserBadge.user_id == user_id, UserBadge.badge_id == badge.id)
        .first()
    )
    if not existing:
        db.add(UserBadge(user_id=user_id, badge_id=badge.id, earned_at=datetime.utcnow()))
        db.commit()
