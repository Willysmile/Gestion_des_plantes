"""Add seasonal watering and fertilizing tables

Revision ID: 007_add_seasonal_tables
Revises: 006_add_watering_preferences
Create Date: 2025-11-02

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007_add_seasonal_tables'
down_revision = '006_add_watering_preferences'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create plant_seasonal_watering table
    op.create_table(
        'plant_seasonal_watering',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plant_id', sa.Integer(), nullable=False),
        sa.Column('season_id', sa.Integer(), nullable=False),
        sa.Column('watering_frequency_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['season_id'], ['seasons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['watering_frequency_id'], ['watering_frequencies.id']),
        sa.UniqueConstraint('plant_id', 'season_id', name='_plant_season_uc')
    )

    # Create plant_seasonal_fertilizing table
    op.create_table(
        'plant_seasonal_fertilizing',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plant_id', sa.Integer(), nullable=False),
        sa.Column('season_id', sa.Integer(), nullable=False),
        sa.Column('fertilizer_frequency_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['season_id'], ['seasons.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['fertilizer_frequency_id'], ['fertilizer_frequencies.id']),
        sa.UniqueConstraint('plant_id', 'season_id', name='_plant_season_fert_uc')
    )


def downgrade() -> None:
    op.drop_table('plant_seasonal_fertilizing')
    op.drop_table('plant_seasonal_watering')
