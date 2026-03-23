from datetime import datetime, timedelta
from statistics import median

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models import SensorData, SustainabilityScore


def _percentile_score(values: list[float], value: float, lower_is_better: bool = True) -> float:
    """Compute a percentile-based score from 0.0 to 1.0."""
    if len(values) <= 1:
        return 1.0
    sorted_values = sorted(values)
    indices = [idx for idx, item in enumerate(sorted_values) if item == value]
    rank = sum(indices) / len(indices)
    percentile = rank / (len(values) - 1)
    return 1 - percentile if lower_is_better else percentile


def _score_from_deviation(values: list[float], value: float) -> float:
    """Score a value based on deviation from the median (lower deviation is better)."""
    if len(values) <= 1:
        return 1.0
    med = median(values)
    deviations = [abs(item - med) for item in values]
    value_deviation = abs(value - med)
    return _percentile_score(deviations, value_deviation, lower_is_better=True)


def calculate_daily_scores(db: Session) -> list[SustainabilityScore]:
    """Calculate and persist sustainability scores for the last 24 hours."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)

    averages = (
        db.query(
            SensorData.zone_id.label("zone_id"),
            func.avg(SensorData.temperature).label("temperature"),
            func.avg(SensorData.humidity).label("humidity"),
            func.avg(SensorData.co2_level).label("co2_level"),
            func.avg(SensorData.energy_usage).label("energy_usage"),
        )
        .filter(SensorData.timestamp >= start_time)
        .group_by(SensorData.zone_id)
        .all()
    )

    if not averages:
        return []

    temperatures = [row.temperature for row in averages]
    humidities = [row.humidity for row in averages]
    co2_levels = [row.co2_level for row in averages]
    energy_values = [row.energy_usage for row in averages]

    results: list[SustainabilityScore] = []
    for row in averages:
        temp_score = _score_from_deviation(temperatures, row.temperature)
        humidity_score = _score_from_deviation(humidities, row.humidity)
        co2_score = _percentile_score(co2_levels, row.co2_level, lower_is_better=True)
        energy_score = _percentile_score(energy_values, row.energy_usage, lower_is_better=True)

        sustainability_score = (temp_score + humidity_score + co2_score + energy_score) / 4
        energy_efficiency_index = energy_score * 100
        carbon_index = co2_score * 100

        existing = (
            db.query(SustainabilityScore)
            .filter(SustainabilityScore.zone_id == row.zone_id)
            .order_by(SustainabilityScore.calculated_at.desc())
            .first()
        )
        if existing and existing.calculated_at.date() == end_time.date():
            existing.sustainability_score = sustainability_score * 100
            existing.energy_efficiency_index = energy_efficiency_index
            existing.carbon_index = carbon_index
            existing.calculated_at = end_time
            score = existing
        else:
            score = SustainabilityScore(
                zone_id=row.zone_id,
                sustainability_score=sustainability_score * 100,
                energy_efficiency_index=energy_efficiency_index,
                carbon_index=carbon_index,
                calculated_at=end_time,
            )
            db.add(score)
        results.append(score)

    db.commit()
    for score in results:
        db.refresh(score)
    return results
