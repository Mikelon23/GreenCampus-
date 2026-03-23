from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import ensure_self_or_admin, get_current_user
from backend.config.database import get_db
from backend.models import User
from backend.schemas.ecoverse import EcoverseOverviewResponse
from backend.services.ecoverse import collect_energy, get_ecoverse_overview, help_collect_energy, rescue_energy

router = APIRouter(prefix="/api/ecoverse", tags=["ecoverse"])


@router.get("/overview/{user_id}", response_model=EcoverseOverviewResponse)
def get_overview(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EcoverseOverviewResponse:
    """Return the game-oriented sustainability overview for a user."""
    ensure_self_or_admin(current_user, user_id)
    return get_ecoverse_overview(db, user_id)


@router.post("/energy/{energy_id}/collect")
def collect_energy_endpoint(
    energy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Collect the user's own energy drop."""
    drop = collect_energy(db, energy_id, current_user.id)
    return {"energy_id": drop.id, "status": drop.status, "amount": drop.amount}


@router.post("/energy/{energy_id}/help")
def help_energy_endpoint(
    energy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Help another user secure an energy drop and earn a helper bonus."""
    drop = help_collect_energy(db, energy_id, current_user.id)
    return {"energy_id": drop.id, "status": drop.status, "amount": drop.amount}


@router.post("/energy/{energy_id}/rescue")
def rescue_energy_endpoint(
    energy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Rescue part of an unattended energy drop from another user."""
    drop = rescue_energy(db, energy_id, current_user.id)
    return {"energy_id": drop.id, "status": drop.status, "amount": drop.amount}
