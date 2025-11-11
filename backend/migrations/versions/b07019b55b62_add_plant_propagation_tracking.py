"""Add plant propagation tracking

Revision ID: b07019b55b62
Revises: 009_add_audit_logs_table
Create Date: 2025-11-11 20:42:02.797965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b07019b55b62'
down_revision: Union[str, None] = '009_add_audit_logs_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create plant_propagations table
    op.create_table(
        'plant_propagations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('parent_plant_id', sa.Integer(), nullable=False),
        sa.Column('child_plant_id', sa.Integer(), nullable=True),
        sa.Column('source_type', sa.String(50), nullable=False),  # cutting, seeds, division, offset
        sa.Column('method', sa.String(50), nullable=False),  # water, soil, air-layer, substrate
        sa.Column('propagation_date', sa.Date(), nullable=False),
        sa.Column('date_harvested', sa.Date(), nullable=False),
        sa.Column('expected_ready', sa.Date(), nullable=True),
        sa.Column('success_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(50), server_default='pending', nullable=False),  # pending, rooting, rooted, growing, ready-to-pot, potted, established, failed, abandoned
        sa.Column('current_root_length_cm', sa.Float(), nullable=True),
        sa.Column('current_leaves_count', sa.Integer(), nullable=True),
        sa.Column('current_roots_count', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('success_rate_estimate', sa.Float(), server_default='0.85', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.ForeignKeyConstraint(['parent_plant_id'], ['plants.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['child_plant_id'], ['plants.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('parent_plant_id != child_plant_id', name='no_self_parent')
    )

    # Create indices
    op.create_index('idx_parent_plant', 'plant_propagations', ['parent_plant_id'])
    op.create_index('idx_child_plant', 'plant_propagations', ['child_plant_id'])
    op.create_index('idx_status', 'plant_propagations', ['status'])
    op.create_index('idx_source_method', 'plant_propagations', ['source_type', 'method'])

    # Create propagation_events table
    op.create_table(
        'propagation_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('propagation_id', sa.Integer(), nullable=False),
        sa.Column('event_date', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),  # rooted, leaves-grown, ready-to-pot, potted, failed
        sa.Column('measurement', sa.JSON(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('photo_url', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp(), nullable=False),
        sa.ForeignKeyConstraint(['propagation_id'], ['plant_propagations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indices for events
    op.create_index('idx_propagation_events', 'propagation_events', ['propagation_id', 'event_date'])


def downgrade() -> None:
    # Drop propagation tables first
    op.drop_index('idx_propagation_events', table_name='propagation_events')
    op.drop_table('propagation_events')
    
    op.drop_index('idx_source_method', table_name='plant_propagations')
    op.drop_index('idx_status', table_name='plant_propagations')
    op.drop_index('idx_child_plant', table_name='plant_propagations')
    op.drop_index('idx_parent_plant', table_name='plant_propagations')
    op.drop_table('plant_propagations')
