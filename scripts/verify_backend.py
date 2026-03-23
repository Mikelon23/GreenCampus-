from __future__ import annotations

"""
Lightweight verification script for the GreenCampus+ backend.

Runs a basic end-to-end flow via FastAPI TestClient:
- auth (admin + student)
- hackathons/teams/projects
- carbon + eco-actions with 30-minute edit window enforcement
- Eco Forest (EcoVerse) overview + energy interactions
- admin CRUD access control

Usage (from repo root):
  backend/.venv/Scripts/python.exe scripts/verify_backend.py
"""

from datetime import datetime, timedelta, timezone
import json
import random
import string
import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.config.database import SessionLocal
from backend.main import app
from backend.models import CarbonFootprint, EcoAction, Project, Team


def _rand_suffix(length: int = 6) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def _post_json(client: TestClient, url: str, payload: dict, headers: dict | None = None):
    return client.post(url, json=payload, headers=headers or {})


def _put_json(client: TestClient, url: str, payload: dict, headers: dict | None = None):
    return client.put(url, json=payload, headers=headers or {})


def main() -> int:
    client = TestClient(app)

    # Basic health check.
    r = client.get("/health")
    assert r.status_code == 200, r.text

    # Admin login (seeded by backend.seed).
    admin_login = _post_json(
        client,
        "/api/auth/login",
        {"email": "admin@campus.edu", "password": "admin1234"},
    )
    assert admin_login.status_code == 200, admin_login.text
    admin_token = admin_login.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Register two students for social interactions.
    suffix = _rand_suffix()
    student_a_email = f"student_a_{suffix}@campus.edu"
    student_b_email = f"student_b_{suffix}@campus.edu"

    reg_a = _post_json(
        client,
        "/api/auth/register",
        {"name": "Student A", "email": student_a_email, "role": "student", "password": "student1234"},
    )
    assert reg_a.status_code in (200, 201), reg_a.text
    a = reg_a.json()
    a_headers = {"Authorization": f"Bearer {a['access_token']}"}
    a_user_id = a["user"]["id"]
    assert a_user_id is not None

    reg_b = _post_json(
        client,
        "/api/auth/register",
        {"name": "Student B", "email": student_b_email, "role": "student", "password": "student1234"},
    )
    assert reg_b.status_code in (200, 201), reg_b.text
    b = reg_b.json()
    b_headers = {"Authorization": f"Bearer {b['access_token']}"}
    b_user_id = b["user"]["id"]
    assert b_user_id is not None

    # Hackathon exists (seed creates one).
    hackathons = client.get("/api/hackathons")
    assert hackathons.status_code == 200, hackathons.text
    hackathon_id = hackathons.json()[0]["id"]

    # Create team (student A).
    team_resp = _post_json(
        client,
        "/api/teams",
        {"team_name": f"EcoTeam-{suffix}", "hackathon_id": hackathon_id},
        headers=a_headers,
    )
    assert team_resp.status_code == 201, team_resp.text
    team = team_resp.json()
    assert team["created_by_user_id"] == a_user_id
    team_id = team["id"]

    # Submit project (student A). Response must include created_by_user_id.
    project_resp = _post_json(
        client,
        "/api/projects",
        {"team_id": team_id, "title": "Solar Swap", "description": "Replace lights with solar powered system."},
        headers=a_headers,
    )
    assert project_resp.status_code == 201, project_resp.text
    project = project_resp.json()
    assert project["created_by_user_id"] == a_user_id

    # Allowed edit inside the window.
    project_update = _put_json(
        client,
        f"/api/projects/{project['id']}",
        {"team_id": team_id, "title": "Solar Swap v2", "description": "Updated description."},
        headers=a_headers,
    )
    assert project_update.status_code == 200, project_update.text

    # Create eco-action (student A) and edit inside the window.
    action_resp = _post_json(
        client,
        "/api/actions",
        {"user_id": a_user_id, "action_type": "recycling paper"},
        headers=a_headers,
    )
    assert action_resp.status_code == 201, action_resp.text
    action = action_resp.json()
    assert "id" in action
    action_update = _put_json(
        client,
        f"/api/actions/{action['id']}",
        {"user_id": a_user_id, "action_type": "waste sorting", "points_awarded": action["points_awarded"]},
        headers=a_headers,
    )
    assert action_update.status_code == 200, action_update.text

    # Create carbon record (student A) and edit inside the window.
    carbon_resp = _post_json(
        client,
        "/api/carbon",
        {"user_id": a_user_id, "activity_type": "Bus commute", "carbon_emission_estimate": 1.15},
        headers=a_headers,
    )
    assert carbon_resp.status_code == 201, carbon_resp.text
    carbon = carbon_resp.json()
    assert "id" in carbon
    carbon_update = _put_json(
        client,
        f"/api/carbon/{carbon['id']}",
        {"user_id": a_user_id, "activity_type": "Bus commute", "carbon_emission_estimate": 1.1},
        headers=a_headers,
    )
    assert carbon_update.status_code == 200, carbon_update.text

    # Enforce 30-minute edit window by pushing timestamps back in the DB.
    db = SessionLocal()
    try:
        too_old = datetime.now(timezone.utc) - timedelta(minutes=31)

        db_action = db.query(EcoAction).filter(EcoAction.id == action["id"]).first()
        assert db_action is not None
        db_action.timestamp = too_old

        db_carbon = db.query(CarbonFootprint).filter(CarbonFootprint.id == carbon["id"]).first()
        assert db_carbon is not None
        db_carbon.recorded_at = too_old

        db_project = db.query(Project).filter(Project.id == project["id"]).first()
        assert db_project is not None
        db_project.submission_date = too_old

        db_team = db.query(Team).filter(Team.id == team_id).first()
        assert db_team is not None
        db_team.created_at = too_old

        db.commit()
    finally:
        db.close()

    # Now edits should be forbidden for non-admin.
    late_action_edit = _put_json(
        client,
        f"/api/actions/{action['id']}",
        {"user_id": a_user_id, "action_type": "composting food waste", "points_awarded": action["points_awarded"]},
        headers=a_headers,
    )
    assert late_action_edit.status_code == 403, late_action_edit.text

    late_carbon_edit = _put_json(
        client,
        f"/api/carbon/{carbon['id']}",
        {"user_id": a_user_id, "activity_type": "Car commute", "carbon_emission_estimate": 4.25},
        headers=a_headers,
    )
    assert late_carbon_edit.status_code == 403, late_carbon_edit.text

    late_project_edit = _put_json(
        client,
        f"/api/projects/{project['id']}",
        {"team_id": team_id, "title": "Solar Swap v3", "description": "Too late edit."},
        headers=a_headers,
    )
    assert late_project_edit.status_code == 403, late_project_edit.text

    late_team_edit = _put_json(
        client,
        f"/api/teams/{team_id}",
        {"team_name": "Too late rename", "hackathon_id": hackathon_id},
        headers=a_headers,
    )
    assert late_team_edit.status_code == 403, late_team_edit.text

    # Admin override should work even after the window.
    admin_team_edit = _put_json(
        client,
        f"/api/teams/{team_id}",
        {"team_name": f"AdminEdit-{suffix}", "hackathon_id": hackathon_id},
        headers=admin_headers,
    )
    assert admin_team_edit.status_code == 200, admin_team_edit.text

    # Eco Forest overview should show campus goals and energy mechanics.
    overview_a = client.get(f"/api/ecoverse/overview/{a_user_id}", headers=a_headers)
    assert overview_a.status_code == 200, overview_a.text
    overview_data = overview_a.json()
    assert "tree" in overview_data
    assert "campus_goals" in overview_data
    assert len(overview_data["campus_goals"]) >= 1

    # Generate energy for student B and validate social energy interaction from A.
    action_b = _post_json(
        client,
        "/api/actions",
        {"user_id": b_user_id, "action_type": "reusing water bottle"},
        headers=b_headers,
    )
    assert action_b.status_code == 201, action_b.text

    overview_a2 = client.get(f"/api/ecoverse/overview/{a_user_id}", headers=a_headers)
    assert overview_a2.status_code == 200, overview_a2.text
    social_energy = overview_a2.json().get("social_energy") or []
    if social_energy:
        energy_id = social_energy[0]["id"]
        helped = client.post(f"/api/ecoverse/energy/{energy_id}/help", headers=a_headers)
        assert helped.status_code == 200, helped.text
        rescued = client.post(f"/api/ecoverse/energy/{energy_id}/rescue", headers=a_headers)
        # Rescue may be blocked depending on energy state; accept 200 or 400/403 as valid behavior.
        assert rescued.status_code in (200, 400, 403), rescued.text

    # Admin CRUD must be admin-only.
    admin_list_ok = client.get("/api/admin/users", headers=admin_headers)
    assert admin_list_ok.status_code == 200, admin_list_ok.text
    admin_list_denied = client.get("/api/admin/users", headers=a_headers)
    assert admin_list_denied.status_code == 403, admin_list_denied.text

    print(
        json.dumps(
            {
                "ok": True,
                "student_a_email": student_a_email,
                "student_b_email": student_b_email,
                "team_id": team_id,
                "project_id": project["id"],
                "action_id": action["id"],
                "carbon_id": carbon["id"],
                "campus_goals": len(overview_data["campus_goals"]),
                "social_energy_seen": len(social_energy),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
