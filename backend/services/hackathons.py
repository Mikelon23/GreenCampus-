from sqlalchemy.orm import Session

from sqlalchemy import func

from backend.models import Hackathon, Project, Team, TeamMember, User
from backend.schemas.hackathon import HackathonCreate
from backend.schemas.project import ProjectCreate
from backend.schemas.team import TeamCreate
from backend.services.ecoverse import create_energy_drop
from backend.services.gamification import award_innovation_badge
from backend.utils.errors import forbidden, not_found
from backend.utils.pagination import apply_pagination


def create_hackathon(db: Session, payload: HackathonCreate) -> Hackathon:
    """Create a new hackathon event."""
    hackathon = Hackathon(
        title=payload.title,
        description=payload.description,
        start_date=payload.start_date,
        end_date=payload.end_date,
        status=payload.status,
    )
    db.add(hackathon)
    db.commit()
    db.refresh(hackathon)
    return hackathon


def list_hackathons(db: Session, limit: int | None, offset: int | None) -> list[Hackathon]:
    """List hackathon events."""
    query = db.query(Hackathon).order_by(Hackathon.start_date.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()


def create_team(db: Session, payload: TeamCreate, creator_user_id: int) -> Team:
    """Create a new hackathon team."""
    hackathon = db.query(Hackathon).filter(Hackathon.id == payload.hackathon_id).first()
    if not hackathon:
        raise not_found("Hackathon not found")

    team = Team(
        team_name=payload.team_name,
        hackathon_id=payload.hackathon_id,
        created_by_user_id=creator_user_id,
    )
    db.add(team)
    db.flush()
    db.add(TeamMember(team_id=team.id, user_id=creator_user_id))
    db.commit()
    db.refresh(team)
    return team


def list_teams(
    db: Session,
    current_user_id: int | None = None,
    hackathon_id: int | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[dict]:
    """List teams with member counts and current-user membership."""
    query = (
        db.query(
            Team.id,
            Team.team_name,
            Team.hackathon_id,
            Team.created_at,
            Team.created_by_user_id,
            func.count(TeamMember.id).label("member_count"),
        )
        .outerjoin(TeamMember, TeamMember.team_id == Team.id)
        .group_by(Team.id)
        .order_by(Team.created_at.desc())
    )
    if hackathon_id is not None:
        query = query.filter(Team.hackathon_id == hackathon_id)
    query = apply_pagination(query, limit, offset)

    memberships = set()
    if current_user_id is not None:
        memberships = {
            row.team_id
            for row in db.query(TeamMember.team_id).filter(TeamMember.user_id == current_user_id).all()
        }

    return [
        {
            "id": row.id,
            "team_name": row.team_name,
            "hackathon_id": row.hackathon_id,
            "created_at": row.created_at,
            "created_by_user_id": row.created_by_user_id,
            "member_count": row.member_count,
            "is_member": row.id in memberships,
        }
        for row in query.all()
    ]


def join_team(db: Session, team_id: int, user_id: int) -> TeamMember:
    """Add a user to a hackathon team."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise not_found("Team not found")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise not_found("User not found")

    existing = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
        .first()
    )
    if existing:
        return existing

    membership = TeamMember(team_id=team_id, user_id=user_id)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def submit_project(db: Session, payload: ProjectCreate, current_user_id: int, is_admin: bool) -> Project:
    """Submit a project for a hackathon team."""
    team = db.query(Team).filter(Team.id == payload.team_id).first()
    if not team:
        raise not_found("Team not found")
    if not is_admin:
        membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == payload.team_id, TeamMember.user_id == current_user_id)
            .first()
        )
        if not membership:
            raise forbidden("You must join a team before submitting a project")

    project = Project(
        team_id=payload.team_id,
        title=payload.title,
        description=payload.description,
        created_by_user_id=current_user_id,
        impact_score=None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    members = db.query(TeamMember).filter(TeamMember.team_id == payload.team_id).all()
    for member in members:
        award_innovation_badge(db, member.user_id)
    create_energy_drop(db, current_user_id, 90, "hackathon-project", project.id)

    return project


def list_projects(db: Session, limit: int | None, offset: int | None) -> list[Project]:
    """List submitted projects."""
    query = db.query(Project).order_by(Project.submission_date.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()
