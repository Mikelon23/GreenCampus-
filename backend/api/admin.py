from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from backend.api.deps import require_admin
from backend.config.database import get_db
from backend.models import (
    Badge,
    CampusGoal,
    CampusZone,
    CarbonFootprint,
    EcoAction,
    Hackathon,
    Project,
    SensorData,
    Team,
    TreesPlanted,
    User,
)
from backend.utils.errors import bad_request, not_found
from backend.utils.security import hash_password

router = APIRouter(prefix="/api/admin", tags=["admin"])


RESOURCE_CONFIG: dict[str, dict] = {
    "users": {"model": User, "fields": {"name", "email", "role", "password"}},
    "zones": {"model": CampusZone, "fields": {"name", "description", "location_coordinates"}},
    "sensors": {
        "model": SensorData,
        "fields": {"zone_id", "temperature", "humidity", "co2_level", "energy_usage", "timestamp"},
        "datetime_fields": {"timestamp"},
    },
    "carbon-records": {
        "model": CarbonFootprint,
        "fields": {"user_id", "activity_type", "carbon_emission_estimate", "recorded_at"},
        "datetime_fields": {"recorded_at"},
    },
    "eco-actions": {
        "model": EcoAction,
        "fields": {"user_id", "action_type", "points_awarded", "timestamp"},
        "datetime_fields": {"timestamp"},
    },
    "badges": {"model": Badge, "fields": {"badge_name", "description", "points_required"}},
    "hackathons": {
        "model": Hackathon,
        "fields": {"title", "description", "start_date", "end_date", "status"},
        "date_fields": {"start_date", "end_date"},
    },
    "teams": {
        "model": Team,
        "fields": {"team_name", "hackathon_id", "created_by_user_id", "created_at"},
        "datetime_fields": {"created_at"},
    },
    "projects": {
        "model": Project,
        "fields": {
            "team_id",
            "title",
            "description",
            "created_by_user_id",
            "submission_date",
            "impact_score",
            "file_url",
        },
        "datetime_fields": {"submission_date"},
    },
    "trees": {
        "model": TreesPlanted,
        "fields": {"user_id", "zone_id", "tree_species", "planting_date"},
        "datetime_fields": {"planting_date"},
    },
    "campus-goals": {
        "model": CampusGoal,
        "fields": {"title", "description", "target_energy", "current_energy", "reward_points", "start_date", "end_date", "status"},
        "date_fields": {"start_date", "end_date"},
    },
}


def _serialize(instance) -> dict:
    return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}


def _get_resource(resource: str) -> dict:
    config = RESOURCE_CONFIG.get(resource)
    if not config:
        raise not_found("Admin resource not found")
    return config


def _coerce_value(field: str, value, config: dict):
    if value is None:
        return None
    if field in config.get("date_fields", set()) and isinstance(value, str):
        return date.fromisoformat(value)
    if field in config.get("datetime_fields", set()) and isinstance(value, str):
        return datetime.fromisoformat(value)
    return value


def _apply_payload(instance, payload: dict, config: dict) -> None:
    for field in config["fields"]:
        if field not in payload:
            continue
        value = _coerce_value(field, payload[field], config)
        if field == "password":
            setattr(instance, "password_hash", hash_password(value))
        else:
            setattr(instance, field, value)


@router.get("/{resource}")
def list_resource(
    resource: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> list[dict]:
    """Return all rows for the selected admin resource."""
    config = _get_resource(resource)
    model = config["model"]
    rows = db.query(model).order_by(model.id.desc()).all()
    return [_serialize(row) for row in rows]


@router.post("/{resource}", status_code=201)
def create_resource(
    resource: str,
    payload: dict,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict:
    """Create a row in the selected admin resource."""
    config = _get_resource(resource)
    model = config["model"]
    instance = model()
    _apply_payload(instance, payload, config)
    if resource == "users" and "password" not in payload:
        raise bad_request("Users require a password")
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return _serialize(instance)


@router.put("/{resource}/{item_id}")
def update_resource(
    resource: str,
    item_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> dict:
    """Update a row in the selected admin resource."""
    config = _get_resource(resource)
    model = config["model"]
    instance = db.query(model).filter(model.id == item_id).first()
    if not instance:
        raise not_found("Record not found")
    _apply_payload(instance, payload, config)
    db.commit()
    db.refresh(instance)
    return _serialize(instance)


@router.delete("/{resource}/{item_id}", status_code=200)
def delete_resource(
    resource: str,
    item_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> None:
    """Delete a row in the selected admin resource."""
    config = _get_resource(resource)
    model = config["model"]
    instance = db.query(model).filter(model.id == item_id).first()
    if not instance:
        raise not_found("Record not found")
    db.delete(instance)
    db.commit()
