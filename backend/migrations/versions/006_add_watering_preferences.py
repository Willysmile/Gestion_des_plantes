"""Add watering preferences to plants table

Revision ID: 006_add_watering_preferences
Revises: 005_add_watering_configuration_tables
Create Date: 2025-11-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006_add_watering_preferences'
down_revision = '005_add_watering_configuration_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('plants', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preferred_watering_method_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('preferred_water_type_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('plants', schema=None) as batch_op:
        batch_op.drop_column('preferred_water_type_id')
        batch_op.drop_column('preferred_watering_method_id')
