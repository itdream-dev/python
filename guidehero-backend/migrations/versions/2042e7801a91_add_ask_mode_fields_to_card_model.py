"""add ask mode fields to card model

Revision ID: 2042e7801a91
Revises: 1a80cb60ea27
Create Date: 2016-11-08 19:52:47.247000

"""

# revision identifiers, used by Alembic.
revision = '2042e7801a91'
down_revision = '1a80cb60ea27'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('card', sa.Column('is_ask_mode_enabled', sa.Boolean))
    op.add_column('card', sa.Column('format', sa.Text))


def downgrade():
    op.drop_column('card', 'is_ask_mode_enabled')
    op.drop_column('card', 'format')
