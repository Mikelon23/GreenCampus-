from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import get_current_user
from backend.config.database import get_db
from backend.models import TreesPlanted, User
from backend.schemas.tree import TreePlantingCreate, TreePlantingResponse, TreePlantingUpdate
from backend.services.trees import create_tree_record, list_trees
from backend.utils.editing import ensure_editable
from backend.utils.errors import not_found

router = APIRouter(prefix="/api/trees", tags=["trees"])


@router.post("", response_model=TreePlantingResponse, status_code=201)
def create_tree(
    payload: TreePlantingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TreePlantingResponse:
    """Register a tree planting activity."""
    if current_user.role.lower() != "admin" and current_user.id != payload.user_id:
        from backend.utils.errors import forbidden

        raise forbidden("You do not have access to this resource")
    return create_tree_record(db, payload)


@router.get("", response_model=list[TreePlantingResponse])
def get_trees(
    db: Session = Depends(get_db),
    limit: int | None = Query(default=None, ge=1, le=200),
    offset: int | None = Query(default=None, ge=0),
) -> list[TreePlantingResponse]:
    """Return tree planting records."""
    return list_trees(db, limit, offset)


@router.put("/{tree_id}", response_model=TreePlantingResponse)
def update_tree(
    tree_id: int,
    payload: TreePlantingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TreePlantingResponse:
    """Update a tree record within the edit window."""
    record = db.query(TreesPlanted).filter(TreesPlanted.id == tree_id).first()
    if not record:
        raise not_found("Tree record not found")
    if current_user.role.lower() != "admin" and current_user.id != record.user_id:
        from backend.utils.errors import forbidden

        raise forbidden("You do not have access to this resource")
    ensure_editable(record.planting_date, current_user.role.lower() == "admin")
    record.zone_id = payload.zone_id
    record.tree_species = payload.tree_species
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{tree_id}", status_code=200)
def delete_tree(
    tree_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a tree record within the edit window."""
    record = db.query(TreesPlanted).filter(TreesPlanted.id == tree_id).first()
    if not record:
        raise not_found("Tree record not found")
    if current_user.role.lower() != "admin" and current_user.id != record.user_id:
        from backend.utils.errors import forbidden

        raise forbidden("You do not have access to this resource")
    ensure_editable(record.planting_date, current_user.role.lower() == "admin")
    db.delete(record)
    db.commit()
