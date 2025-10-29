"""Add disease lookup tables

Revision ID: 004_add_disease_lookup_tables
Revises: 003_add_unit_to_fertilizer_types
Create Date: 2025-10-28

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_disease_lookup_tables'
down_revision = '003_add_unit_to_fertilizer_types'
branch_labels = None
depends_on = None


def upgrade():
    # Create DiseaseType table
    op.create_table('disease_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create TreatmentType table
    op.create_table('treatment_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create PlantHealthStatus table
    op.create_table('plant_health_statuses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add foreign keys to disease_histories
    op.add_column('disease_histories', sa.Column('disease_type_id', sa.Integer(), nullable=True))
    op.add_column('disease_histories', sa.Column('treatment_type_id', sa.Integer(), nullable=True))
    op.add_column('disease_histories', sa.Column('health_status_id', sa.Integer(), nullable=True))
    
    op.create_foreign_key('fk_disease_histories_disease_type_id', 'disease_histories', 'disease_types', ['disease_type_id'], ['id'])
    op.create_foreign_key('fk_disease_histories_treatment_type_id', 'disease_histories', 'treatment_types', ['treatment_type_id'], ['id'])
    op.create_foreign_key('fk_disease_histories_health_status_id', 'disease_histories', 'plant_health_statuses', ['health_status_id'], ['id'])


def downgrade():
    # Drop foreign keys
    op.drop_constraint('fk_disease_histories_disease_type_id', 'disease_histories', type_='foreignkey')
    op.drop_constraint('fk_disease_histories_treatment_type_id', 'disease_histories', type_='foreignkey')
    op.drop_constraint('fk_disease_histories_health_status_id', 'disease_histories', type_='foreignkey')
    
    # Drop columns
    op.drop_column('disease_histories', 'disease_type_id')
    op.drop_column('disease_histories', 'treatment_type_id')
    op.drop_column('disease_histories', 'health_status_id')
    
    # Drop tables
    op.drop_table('plant_health_statuses')
    op.drop_table('treatment_types')
    op.drop_table('disease_types')
