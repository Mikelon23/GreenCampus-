"""Initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-03-14
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial tables."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)

    op.create_table(
        "campus_zones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location_coordinates", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_campus_zones_id", "campus_zones", ["id"], unique=False)

    op.create_table(
        "sensor_data",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("campus_zones.id"), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Float(), nullable=False),
        sa.Column("co2_level", sa.Float(), nullable=False),
        sa.Column("energy_usage", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_sensor_data_id", "sensor_data", ["id"], unique=False)
    op.create_index("ix_sensor_data_zone_id", "sensor_data", ["zone_id"], unique=False)

    op.create_table(
        "sustainability_scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("campus_zones.id"), nullable=False),
        sa.Column("sustainability_score", sa.Float(), nullable=False),
        sa.Column("energy_efficiency_index", sa.Float(), nullable=False),
        sa.Column("carbon_index", sa.Float(), nullable=False),
        sa.Column("calculated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_sustainability_scores_id", "sustainability_scores", ["id"], unique=False)
    op.create_index(
        "ix_sustainability_scores_zone_id", "sustainability_scores", ["zone_id"], unique=False
    )

    op.create_table(
        "carbon_footprint",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("activity_type", sa.String(length=120), nullable=False),
        sa.Column("carbon_emission_estimate", sa.Float(), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_carbon_footprint_id", "carbon_footprint", ["id"], unique=False)
    op.create_index("ix_carbon_footprint_user_id", "carbon_footprint", ["user_id"], unique=False)

    op.create_table(
        "eco_actions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("action_type", sa.String(length=120), nullable=False),
        sa.Column("points_awarded", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_eco_actions_id", "eco_actions", ["id"], unique=False)
    op.create_index("ix_eco_actions_user_id", "eco_actions", ["user_id"], unique=False)

    op.create_table(
        "green_points",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("total_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_updated", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_green_points_id", "green_points", ["id"], unique=False)
    op.create_index("ix_green_points_user_id", "green_points", ["user_id"], unique=True)

    op.create_table(
        "badges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("badge_name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("points_required", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_badges_id", "badges", ["id"], unique=False)
    op.create_index("ix_badges_badge_name", "badges", ["badge_name"], unique=True)

    op.create_table(
        "user_badges",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("badge_id", sa.Integer(), sa.ForeignKey("badges.id"), nullable=False),
        sa.Column("earned_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_user_badges_id", "user_badges", ["id"], unique=False)
    op.create_index("ix_user_badges_user_id", "user_badges", ["user_id"], unique=False)
    op.create_index("ix_user_badges_badge_id", "user_badges", ["badge_id"], unique=False)

    op.create_table(
        "hackathons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
    )
    op.create_index("ix_hackathons_id", "hackathons", ["id"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("team_name", sa.String(length=120), nullable=False),
        sa.Column("hackathon_id", sa.Integer(), sa.ForeignKey("hackathons.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_teams_id", "teams", ["id"], unique=False)
    op.create_index("ix_teams_hackathon_id", "teams", ["hackathon_id"], unique=False)

    op.create_table(
        "team_members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_index("ix_team_members_id", "team_members", ["id"], unique=False)
    op.create_index("ix_team_members_team_id", "team_members", ["team_id"], unique=False)
    op.create_index("ix_team_members_user_id", "team_members", ["user_id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("submission_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("impact_score", sa.Float(), nullable=True),
    )
    op.create_index("ix_projects_id", "projects", ["id"], unique=False)
    op.create_index("ix_projects_team_id", "projects", ["team_id"], unique=False)

    op.create_table(
        "trees_planted",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("zone_id", sa.Integer(), sa.ForeignKey("campus_zones.id"), nullable=False),
        sa.Column("tree_species", sa.String(length=120), nullable=False),
        sa.Column("planting_date", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_trees_planted_id", "trees_planted", ["id"], unique=False)
    op.create_index("ix_trees_planted_user_id", "trees_planted", ["user_id"], unique=False)
    op.create_index("ix_trees_planted_zone_id", "trees_planted", ["zone_id"], unique=False)


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index("ix_trees_planted_zone_id", table_name="trees_planted")
    op.drop_index("ix_trees_planted_user_id", table_name="trees_planted")
    op.drop_index("ix_trees_planted_id", table_name="trees_planted")
    op.drop_table("trees_planted")

    op.drop_index("ix_projects_team_id", table_name="projects")
    op.drop_index("ix_projects_id", table_name="projects")
    op.drop_table("projects")

    op.drop_index("ix_team_members_user_id", table_name="team_members")
    op.drop_index("ix_team_members_team_id", table_name="team_members")
    op.drop_index("ix_team_members_id", table_name="team_members")
    op.drop_table("team_members")

    op.drop_index("ix_teams_hackathon_id", table_name="teams")
    op.drop_index("ix_teams_id", table_name="teams")
    op.drop_table("teams")

    op.drop_index("ix_hackathons_id", table_name="hackathons")
    op.drop_table("hackathons")

    op.drop_index("ix_user_badges_badge_id", table_name="user_badges")
    op.drop_index("ix_user_badges_user_id", table_name="user_badges")
    op.drop_index("ix_user_badges_id", table_name="user_badges")
    op.drop_table("user_badges")

    op.drop_index("ix_badges_badge_name", table_name="badges")
    op.drop_index("ix_badges_id", table_name="badges")
    op.drop_table("badges")

    op.drop_index("ix_green_points_user_id", table_name="green_points")
    op.drop_index("ix_green_points_id", table_name="green_points")
    op.drop_table("green_points")

    op.drop_index("ix_eco_actions_user_id", table_name="eco_actions")
    op.drop_index("ix_eco_actions_id", table_name="eco_actions")
    op.drop_table("eco_actions")

    op.drop_index("ix_carbon_footprint_user_id", table_name="carbon_footprint")
    op.drop_index("ix_carbon_footprint_id", table_name="carbon_footprint")
    op.drop_table("carbon_footprint")

    op.drop_index("ix_sustainability_scores_zone_id", table_name="sustainability_scores")
    op.drop_index("ix_sustainability_scores_id", table_name="sustainability_scores")
    op.drop_table("sustainability_scores")

    op.drop_index("ix_sensor_data_zone_id", table_name="sensor_data")
    op.drop_index("ix_sensor_data_id", table_name="sensor_data")
    op.drop_table("sensor_data")

    op.drop_index("ix_campus_zones_id", table_name="campus_zones")
    op.drop_table("campus_zones")

    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
