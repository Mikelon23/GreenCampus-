from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.config.database import Base, get_db
from backend.config.settings import settings
from backend.main import app
from backend.models import CampusZone, SensorData


def test_iot_sensor_ingestion_requires_api_key(monkeypatch):
    """Accept ESP32 sensor posts only when X-API-Key matches the IoT secret."""
    monkeypatch.setattr(settings, "iot_api_key", "test-iot-key")

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(engine)

    db = SessionLocal()
    db.add(CampusZone(id=1, name="Demo Stand", description="TELECOM 2026", location_coordinates="0,0"))
    db.commit()
    db.close()

    def override_get_db():
        session = SessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    payload = {
        "zone_id": 1,
        "temperature": 24.0,
        "humidity": 50.0,
        "co2_level": 620.0,
        "energy_usage": 130.0,
    }

    try:
        assert client.post("/api/iot/sensors", json=payload).status_code == 401
        assert client.post("/api/iot/sensors", json=payload, headers={"X-API-Key": "wrong"}).status_code == 401

        response = client.post("/api/iot/sensors", json=payload, headers={"X-API-Key": "test-iot-key"})

        assert response.status_code == 201
        body = response.json()
        assert body["zone_id"] == 1
        assert body["co2_level"] == 620.0

        db = SessionLocal()
        try:
            records = db.query(SensorData).all()
            assert len(records) == 1
            assert records[0].zone_id == 1
        finally:
            db.close()
    finally:
        app.dependency_overrides.clear()
