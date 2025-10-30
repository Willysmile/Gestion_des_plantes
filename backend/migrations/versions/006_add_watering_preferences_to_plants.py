"""Add watering preferences to plants table

Revision ID: 006_add_watering_preferences_to_plants
Revises: 005_add_watering_configuration_tables
Create Date: 2025-10-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006_add_watering_preferences_to_plants'
down_revision = '005_add_watering_configuration_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to plants table
    op.add_column('plants', sa.Column('preferred_watering_method_id', sa.Integer(), nullable=True))
    op.add_column('plants', sa.Column('preferred_water_type_id', sa.Integer(), nullable=True))
    
    # Add foreign key constraints
    op.create_foreign_key(
        'fk_plants_preferred_watering_method_id',
        'plants',
        'watering_methods',
        ['preferred_watering_method_id'],
        ['id'],
        ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_plants_preferred_water_type_id',
        'plants',
        'water_types',
        ['preferred_water_type_id'],
        ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # Remove foreign key constraints
    op.drop_constraint('fk_plants_preferred_water_type_id', 'plants', type_='foreignkey')
    op.drop_constraint('fk_plants_preferred_watering_method_id', 'plants', type_='foreignkey')
    
    # Remove columns
    op.drop_column('plants', 'preferred_water_type_id')
    op.drop_column('plants', 'preferred_watering_method_id')
