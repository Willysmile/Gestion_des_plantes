"""
Add photos table for plant photo gallery

Revision ID: 002_add_photos_table
Revises: 001_add_archive_columns
Create Date: 2025-10-26 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_photos_table'
down_revision = '001_add_archive_columns'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create photos table
    op.create_table(
        'photos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plant_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['plant_id'], ['plants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_photos_plant_id'), 'photos', ['plant_id'], unique=False)
    op.create_index(op.f('ix_photos_is_primary'), 'photos', ['is_primary'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_photos_is_primary'), table_name='photos')
    op.drop_index(op.f('ix_photos_plant_id'), table_name='photos')
    op.drop_table('photos')
