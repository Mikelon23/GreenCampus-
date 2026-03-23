"""Add file_url to projects

Revision ID: 0002_add_project_file_url
Revises: 0001_initial
Create Date: 2026-03-17
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_project_file_url"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add uploaded project file path."""
    op.add_column("projects", sa.Column("file_url", sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Remove uploaded project file path."""
    op.drop_column("projects", "file_url")
