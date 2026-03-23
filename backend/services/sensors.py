from datetime import datetime

from sqlalchemy.orm import Session

from backend.models import CampusZone, SensorData
from backend.schemas.sensor import SensorDataCreate
from backend.utils.errors import not_found
from backend.utils.pagination import apply_pagination


def create_sensor_data(db: Session, payload: SensorDataCreate) -> SensorData:
    """Create and persist a sensor data record."""
    zone = db.query(CampusZone).filter(CampusZone.id == payload.zone_id).first()
    if not zone:
        raise not_found("Campus zone not found")

    record = SensorData(
        zone_id=payload.zone_id,
        temperature=payload.temperature,
        humidity=payload.humidity,
        co2_level=payload.co2_level,
        energy_usage=payload.energy_usage,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_sensor_data(
    db: Session,
    zone_id: int | None,
    start_date: datetime | None,
    end_date: datetime | None,
    limit: int | None,
    offset: int | None,
) -> list[SensorData]:
    """Return sensor data filtered by zone and date range."""
    query = db.query(SensorData)
    if zone_id is not None:
        query = query.filter(SensorData.zone_id == zone_id)
    if start_date is not None:
        query = query.filter(SensorData.timestamp >= start_date)
    if end_date is not None:
        query = query.filter(SensorData.timestamp <= end_date)
    query = query.order_by(SensorData.timestamp.desc())
    query = apply_pagination(query, limit, offset)
    return query.all()
