import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config.database import Base
from datetime import date, timedelta

from backend.models import Badge, CampusZone, Hackathon, User
from backend.services.gamification import DEFAULT_BADGES
from backend.utils.security import hash_password


def main() -> None:
    """Seed the database with initial data."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required to seed data.")

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    admin_email = os.getenv("ADMIN_EMAIL", "admin@greencampus.local")
    admin_password = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")

    if not session.query(User).filter(User.email == admin_email).first():
        session.add(
            User(
                name="Admin",
                email=admin_email,
                role="admin",
                password_hash=hash_password(admin_password),
            )
        )

    default_zones = [
        ("Library", "Main campus library", "0,0"),
        ("Engineering Building", "Engineering classrooms", "1,0"),
        ("Cafeteria", "Student dining area", "0,1"),
        ("Green Areas", "Outdoor gardens", "1,1"),
    ]
    for name, description, coords in default_zones:
        exists = session.query(CampusZone).filter(CampusZone.name == name).first()
        if not exists:
            session.add(
                CampusZone(name=name, description=description, location_coordinates=coords)
            )

    existing_badges = {badge.badge_name for badge in session.query(Badge).all()}
    for badge in DEFAULT_BADGES:
        if badge["badge_name"] not in existing_badges:
            session.add(Badge(**badge))

    if not session.query(Hackathon).filter(Hackathon.title == "Green Launch Challenge").first():
        session.add(
            Hackathon(
                title="Green Launch Challenge",
                description="Kickoff hackathon for sustainability prototypes across campus.",
                start_date=date.today() + timedelta(days=3),
                end_date=date.today() + timedelta(days=5),
                status="open",
            )
        )

    session.commit()
    session.close()


if __name__ == "__main__":
    main()
