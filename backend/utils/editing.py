from datetime import datetime, timedelta

from backend.utils.errors import forbidden


EDIT_WINDOW_MINUTES = 30


def ensure_editable(created_at: datetime, is_admin: bool) -> None:
    """Allow edits only during the configured window unless the actor is an admin."""
    if is_admin:
        return
    if datetime.utcnow() > created_at.replace(tzinfo=None) + timedelta(minutes=EDIT_WINDOW_MINUTES):
        raise forbidden("This record can only be edited during the first 30 minutes")
