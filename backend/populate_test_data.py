"""Populate test data - simple version without SQLAlchemy lazy-load issues."""
import sys
from datetime import datetime, timedelta, timezone

from backend.config.database import SessionLocal
from backend.models import (
    Badge, CampusZone, CarbonFootprint, EcoAction, GreenPoints,
    Hackathon, Project, SustainabilityScore, Team, TeamMember,
    TreesPlanted, User, UserBadge,
)
from backend.utils.security import hash_password

now = datetime.now(timezone.utc).replace(tzinfo=None)


def populate():
    db = SessionLocal()
    try:
        # ── Users ──────────────────────────────────────────────────────────
        users_raw = [
            ("Admin GreenCampus", "admin@campus.edu",   "admin",      "admin1234"),
            ("Carlos Estudiante", "carlos@campus.edu",  "student",    "student1234"),
            ("Ana Verde",         "ana@campus.edu",      "student",    "student1234"),
            ("Dr. Ramirez",       "ramirez@campus.edu", "researcher", "research1234"),
        ]
        users = {}
        for name, email, role, pwd in users_raw:
            u = db.query(User).filter(User.email == email).first()
            if not u:
                u = User(name=name, email=email, role=role, password_hash=hash_password(pwd))
                db.add(u)
                db.flush()
                print(f"  created user: {email}")
            else:
                print(f"  exists  user: {email}")
            users[email] = u
        db.commit()
        for u in users.values():
            db.refresh(u)

        # ── Eco-Actions + Green Points ──────────────────────────────────────
        actions_spec = {
            "carlos@campus.edu": [
                ("walking to campus",         50, 5),
                ("recycling paper",           30, 3),
                ("using public transport",    40, 2),
                ("participating in cleanup",  80, 1),
                ("reusing water bottle",      20, 7),
                ("planting a tree",          100, 1),
            ],
            "ana@campus.edu": [
                ("cycling to campus",         60, 4),
                ("reducing energy at home",   45, 6),
                ("composting food waste",     35, 2),
                ("participating in hackathon",120, 1),
                ("using reusable bags",       25, 3),
            ],
            "ramirez@campus.edu": [
                ("environmental research",   90, 3),
                ("sustainability workshop",  70, 2),
                ("carbon audit activity",    85, 1),
            ],
            "admin@campus.edu": [
                ("setting up green initiative", 200, 1),
                ("organizing campus cleanup",   150, 2),
            ],
        }
        print("\nEco-Actions & Green Points:")
        for email, specs in actions_spec.items():
            user = users[email]
            total_added = 0
            for action_type, points, count in specs:
                existing = db.query(EcoAction).filter(
                    EcoAction.user_id == user.id,
                    EcoAction.action_type == action_type,
                ).count()
                to_add = max(0, count - existing)
                for i in range(to_add):
                    db.add(EcoAction(
                        user_id=user.id,
                        action_type=action_type,
                        points_awarded=points,
                        timestamp=now - timedelta(days=i * 2 + 1),
                    ))
                    total_added += points
            db.flush()
            # Upsert green points
            gp = db.query(GreenPoints).filter(GreenPoints.user_id == user.id).first()
            if gp:
                gp.total_points += total_added
                gp.last_updated = now
            else:
                # Calculate total from all actions
                all_actions = db.query(EcoAction).filter(EcoAction.user_id == user.id).all()
                total_pts = sum(a.points_awarded for a in all_actions) + total_added
                db.add(GreenPoints(user_id=user.id, total_points=total_pts, last_updated=now))
            db.commit()
            gp = db.query(GreenPoints).filter(GreenPoints.user_id == user.id).first()
            print(f"  {email:35} -> {gp.total_points if gp else 0} pts")

        # ── Badge Awards ───────────────────────────────────────────────────
        print("\nBadge Awards:")
        badges = db.query(Badge).all()
        for email, user in users.items():
            gp = db.query(GreenPoints).filter(GreenPoints.user_id == user.id).first()
            if not gp:
                continue
            total = gp.total_points
            earned_ids = {ub.badge_id for ub in db.query(UserBadge).filter(UserBadge.user_id == user.id).all()}
            awarded = []
            for badge in badges:
                if badge.id not in earned_ids and total >= badge.points_required:
                    db.add(UserBadge(user_id=user.id, badge_id=badge.id, earned_at=now))
                    awarded.append(badge.badge_name)
            db.commit()
            print(f"  {email:35} -> {awarded or 'no new badges'}")

        # ── Carbon Footprint ───────────────────────────────────────────────
        print("\nCarbon Footprint:")
        carbon_spec = {
            "carlos@campus.edu": [
                ("transportation",   2.5, 10),
                ("energy_usage",     1.2,  5),
                ("transportation",   0.8,  2),
                ("waste_generation", 0.4,  1),
            ],
            "ana@campus.edu": [
                ("transportation",   1.1, 8),
                ("energy_usage",     0.9, 4),
                ("waste_generation", 0.3, 2),
            ],
            "ramirez@campus.edu": [
                ("transportation",   3.2, 15),
                ("energy_usage",     2.1,  7),
            ],
            "admin@campus.edu": [
                ("energy_usage",     1.8, 12),
                ("transportation",   0.6,  3),
            ],
        }
        for email, records in carbon_spec.items():
            user = users[email]
            existing = db.query(CarbonFootprint).filter(CarbonFootprint.user_id == user.id).count()
            if existing == 0:
                for activity, emission, days_ago in records:
                    db.add(CarbonFootprint(
                        user_id=user.id,
                        activity_type=activity,
                        carbon_emission_estimate=emission,
                        recorded_at=now - timedelta(days=days_ago),
                    ))
                db.commit()
                print(f"  {email:35} -> {len(records)} records")
            else:
                print(f"  {email:35} -> {existing} records (skip)")

        # ── Trees Planted ──────────────────────────────────────────────────
        print("\nTrees Planted:")
        trees_spec = [
            ("carlos@campus.edu",  "Green Area",           "Roble",     10),
            ("carlos@campus.edu",  "Green Area",           "Cedro",      8),
            ("ana@campus.edu",     "Green Area",           "Pino",       5),
            ("ana@campus.edu",     "Library",              "Araucaria",  3),
            ("ramirez@campus.edu", "Engineering Building", "Eucalipto",  7),
            ("admin@campus.edu",   "Green Area",           "Naranjo",    1),
        ]
        zones_by_name = {z.name: z for z in db.query(CampusZone).all()}
        for email, zone_name, species, days_ago in trees_spec:
            user = users[email]
            zone = zones_by_name.get(zone_name)
            if not zone:
                print(f"  WARN zone not found: '{zone_name}'. Available: {list(zones_by_name.keys())}")
                continue
            exists = db.query(TreesPlanted).filter(
                TreesPlanted.user_id == user.id,
                TreesPlanted.tree_species == species,
            ).first()
            if not exists:
                db.add(TreesPlanted(
                    user_id=user.id, zone_id=zone.id, tree_species=species,
                    planting_date=now - timedelta(days=days_ago),
                ))
        db.commit()
        print(f"  Total trees in DB: {db.query(TreesPlanted).count()}")

        # ── Hackathons, Teams, Projects ────────────────────────────────────
        print("\nHackathons:")
        hack_specs = [
            ("Green Energy Challenge 2026",
             "Design innovative renewable energy solutions for the campus.",
             datetime(2026, 3, 1).date(), datetime(2026, 3, 31).date(), "active"),
            ("Zero Waste Campus Sprint",
             "48-hour hackathon: eliminate single-use plastics across campus.",
             datetime(2026, 4, 15).date(), datetime(2026, 4, 17).date(), "upcoming"),
            ("Biodiversity Mapping Initiative",
             "Students used data science to map and improve campus biodiversity.",
             datetime(2025, 11, 1).date(), datetime(2025, 11, 30).date(), "completed"),
        ]
        hacks = []
        for title, desc, sd, ed, status in hack_specs:
            h = db.query(Hackathon).filter(Hackathon.title == title).first()
            if not h:
                h = Hackathon(title=title, description=desc, start_date=sd, end_date=ed, status=status)
                db.add(h)
                db.flush()
                print(f"  created: {title}")
            else:
                print(f"  exists:  {title}")
            hacks.append(h)
        db.commit()

        teams_spec = [
            # hack index: 0 (active)
            [("Solar Innovators",   ["carlos@campus.edu", "ana@campus.edu"]),
             ("Wind Pioneers",      ["ramirez@campus.edu"]),
             ("EcoBuild Solutions", ["admin@campus.edu"])],
            # hack index: 1 (upcoming)
            [("Zero Heroes",        ["ana@campus.edu", "carlos@campus.edu"]),
             ("Green Warriors",     ["ramirez@campus.edu"])],
            # hack index: 2 (completed)
            [("Nature Mappers",     ["carlos@campus.edu"]),
             ("Eco Analysts",       ["ana@campus.edu", "ramirez@campus.edu"])],
        ]
        project_specs = [
            [("Solar Innovators",   "Campus Solar Grid",         "Proposal to install 200 solar panels, reducing energy by 35%.", 88.5),
             ("Wind Pioneers",      "Micro-Wind Network",        "Distributed small wind turbines in high-wind corridors.",        74.2),
             ("EcoBuild Solutions", "Smart Energy Dashboard",    "Real-time energy monitoring integrated with HVAC for 20% savings.", 81.0)],
            [],
            [("Nature Mappers",     "Campus Green Atlas",        "Interactive biodiversity map of all campus green areas.",        92.3),
             ("Eco Analysts",       "Pollinator Corridor Study", "Statistical analysis of bee/butterfly corridors.",               85.7)],
        ]
        for i, hack in enumerate(hacks):
            team_map = {}
            for team_name, member_emails in teams_spec[i]:
                t = db.query(Team).filter(Team.team_name == team_name, Team.hackathon_id == hack.id).first()
                if not t:
                    t = Team(team_name=team_name, hackathon_id=hack.id, created_at=now)
                    db.add(t)
                    db.flush()
                team_map[team_name] = t
                for email in member_emails:
                    u = users.get(email)
                    if u and not db.query(TeamMember).filter(
                        TeamMember.team_id == t.id, TeamMember.user_id == u.id
                    ).first():
                        db.add(TeamMember(team_id=t.id, user_id=u.id))
            for team_name, title, desc, impact in project_specs[i]:
                t = team_map.get(team_name)
                if t and not db.query(Project).filter(Project.team_id == t.id, Project.title == title).first():
                    db.add(Project(
                        team_id=t.id, title=title, description=desc,
                        submission_date=now - timedelta(days=2), impact_score=impact,
                    ))
        db.commit()

        # ── Sustainability Scores ──────────────────────────────────────────
        print("\nSustainability Scores:")
        zone_score_map = {
            "Library":              (78.5, 82.0, 75.0),
            "Engineering Building": (65.2, 70.0, 62.0),
            "Cafeteria":            (71.8, 68.0, 74.0),
            "Green Area":           (88.3, 90.0, 86.5),
        }
        for zname, (score, e_idx, c_idx) in zone_score_map.items():
            zone = zones_by_name.get(zname)
            if not zone:
                continue
            if not db.query(SustainabilityScore).filter(SustainabilityScore.zone_id == zone.id).first():
                db.add(SustainabilityScore(
                    zone_id=zone.id, sustainability_score=score,
                    energy_efficiency_index=e_idx, carbon_index=c_idx, calculated_at=now,
                ))
                print(f"  added: {zname} -> {score}")
        db.commit()

        # ── Summary ────────────────────────────────────────────────────────
        print("\n=== DONE ===")
        print(f"  Users:         {db.query(User).count()}")
        print(f"  Eco-Actions:   {db.query(EcoAction).count()}")
        print(f"  Green Points:  {db.query(GreenPoints).count()}")
        print(f"  Carbon:        {db.query(CarbonFootprint).count()}")
        print(f"  Trees:         {db.query(TreesPlanted).count()}")
        print(f"  Hackathons:    {db.query(Hackathon).count()}")
        print(f"  Teams:         {db.query(Team).count()}")
        print(f"  Projects:      {db.query(Project).count()}")

    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    populate()
