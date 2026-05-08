from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.config.settings import settings
from backend.schemas.sensor import SensorDataCreate, SensorDataResponse
from backend.services.sensors import create_sensor_data
from backend.utils.errors import unauthorized

router = APIRouter(prefix="/api/iot", tags=["iot"])


def verify_iot_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    """Allow hardware ingestion only when the static IoT API key matches."""
    if not x_api_key or x_api_key != settings.iot_api_key:
        raise unauthorized("Invalid IoT API key")


@router.post(
    "/sensors",
    response_model=SensorDataResponse,
    status_code=201,
    dependencies=[Depends(verify_iot_api_key)],
)
def create_iot_sensor(payload: SensorDataCreate, db: Session = Depends(get_db)) -> SensorDataResponse:
    """Register sensor data sent directly from ESP32 devices."""
    return create_sensor_data(db, payload)
