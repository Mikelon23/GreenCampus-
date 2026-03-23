"""Expand gamification, ownership, and campus goals

Revision ID: 0003_gamification_expansion
Revises: 0002_add_project_file_url
Create Date: 2026-03-18
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_gamification_expansion"
down_revision = "0002_add_project_file_url"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply gamification expansion schema changes."""
    op.add_column("users", sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("best_streak", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("last_green_action_at", sa.DateTime(timezone=True), nullable=True))

    op.add_column("teams", sa.Column("created_by_user_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_teams_created_by_user_id", "teams", "users", ["created_by_user_id"], ["id"])
    op.create_index("ix_teams_created_by_user_id", "teams", ["created_by_user_id"], unique=False)

    op.add_column("projects", sa.Column("created_by_user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_projects_created_by_user_id", "projects", "users", ["created_by_user_id"], ["id"]
    )
    op.create_index("ix_projects_created_by_user_id", "projects", ["created_by_user_id"], unique=False)

    op.create_table(
        "eco_energy",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("source_type", sa.String(length=60), nullable=False),
        sa.Column("source_ref_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="available"),
        sa.Column("available_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_eco_energy_id", "eco_energy", ["id"], unique=False)
    op.create_index("ix_eco_energy_owner_user_id", "eco_energy", ["owner_user_id"], unique=False)

    op.create_table(
        "energy_interactions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("energy_id", sa.Integer(), sa.ForeignKey("eco_energy.id"), nullable=False),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("interaction_type", sa.String(length=30), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_energy_interactions_id", "energy_interactions", ["id"], unique=False)
    op.create_index("ix_energy_interactions_energy_id", "energy_interactions", ["energy_id"], unique=False)
    op.create_index(
        "ix_energy_interactions_actor_user_id", "energy_interactions", ["actor_user_id"], unique=False
    )
    op.create_index(
        "ix_energy_interactions_target_user_id", "energy_interactions", ["target_user_id"], unique=False
    )

    op.create_table(
        "user_trees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("species", sa.String(length=120), nullable=False, server_default="Campus Oak"),
        sa.Column("nickname", sa.String(length=120), nullable=False, server_default="My Green Tree"),
        sa.Column("stage", sa.String(length=30), nullable=False, server_default="seed"),
        sa.Column("growth_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_energy_contributed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_user_trees_id", "user_trees", ["id"], unique=False)
    op.create_index("ix_user_trees_user_id", "user_trees", ["user_id"], unique=True)

    op.create_table(
        "campus_goals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("target_energy", sa.Integer(), nullable=False),
        sa.Column("current_energy", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reward_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="active"),
    )
    op.create_index("ix_campus_goals_id", "campus_goals", ["id"], unique=False)

    op.create_table(
        "goal_contributions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("goal_id", sa.Integer(), sa.ForeignKey("campus_goals.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("contributed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_goal_contributions_id", "goal_contributions", ["id"], unique=False)
    op.create_index("ix_goal_contributions_goal_id", "goal_contributions", ["goal_id"], unique=False)
    op.create_index("ix_goal_contributions_user_id", "goal_contributions", ["user_id"], unique=False)


def downgrade() -> None:
    """Revert gamification expansion schema changes."""
    op.drop_index("ix_goal_contributions_user_id", table_name="goal_contributions")
    op.drop_index("ix_goal_contributions_goal_id", table_name="goal_contributions")
    op.drop_index("ix_goal_contributions_id", table_name="goal_contributions")
    op.drop_table("goal_contributions")

    op.drop_index("ix_campus_goals_id", table_name="campus_goals")
    op.drop_table("campus_goals")

    op.drop_index("ix_user_trees_user_id", table_name="user_trees")
    op.drop_index("ix_user_trees_id", table_name="user_trees")
    op.drop_table("user_trees")

    op.drop_index("ix_energy_interactions_target_user_id", table_name="energy_interactions")
    op.drop_index("ix_energy_interactions_actor_user_id", table_name="energy_interactions")
    op.drop_index("ix_energy_interactions_energy_id", table_name="energy_interactions")
    op.drop_index("ix_energy_interactions_id", table_name="energy_interactions")
    op.drop_table("energy_interactions")

    op.drop_index("ix_eco_energy_owner_user_id", table_name="eco_energy")
    op.drop_index("ix_eco_energy_id", table_name="eco_energy")
    op.drop_table("eco_energy")

    op.drop_index("ix_projects_created_by_user_id", table_name="projects")
    op.drop_constraint("fk_projects_created_by_user_id", "projects", type_="foreignkey")
    op.drop_column("projects", "created_by_user_id")

    op.drop_index("ix_teams_created_by_user_id", table_name="teams")
    op.drop_constraint("fk_teams_created_by_user_id", "teams", type_="foreignkey")
    op.drop_column("teams", "created_by_user_id")

    op.drop_column("users", "last_green_action_at")
    op.drop_column("users", "best_streak")
    op.drop_column("users", "current_streak")
