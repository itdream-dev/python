"""create user_permission table

Revision ID: 02bb96579aa1
Revises: 2042e7801a91
Create Date: 2016-11-09 18:33:50.948000

"""

# revision identifiers, used by Alembic.
revision = '02bb96579aa1'
down_revision = '2042e7801a91'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'user_permission',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('card_id', sa.String(255), nullable=False),
        sa.Column('permission_id', sa.String(255), nullable=False),
    )


def downgrade():
    op.drop_table('user_permission')
