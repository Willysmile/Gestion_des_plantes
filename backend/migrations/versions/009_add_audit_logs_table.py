"""Add audit_logs table

Revision ID: 009
Revises: 008
Create Date: 2025-11-10
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '009_add_audit_logs_table'
down_revision = '008_add_soil_ideal_ph'
branch_labels = None
depends_on = None


def upgrade():
    """Create audit_logs table"""
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(20), nullable=False, index=True),
        sa.Column('entity_type', sa.String(100), nullable=False, index=True),
        sa.Column('entity_id', sa.Integer(), nullable=False, index=True),
        sa.Column('field_name', sa.String(100), nullable=True),
        sa.Column('old_value', sa.Text(), nullable=True),
        sa.Column('new_value', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True, index=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(255), nullable=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('raw_changes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    """Drop audit_logs table"""
    op.drop_table('audit_logs')

