from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import ensure_self_or_admin, get_current_user
from backend.config.database import get_db
from backend.models import Team, User
from backend.schemas.team import TeamCreate, TeamJoin, TeamResponse, TeamUpdate
from backend.services.hackathons import create_team, join_team, list_teams
from backend.utils.editing import ensure_editable
from backend.utils.errors import forbidden
from backend.utils.errors import not_found

router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.get("", response_model=list[TeamResponse])
def get_teams(
    db: Session = Depends(get_db),
    hackathon_id: int | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
    current_user: User = Depends(get_current_user),
) -> list[TeamResponse]:
    """Return teams, optionally filtered by hackathon."""
    return list_teams(db, current_user.id, hackathon_id, limit, offset)


@router.post("", response_model=TeamResponse, status_code=201)
def create_team_endpoint(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TeamResponse:
    """Create a team for a hackathon."""
    return create_team(db, payload, current_user.id)


@router.post("/{team_id}/join", status_code=201)
def join_team_endpoint(
    team_id: int,
    payload: TeamJoin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Add a user to a team."""
    ensure_self_or_admin(current_user, payload.user_id)
    membership = join_team(db, team_id, payload.user_id)
    return {"team_id": membership.team_id, "user_id": membership.user_id}


@router.put("/{team_id}", response_model=TeamResponse)
def update_team_endpoint(
    team_id: int,
    payload: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TeamResponse:
    """Allow the team creator to edit the team for 30 minutes."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise not_found("Team not found")
    if current_user.role.lower() != "admin" and team.created_by_user_id != current_user.id:
        raise forbidden("You do not have access to this team")
    ensure_editable(team.created_at, current_user.role.lower() == "admin")
    team.team_name = payload.team_name
    team.hackathon_id = payload.hackathon_id
    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=200)
def delete_team_endpoint(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Allow the team creator to delete the team for 30 minutes."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise not_found("Team not found")
    if current_user.role.lower() != "admin" and team.created_by_user_id != current_user.id:
        raise forbidden("You do not have access to this team")
    ensure_editable(team.created_at, current_user.role.lower() == "admin")
    db.delete(team)
    db.commit()
