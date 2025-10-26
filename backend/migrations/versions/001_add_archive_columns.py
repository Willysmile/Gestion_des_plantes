"""Add archived_date and archived_reason to plants

Revision ID: 001_add_archive_columns
Revises: 
Create Date: 2025-10-26 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_add_archive_columns'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to plants table
    op.add_column('plants', sa.Column('archived_date', sa.DateTime(), nullable=True))
    op.add_column('plants', sa.Column('archived_reason', sa.String(255), nullable=True))


def downgrade() -> None:
    # Remove columns if downgrading
    op.drop_column('plants', 'archived_reason')
    op.drop_column('plants', 'archived_date')
