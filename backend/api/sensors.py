from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.api.deps import get_current_user
from backend.config.database import get_db
from backend.schemas.sensor import SensorDataCreate, SensorDataResponse
from backend.services.sensors import create_sensor_data, list_sensor_data

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


@router.get("", response_model=list[SensorDataResponse])
def get_sensors(
    db: Session = Depends(get_db),
    zone_id: int | None = Query(default=None),
    start_date: datetime | None = Query(default=None),
    end_date: datetime | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=500),
    offset: int | None = Query(default=None, ge=0),
) -> list[SensorDataResponse]:
    """Return sensor data with optional filters."""
    return list_sensor_data(db, zone_id, start_date, end_date, limit, offset)


@router.post("", response_model=SensorDataResponse, status_code=201, dependencies=[Depends(get_current_user)])
def create_sensor(payload: SensorDataCreate, db: Session = Depends(get_db)) -> SensorDataResponse:
    """Register new sensor data."""
    return create_sensor_data(db, payload)
