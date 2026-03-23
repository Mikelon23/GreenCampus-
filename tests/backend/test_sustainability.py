from datetime import datetime, timedelta

from backend.models import CampusZone, SensorData
from backend.services.sustainability import calculate_daily_scores


def test_calculate_daily_scores(db_session):
    """Ensure sustainability scores are produced for zones."""
    zone_a = CampusZone(name="Zone A", description="Test", location_coordinates="0,0")
    zone_b = CampusZone(name="Zone B", description="Test", location_coordinates="1,1")
    db_session.add_all([zone_a, zone_b])
    db_session.commit()

    now = datetime.utcnow()
    db_session.add_all(
        [
            SensorData(
                zone_id=zone_a.id,
                temperature=22.0,
                humidity=50.0,
                co2_level=400.0,
                energy_usage=120.0,
                timestamp=now - timedelta(hours=1),
            ),
            SensorData(
                zone_id=zone_b.id,
                temperature=25.0,
                humidity=55.0,
                co2_level=420.0,
                energy_usage=150.0,
                timestamp=now - timedelta(hours=2),
            ),
        ]
    )
    db_session.commit()

    scores = calculate_daily_scores(db_session)
    assert len(scores) == 2
