from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models import (
    CampusGoal,
    EcoEnergy,
    EnergyInteraction,
    GoalContribution,
    User,
    UserTree,
)
from backend.utils.errors import forbidden, not_found

ENERGY_EXPIRY_HOURS = 24
TREE_STAGES = [
    (0, "seed"),
    (120, "sprout"),
    (300, "sapling"),
    (650, "young-canopy"),
    (1100, "forest-guardian"),
]


def _resolve_tree_stage(total_energy: int) -> str:
    stage = TREE_STAGES[0][1]
    for threshold, candidate in TREE_STAGES:
        if total_energy >= threshold:
            stage = candidate
    return stage


def ensure_user_tree(db: Session, user_id: int) -> UserTree:
    """Create the player's tree profile if it does not yet exist."""
    tree = db.query(UserTree).filter(UserTree.user_id == user_id).first()
    if tree:
        return tree
    tree = UserTree(user_id=user_id)
    db.add(tree)
    db.commit()
    db.refresh(tree)
    return tree


def expire_energy(db: Session) -> None:
    """Mark stale energy drops as expired before any forest interaction."""
    now = datetime.utcnow()
    (
        db.query(EcoEnergy)
        .filter(EcoEnergy.status == "available", EcoEnergy.expires_at < now)
        .update({EcoEnergy.status: "expired"}, synchronize_session=False)
    )
    db.commit()


def create_energy_drop(
    db: Session,
    owner_user_id: int,
    amount: int,
    source_type: str,
    source_ref_id: int | None = None,
) -> EcoEnergy:
    """Generate collectible energy for a user after a sustainable action."""
    drop = EcoEnergy(
        owner_user_id=owner_user_id,
        amount=amount,
        source_type=source_type,
        source_ref_id=source_ref_id,
        status="available",
        available_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(hours=ENERGY_EXPIRY_HOURS),
    )
    db.add(drop)
    db.commit()
    db.refresh(drop)
    return drop


def _update_active_goals(db: Session, user_id: int, amount: int) -> None:
    active_goals = db.query(CampusGoal).filter(CampusGoal.status == "active").all()
    for goal in active_goals:
        goal.current_energy += amount
        db.add(GoalContribution(goal_id=goal.id, user_id=user_id, amount=amount))
        if goal.current_energy >= goal.target_energy:
            goal.current_energy = goal.target_energy
            goal.status = "completed"


def apply_energy_to_tree(db: Session, user_id: int, amount: int) -> UserTree:
    """Convert collected energy into tree growth and shared campus progress."""
    tree = ensure_user_tree(db, user_id)
    tree.growth_points += amount
    tree.total_energy_contributed += amount
    tree.stage = _resolve_tree_stage(tree.total_energy_contributed)
    _update_active_goals(db, user_id, amount)
    db.commit()
    db.refresh(tree)
    return tree


def update_daily_streak(db: Session, user_id: int) -> int:
    """Update streak state whenever a user performs a green action."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")

    now = datetime.utcnow()
    today = now.date()
    last_date = user.last_green_action_at.date() if user.last_green_action_at else None

    if last_date == today:
        return user.current_streak
    if last_date == today - timedelta(days=1):
        user.current_streak += 1
    else:
        user.current_streak = 1
    user.best_streak = max(user.best_streak, user.current_streak)
    user.last_green_action_at = now
    db.commit()
    return user.current_streak


def grant_daily_streak_bonus(db: Session, user_id: int, streak: int) -> EcoEnergy | None:
    """Reward users for consistency on meaningful streak milestones."""
    milestone_bonus = {3: 20, 5: 35, 7: 50, 14: 90}
    bonus = milestone_bonus.get(streak)
    if not bonus:
        return None
    return create_energy_drop(db, user_id, bonus, "daily-streak")


def collect_energy(db: Session, energy_id: int, actor_user_id: int) -> EcoEnergy:
    """Collect the player's own energy before it expires."""
    expire_energy(db)
    drop = db.query(EcoEnergy).filter(EcoEnergy.id == energy_id).first()
    if not drop:
        raise not_found("Energy drop not found")
    if drop.owner_user_id != actor_user_id:
        raise forbidden("You can only collect your own energy")
    if drop.status != "available":
        raise forbidden("This energy is no longer available")

    drop.status = "collected"
    drop.collected_at = datetime.utcnow()
    db.add(EnergyInteraction(
        energy_id=drop.id,
        actor_user_id=actor_user_id,
        target_user_id=drop.owner_user_id,
        interaction_type="collect",
        amount=drop.amount,
    ))
    apply_energy_to_tree(db, actor_user_id, drop.amount)
    db.commit()
    db.refresh(drop)
    return drop


