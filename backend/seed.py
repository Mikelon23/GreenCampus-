"""Seed script for GreenCampus+ development environment.

Usage (from repo root):
    python -m backend.seed

Creates:
- 4 campus zones
- 5 sustainability badges
- 1 demo admin user  (admin@campus.edu / admin1234)
- 1 demo hackathon
- 1 active campus goal
- 12 sensor readings  (3 per zone, spread over 3 days)
- 4 sustainability scores (one per zone)
"""

from __future__ import annotations

import sys
import os
from datetime import datetime, timedelta

# Load settings so the DB URL is available
from backend.config.database import Base, SessionLocal, engine  # noqa: F401 – creates engine
from backend.config.settings import settings  # noqa: F401
from backend.models import (
    Badge,
    CampusGoal,
    CampusZone,
    Hackathon,
    SensorData,
    SustainabilityScore,
    User,
)
from backend.utils.security import hash_password


# ---------------------------------------------------------------------------
# Seed data definitions
# ---------------------------------------------------------------------------

ZONES = [
    {"name": "Library", "description": "Main university library", "location_coordinates": "4.6387,-74.0828"},
    {"name": "Engineering Building", "description": "Faculty of Engineering & Sciences", "location_coordinates": "4.6392,-74.0831"},
    {"name": "Cafeteria", "description": "Central dining hall", "location_coordinates": "4.6380,-74.0820"},
    {"name": "Green Area", "description": "Campus eco-park and gardens", "location_coordinates": "4.6375,-74.0815"},
]

BADGES = [
    {"badge_name": "Eco Explorer", "description": "Completed your first sustainability action.", "points_required": 10},
    {"badge_name": "Green Guardian", "description": "Accumulated 100 green points.", "points_required": 100},
    {"badge_name": "Carbon Cutter", "description": "Reduced carbon footprint 5 times.", "points_required": 250},
    {"badge_name": "Tree Planter", "description": "Planted at least one tree on campus.", "points_required": 50},
    {"badge_name": "Campus Champion", "description": "Reached the top of the leaderboard.", "points_required": 500},
]

ADMIN_USER = {
    "name": "Admin GreenCampus",
    "email": "admin@campus.edu",
    "role": "admin",
    "password": "admin1234",
}

# Minimal demo content for the hackathon flow and Eco Forest view.
DEMO_HACKATHON = {
    "title": "GreenHack Sprint",
    "description": "A short sustainability hackathon for testing teams and project submissions.",
}

DEMO_CAMPUS_GOAL = {
    "title": "Collect 500 Energy This Week",
    "description": "Collect energy drops across the campus to unlock a points bonus for everyone.",
    "target_energy": 500,
    "reward_points": 150,
}

# Sensor readings: (hours_ago, temp, humidity, co2, energy)
SENSOR_READINGS: list[tuple] = [
    (1,  22.3, 51.2, 398.0, 118.5),
    (2,  21.8, 52.0, 402.5, 122.0),
    (3,  23.1, 49.8, 395.0, 115.0),
    (25, 20.5, 54.3, 410.0, 130.0),
    (26, 21.0, 53.5, 408.0, 128.0),
    (27, 22.8, 50.1, 403.0, 120.0),
    (49, 19.8, 56.0, 415.0, 135.0),
    (50, 20.2, 55.2, 412.0, 133.0),
    (51, 21.5, 53.0, 405.0, 125.0),
    (73, 23.5, 48.5, 392.0, 112.0),
    (74, 22.0, 50.8, 396.0, 116.0),
    (75, 21.2, 52.5, 400.0, 119.0),
]

# Sustainability scores: (score, energy_index, carbon_index)
ZONE_SCORES = [
    (78.5, 82.0, 75.0),
    (65.2, 70.0, 62.0),
    (71.8, 68.0, 74.0),
    (88.3, 90.0, 86.5),
]


# ---------------------------------------------------------------------------
# Main seed function
# ---------------------------------------------------------------------------

