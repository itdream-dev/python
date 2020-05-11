"""remove user_permission table

Revision ID: ad71dda5de4b
Revises: 5c07ffa6a09b
Create Date: 2016-11-18 10:47:04.692000

"""

# revision identifiers, used by Alembic.
revision = 'ad71dda5de4b'
down_revision = '5c07ffa6a09b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_table('user_permission')


def downgrade():
    op.create_table(
        'user_permission',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('card_id', sa.String(255), nullable=False),
        sa.Column('permission_id', sa.String(255), nullable=False),
    )
