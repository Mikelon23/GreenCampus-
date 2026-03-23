from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from backend.config.database import Base


class User(Base):
    """Represents a platform user account."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    role = Column(String(30), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    current_streak = Column(Integer, nullable=False, default=0)
    best_streak = Column(Integer, nullable=False, default=0)
    last_green_action_at = Column(DateTime(timezone=True), nullable=True)

    eco_actions = relationship("EcoAction", back_populates="user")
    carbon_footprints = relationship("CarbonFootprint", back_populates="user")
    green_points = relationship("GreenPoints", back_populates="user", uselist=False)
    user_badges = relationship("UserBadge", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")
    trees_planted = relationship("TreesPlanted", back_populates="user")
    owned_teams = relationship("Team", back_populates="creator")
    created_projects = relationship("Project", back_populates="creator")
    energy_drops = relationship("EcoEnergy", back_populates="owner")
    tree_profile = relationship("UserTree", back_populates="user", uselist=False)
    goal_contributions = relationship("GoalContribution", back_populates="user")


class CampusZone(Base):
    """Represents a campus zone where environmental data is collected."""

    __tablename__ = "campus_zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    location_coordinates = Column(String(255), nullable=True)

    sensor_data = relationship("SensorData", back_populates="zone")
    sustainability_scores = relationship("SustainabilityScore", back_populates="zone")
    trees_planted = relationship("TreesPlanted", back_populates="zone")


class SensorData(Base):
    """Stores raw environmental sensor readings."""

    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("campus_zones.id"), nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    co2_level = Column(Float, nullable=False)
    energy_usage = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    zone = relationship("CampusZone", back_populates="sensor_data")


class SustainabilityScore(Base):
    """Stores calculated sustainability indicators for zones."""

    __tablename__ = "sustainability_scores"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("campus_zones.id"), nullable=False, index=True)
    sustainability_score = Column(Float, nullable=False)
    energy_efficiency_index = Column(Float, nullable=False)
    carbon_index = Column(Float, nullable=False)
    calculated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    zone = relationship("CampusZone", back_populates="sustainability_scores")


class CarbonFootprint(Base):
    """Tracks carbon footprint estimates for user activities."""

    __tablename__ = "carbon_footprint"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_type = Column(String(120), nullable=False)
    carbon_emission_estimate = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="carbon_footprints")


class EcoAction(Base):
    """Records sustainability actions performed by users."""

    __tablename__ = "eco_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action_type = Column(String(120), nullable=False)
    points_awarded = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="eco_actions")


class GreenPoints(Base):
    """Stores accumulated green points for users."""

    __tablename__ = "green_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    total_points = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="green_points")


class Badge(Base):
    """Defines badge requirements for sustainability achievements."""

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    badge_name = Column(String(120), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    points_required = Column(Integer, nullable=False, default=0)

    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """Associates badges with users."""

    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False, index=True)
    earned_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")


class Hackathon(Base):
    """Stores sustainability hackathon events."""

    __tablename__ = "hackathons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)

    teams = relationship("Team", back_populates="hackathon")


class Team(Base):
    """Represents a team participating in a hackathon."""

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(120), nullable=False)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False, index=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    hackathon = relationship("Hackathon", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")
    projects = relationship("Project", back_populates="team")
    creator = relationship("User", back_populates="owned_teams")


class TeamMember(Base):
    """Associates users with hackathon teams."""

    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")


class Project(Base):
    """Stores hackathon project submissions."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    submission_date = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    impact_score = Column(Float, nullable=True)
    file_url = Column(String(255), nullable=True)

    team = relationship("Team", back_populates="projects")
    creator = relationship("User", back_populates="created_projects")


class TreesPlanted(Base):
    """Tracks tree planting activities."""

    __tablename__ = "trees_planted"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    zone_id = Column(Integer, ForeignKey("campus_zones.id"), nullable=False, index=True)
    tree_species = Column(String(120), nullable=False)
    planting_date = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="trees_planted")
    zone = relationship("CampusZone", back_populates="trees_planted")


class EcoEnergy(Base):
    """Stores collectible energy generated from sustainable actions."""

    __tablename__ = "eco_energy"

    id = Column(Integer, primary_key=True, index=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source_type = Column(String(60), nullable=False)
    source_ref_id = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=False, default=0)
    status = Column(String(30), nullable=False, default="available")
    available_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    collected_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="energy_drops")
    interactions = relationship("EnergyInteraction", back_populates="energy_drop")


class EnergyInteraction(Base):
    """Tracks social interactions around collectible energy."""

    __tablename__ = "energy_interactions"

    id = Column(Integer, primary_key=True, index=True)
    energy_id = Column(Integer, ForeignKey("eco_energy.id"), nullable=False, index=True)
    actor_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    interaction_type = Column(String(30), nullable=False)
    amount = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    energy_drop = relationship("EcoEnergy", back_populates="interactions")


class UserTree(Base):
    """Represents the user-facing virtual tree that grows with contributions."""

    __tablename__ = "user_trees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    species = Column(String(120), nullable=False, default="Campus Oak")
    nickname = Column(String(120), nullable=False, default="My Green Tree")
    stage = Column(String(30), nullable=False, default="seed")
    growth_points = Column(Integer, nullable=False, default=0)
    total_energy_contributed = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="tree_profile")


class CampusGoal(Base):
    """Stores collaborative campus-wide sustainability goals."""

    __tablename__ = "campus_goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    target_energy = Column(Integer, nullable=False)
    current_energy = Column(Integer, nullable=False, default=0)
    reward_points = Column(Integer, nullable=False, default=0)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(30), nullable=False, default="active")

    contributions = relationship("GoalContribution", back_populates="goal")


class GoalContribution(Base):
    """Tracks which users contributed energy toward campus goals."""

    __tablename__ = "goal_contributions"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("campus_goals.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Integer, nullable=False, default=0)
    contributed_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    goal = relationship("CampusGoal", back_populates="contributions")
    user = relationship("User", back_populates="goal_contributions")
