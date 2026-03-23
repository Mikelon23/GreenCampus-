from sqlalchemy.orm import Session

from backend.models import CampusZone, TreesPlanted, User
from backend.schemas.tree import TreePlantingCreate
from backend.utils.errors import not_found
from backend.utils.pagination import apply_pagination


def create_tree_record(db: Session, payload: TreePlantingCreate) -> TreesPlanted:
    """Create a tree planting record."""
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise not_found("User not found")
    zone = db.query(CampusZone).filter(CampusZone.id == payload.zone_id).first()
    if not zone:
        raise not_found("Campus zone not found")

    record = TreesPlanted(
        user_id=payload.user_id,
        zone_id=payload.zone_id,
        tree_species=payload.tree_species,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_trees(db: Session, limit: int | None, offset: int | None) -> list[TreesPlanted]:
    """List tree planting records."""
    query = db.query(TreesPlanted).order_by(TreesPlanted.planting_date.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()
