"""Initial schema - Create plants table

Revision ID: 000_create_plants_table
Revises: 
Create Date: 2025-10-31

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000_create_plants_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create plants table
    op.create_table(
        'plants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('scientific_name', sa.String(length=150), nullable=True),
        sa.Column('family', sa.String(length=100), nullable=True),
        sa.Column('subfamily', sa.String(length=100), nullable=True),
        sa.Column('genus', sa.String(length=100), nullable=True),
        sa.Column('species', sa.String(length=100), nullable=True),
        sa.Column('subspecies', sa.String(length=100), nullable=True),
        sa.Column('variety', sa.String(length=100), nullable=True),
        sa.Column('cultivar', sa.String(length=100), nullable=True),
        sa.Column('reference', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('health_status', sa.String(length=50), nullable=True),
        sa.Column('difficulty_level', sa.String(length=50), nullable=True),
        sa.Column('growth_speed', sa.String(length=50), nullable=True),
        sa.Column('flowering_season', sa.String(length=100), nullable=True),
        sa.Column('location_id', sa.Integer(), nullable=True),
        sa.Column('purchase_date', sa.String(length=20), nullable=True),
        sa.Column('purchase_place_id', sa.Integer(), nullable=True),
        sa.Column('purchase_price', sa.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column('watering_frequency_id', sa.Integer(), nullable=True),
        sa.Column('light_requirement_id', sa.Integer(), nullable=True),
        sa.Column('temperature_min', sa.Integer(), nullable=True),
        sa.Column('temperature_max', sa.Integer(), nullable=True),
        sa.Column('humidity_level', sa.Integer(), nullable=True),
        sa.Column('soil_humidity', sa.String(length=50), nullable=True),
        sa.Column('soil_type', sa.String(length=100), nullable=True),
        sa.Column('pot_size', sa.String(length=50), nullable=True),
        sa.Column('is_indoor', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('is_outdoor', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('is_favorite', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('is_toxic', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('is_archived', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('archived_date', sa.DateTime(), nullable=True),
        sa.Column('archived_reason', sa.String(length=255), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_plants_name'), 'plants', ['name'], unique=False)
    op.create_index(op.f('ix_plants_reference'), 'plants', ['reference'], unique=True)
    op.create_index(op.f('ix_plants_is_archived'), 'plants', ['is_archived'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_plants_is_archived'), table_name='plants')
    op.drop_index(op.f('ix_plants_reference'), table_name='plants')
    op.drop_index(op.f('ix_plants_name'), table_name='plants')
    op.drop_table('plants')
