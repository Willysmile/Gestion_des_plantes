"""
Add unit field to fertilizer_types table

Revision ID: 003_add_unit_to_fertilizer_types
Revises: 002_add_photos_table
Create Date: 2025-10-28 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_unit_to_fertilizer_types'
down_revision = '002_add_photos_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add unit column to fertilizer_types table
    op.add_column(
        'fertilizer_types',
        sa.Column('unit', sa.String(length=50), nullable=False, server_default='ml')
    )


def downgrade() -> None:
    # Remove unit column
    op.drop_column('fertilizer_types', 'unit')
