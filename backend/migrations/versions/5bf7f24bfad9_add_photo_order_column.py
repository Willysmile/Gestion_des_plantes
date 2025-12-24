"""add_photo_order_column

Revision ID: 5bf7f24bfad9
Revises: 006_add_watering_preferences_to_plants
Create Date: 2025-12-19 05:56:26.519748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bf7f24bfad9'
down_revision: Union[str, None] = '006_add_watering_preferences_to_plants'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ajouter colonne photo_order avec default 0
    op.add_column('photos', sa.Column('photo_order', sa.Integer(), nullable=False, server_default='0'))
    
    # Créer index pour performance
    op.create_index('idx_photos_plant_order', 'photos', ['plant_id', 'photo_order'])


def downgrade() -> None:
    op.drop_index('idx_photos_plant_order', table_name='photos')
    op.drop_column('photos', 'photo_order')