def seed() -> None:
    """Insert seed data into the database."""
    db = SessionLocal()
    try:
        # Allow docker-compose / scripts to override demo credentials without hardcoding secrets.
        admin_email = os.getenv("ADMIN_EMAIL", ADMIN_USER["email"])
        admin_password = os.getenv("ADMIN_PASSWORD", ADMIN_USER["password"])

        # ---- Zones -------------------------------------------------------
        zones: list[CampusZone] = []
        for z in ZONES:
            existing = db.query(CampusZone).filter(CampusZone.name == z["name"]).first()
            if existing:
                zones.append(existing)
                print(f"  zone already exists: {z['name']}")
            else:
                zone = CampusZone(**z)
                db.add(zone)
                db.flush()
                zones.append(zone)
                print(f"  created zone: {z['name']}")
        db.commit()

        # ---- Badges ------------------------------------------------------
        for b in BADGES:
            existing = db.query(Badge).filter(Badge.badge_name == b["badge_name"]).first()
            if not existing:
                db.add(Badge(**b))
                print(f"  created badge: {b['badge_name']}")
            else:
                print(f"  badge already exists: {b['badge_name']}")
        db.commit()

        # ---- Admin user --------------------------------------------------
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            admin = User(
                name=ADMIN_USER["name"],
                email=admin_email,
                role=ADMIN_USER["role"],
                password_hash=hash_password(admin_password),
            )
            db.add(admin)
            db.commit()
            print(f"  created admin user: {admin_email}")
        else:
            print(f"  admin user already exists: {admin_email}")

        # ---- Demo hackathon ---------------------------------------------
        existing_hackathon = db.query(Hackathon).filter(Hackathon.title == DEMO_HACKATHON["title"]).first()
        if not existing_hackathon:
            today = datetime.utcnow().date()
            hackathon = Hackathon(
                title=DEMO_HACKATHON["title"],
                description=DEMO_HACKATHON["description"],
                start_date=today,
                end_date=today + timedelta(days=7),
                status="active",
            )
            db.add(hackathon)
            db.commit()
            print(f"  created hackathon: {hackathon.title}")
        else:
            print(f"  hackathon already exists: {existing_hackathon.title}")

        # ---- Campus goals ------------------------------------------------
        existing_goal = db.query(CampusGoal).filter(CampusGoal.title == DEMO_CAMPUS_GOAL["title"]).first()
        if not existing_goal:
            today = datetime.utcnow().date()
            goal = CampusGoal(
                title=DEMO_CAMPUS_GOAL["title"],
                description=DEMO_CAMPUS_GOAL["description"],
                target_energy=DEMO_CAMPUS_GOAL["target_energy"],
                current_energy=0,
                reward_points=DEMO_CAMPUS_GOAL["reward_points"],
                start_date=today,
                end_date=today + timedelta(days=7),
                status="active",
            )
            db.add(goal)
            db.commit()
            print(f"  created campus goal: {goal.title}")
        else:
            print(f"  campus goal already exists: {existing_goal.title}")

        # ---- Sensor readings ----------------------------------------------
        now = datetime.utcnow()
        existing_readings = db.query(SensorData.id).first()
        if not existing_readings:
            readings_added = 0
            for i, zone in enumerate(zones):
                for hrs, temp, hum, co2, energy in SENSOR_READINGS[i * 3 : i * 3 + 3]:
                    ts = now - timedelta(hours=hrs)
                    record = SensorData(
                        zone_id=zone.id,
                        temperature=temp,
                        humidity=hum,
                        co2_level=co2,
                        energy_usage=energy,
                        timestamp=ts,
                    )
                    db.add(record)
                    readings_added += 1
            db.commit()
            print(f"  created {readings_added} sensor readings")
        else:
            print("  sensor readings already exist; skipping")

        # ---- Sustainability scores ----------------------------------------
        existing_scores = db.query(SustainabilityScore.id).first()
        if not existing_scores:
            scores_added = 0
            for zone, (score, energy_idx, carbon_idx) in zip(zones, ZONE_SCORES):
                s = SustainabilityScore(
                    zone_id=zone.id,
                    sustainability_score=score,
                    energy_efficiency_index=energy_idx,
                    carbon_index=carbon_idx,
                    calculated_at=now,
                )
                db.add(s)
                scores_added += 1
            db.commit()
            print(f"  created {scores_added} sustainability scores")
        else:
            print("  sustainability scores already exist; skipping")

        print("\n[OK] Seed completed successfully!")
        print(f"Admin login: {admin_email} / {admin_password}")

    except Exception as exc:
        db.rollback()
        print(f"\n[ERROR] Seed failed: {exc}", file=sys.stderr)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("[seed] Seeding database...")
    seed()
