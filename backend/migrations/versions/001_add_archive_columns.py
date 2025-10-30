"""Add archived_date and archived_reason to plants

Revision ID: 001_add_archive_columns
Revises: 000_create_plants_table
Create Date: 2025-10-26 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_archive_columns'
down_revision = '000_create_plants_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Columns already exist in base schema from 000_create_plants_table
    # This migration is now a no-op
    pass


def downgrade() -> None:
    # This migration is now a no-op
    pass
