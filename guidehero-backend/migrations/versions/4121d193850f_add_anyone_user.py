"""add anyone user

Revision ID: 4121d193850f
Revises: ad71dda5de4b
Create Date: 2016-11-18 11:49:36.017000

"""

# revision identifiers, used by Alembic.
revision = '4121d193850f'
down_revision = 'ad71dda5de4b'

from alembic import op
from sqlalchemy.sql import text
# import sqlalchemy as sa


def upgrade():
    from lib.models.user import User
    table = User.__table__
    sql = 'INSERT INTO "user" (id, username) VALUES (:id, :username)'
    op.get_bind().execute(text(sql), **{'id': User.ANYONE_ID, 'username': 'Anyone'})


def downgrade():
    from lib.models.user import User
    table = User.__table__
    op.execute(
        table.delete().where(table.c.id == op.inline_literal(User.ANYONE_ID))
    )
