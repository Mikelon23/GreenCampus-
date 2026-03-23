from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from backend.api.deps import get_current_user
from backend.config.database import get_db
from backend.models import Project, TeamMember, User
from backend.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from backend.services.hackathons import list_projects, submit_project
from backend.utils.editing import ensure_editable
from backend.utils.errors import forbidden
from backend.utils.errors import not_found

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectResponse:
    """Submit a project to a hackathon."""
    return submit_project(db, payload, current_user.id, current_user.role.lower() == "admin")


@router.get("", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[ProjectResponse]:
    """Return submitted projects."""
    return list_projects(db, limit, offset)


@router.post("/{project_id}/upload", response_model=ProjectResponse)
def upload_project_file(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectResponse:
    """Upload a file for a specific project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if current_user.role.lower() != "admin":
        membership = (
            db.query(TeamMember)
            .filter(TeamMember.team_id == project.team_id, TeamMember.user_id == current_user.id)
            .first()
        )
        if not membership:
            raise forbidden("You do not have access to this project")

    # Generate a unique filename to prevent collisions
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = f"backend/uploads/{unique_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    project.file_url = f"/uploads/{unique_filename}"
    db.commit()
    db.refresh(project)
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectResponse:
    """Allow project creators to edit their submission for 30 minutes."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise not_found("Project not found")
    if current_user.role.lower() != "admin" and project.created_by_user_id != current_user.id:
        raise forbidden("You do not have access to this project")
    ensure_editable(project.submission_date, current_user.role.lower() == "admin")
    project.team_id = payload.team_id
    project.title = payload.title
    project.description = payload.description
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=200)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Allow project creators to delete their submission for 30 minutes."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise not_found("Project not found")
    if current_user.role.lower() != "admin" and project.created_by_user_id != current_user.id:
        raise forbidden("You do not have access to this project")
    ensure_editable(project.submission_date, current_user.role.lower() == "admin")
    db.delete(project)
    db.commit()
