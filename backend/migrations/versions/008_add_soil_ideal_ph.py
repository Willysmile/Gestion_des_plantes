"""Add soil_ideal_ph column to plants table

Revision ID: 008
Revises: 007
Create Date: 2025-11-10
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '008_add_soil_ideal_ph'
down_revision = '007_add_seasonal_tables'
branch_labels = None
depends_on = None


def upgrade():
    """Add soil_ideal_ph column"""
    op.add_column('plants', sa.Column('soil_ideal_ph', sa.Float(), nullable=True))


def downgrade():
    """Remove soil_ideal_ph column"""
    op.drop_column('plants', 'soil_ideal_ph')
