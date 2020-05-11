"""Add opened field to notification

Revision ID: 9cbfa7c72c88
Revises: dfcf0d90e1d2
Create Date: 2016-11-13 13:27:06.891000

"""

# revision identifiers, used by Alembic.
revision = '9cbfa7c72c88'
down_revision = 'dfcf0d90e1d2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression


def upgrade():
    op.add_column('notification', sa.Column('opened', sa.Boolean, nullable=False, default=False, server_default=expression.false()))


def downgrade():
    op.drop_column('notification', 'opened')
