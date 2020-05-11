"""Add role_id field to user_peermission table

Revision ID: dfcf0d90e1d2
Revises: 02bb96579aa1
Create Date: 2016-11-11 15:04:41.168000

"""

# revision identifiers, used by Alembic.
revision = 'dfcf0d90e1d2'
down_revision = '02bb96579aa1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user_permission', sa.Column('role_id', sa.Integer, nullable=True))
    op.alter_column('user_permission', 'user_id', nullable=True)


def downgrade():
    op.alter_column('user_permission', 'user_id', nullable=False)
    op.drop_column('user_permission', 'role_id')