def help_collect_energy(db: Session, energy_id: int, actor_user_id: int) -> EcoEnergy:
    """Allow one player to help another secure an available energy drop."""
    expire_energy(db)
    drop = db.query(EcoEnergy).filter(EcoEnergy.id == energy_id).first()
    if not drop:
        raise not_found("Energy drop not found")
    if drop.owner_user_id == actor_user_id:
        raise forbidden("Use collect for your own energy")
    if drop.status != "available":
        raise forbidden("This energy is no longer available")

    bonus_for_helper = max(5, round(drop.amount * 0.2))
    drop.status = "helped"
    drop.collected_at = datetime.utcnow()
    db.add(EnergyInteraction(
        energy_id=drop.id,
        actor_user_id=actor_user_id,
        target_user_id=drop.owner_user_id,
        interaction_type="help",
        amount=drop.amount,
    ))
    apply_energy_to_tree(db, drop.owner_user_id, drop.amount)
    create_energy_drop(db, actor_user_id, bonus_for_helper, "social-help", drop.id)
    db.commit()
    db.refresh(drop)
    return drop


def rescue_energy(db: Session, energy_id: int, actor_user_id: int) -> EcoEnergy:
    """Let another user rescue a portion of unattended energy for themselves."""
    expire_energy(db)
    drop = db.query(EcoEnergy).filter(EcoEnergy.id == energy_id).first()
    if not drop:
        raise not_found("Energy drop not found")
    if drop.owner_user_id == actor_user_id:
        raise forbidden("You cannot rescue your own energy")
    if drop.status != "available":
        raise forbidden("This energy is no longer available")

    rescued_amount = max(5, round(drop.amount * 0.4))
    drop.status = "rescued"
    drop.collected_at = datetime.utcnow()
    db.add(EnergyInteraction(
        energy_id=drop.id,
        actor_user_id=actor_user_id,
        target_user_id=drop.owner_user_id,
        interaction_type="rescue",
        amount=rescued_amount,
    ))
    apply_energy_to_tree(db, actor_user_id, rescued_amount)
    db.commit()
    db.refresh(drop)
    return drop


def get_social_forest(db: Session, user_id: int, limit: int = 8) -> list[dict]:
    """Build playful peer cards showing who has energy available."""
    expire_energy(db)
    available_subquery = (
        db.query(EcoEnergy.owner_user_id, func.sum(EcoEnergy.amount).label("available_energy"))
        .filter(EcoEnergy.status == "available")
        .group_by(EcoEnergy.owner_user_id)
        .subquery()
    )
    rows = (
        db.query(
            User.id,
            User.name,
            User.current_streak,
            UserTree.stage,
            func.coalesce(available_subquery.c.available_energy, 0).label("available_energy"),
        )
        .outerjoin(UserTree, UserTree.user_id == User.id)
        .outerjoin(available_subquery, available_subquery.c.owner_user_id == User.id)
        .filter(User.id != user_id)
        .order_by(func.coalesce(available_subquery.c.available_energy, 0).desc(), User.current_streak.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "user_id": row.id,
            "name": row.name,
            "tree_stage": row.stage or "seed",
            "available_energy": int(row.available_energy or 0),
            "current_streak": row.current_streak,
        }
        for row in rows
    ]


def get_social_energy(db: Session, user_id: int, limit: int = 8) -> list[dict]:
    """Expose available energy drops from other users for help or rescue loops."""
    expire_energy(db)
    rows = (
        db.query(EcoEnergy, User.name)
        .join(User, User.id == EcoEnergy.owner_user_id)
        .filter(EcoEnergy.owner_user_id != user_id, EcoEnergy.status == "available")
        .order_by(EcoEnergy.available_at.asc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": drop.id,
            "owner_user_id": drop.owner_user_id,
            "source_type": drop.source_type,
            "source_ref_id": drop.source_ref_id,
            "amount": drop.amount,
            "status": drop.status,
            "available_at": drop.available_at,
            "expires_at": drop.expires_at,
            "collected_at": drop.collected_at,
            "owner_name": owner_name,
        }
        for drop, owner_name in rows
    ]


def get_ecoverse_overview(db: Session, user_id: int) -> dict:
    """Aggregate the forest game state for a single user."""
    expire_energy(db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")
    tree = ensure_user_tree(db, user_id)
    available = (
        db.query(EcoEnergy)
        .filter(EcoEnergy.owner_user_id == user_id, EcoEnergy.status == "available")
        .order_by(EcoEnergy.available_at.asc())
        .all()
    )
    available_total = sum(drop.amount for drop in available)
    goals = db.query(CampusGoal).order_by(CampusGoal.end_date.asc()).all()
    return {
        "user_id": user.id,
        "current_streak": user.current_streak,
        "best_streak": user.best_streak,
        "available_energy_total": available_total,
        "collectable_energy": available,
        "tree": tree,
        "campus_goals": goals,
        "social_forest": get_social_forest(db, user_id),
        "social_energy": get_social_energy(db, user_id),
    }
