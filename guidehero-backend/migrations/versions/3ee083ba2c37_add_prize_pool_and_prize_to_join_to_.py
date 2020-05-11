"""Add prize_pool and prize_to_join to card model

Revision ID: 3ee083ba2c37
Revises: 4121d193850f
Create Date: 2016-11-23 11:21:12.199000

"""

# revision identifiers, used by Alembic.
revision = '3ee083ba2c37'
down_revision = '4121d193850f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('card', sa.Column('prize_pool', sa.Integer, nullable=False, default=0, server_default='0'))
    op.add_column('card', sa.Column('prize_to_join', sa.Integer, nullable=False, default=0, server_default='0'))


def downgrade():
    op.drop_column('card', 'prize_pool')
    op.drop_column('card', 'prize_to_join')
