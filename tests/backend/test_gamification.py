from backend.models import User
from backend.services.gamification import record_eco_action
from backend.utils.security import hash_password


def test_record_eco_action_awards_points(db_session):
    """Ensure eco-actions update points."""
    user = User(
        name="Test User",
        email="user@example.com",
        role="student",
        password_hash=hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()

    action = record_eco_action(db_session, user.id, "walking to campus")
    assert action.points_awarded > 0

    db_session.refresh(user)
