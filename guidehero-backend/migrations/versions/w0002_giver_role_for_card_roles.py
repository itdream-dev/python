"""giver role for card roles

Revision ID: w0002
Revises: w0001
Create Date: 2016-12-01 10:06:53.104000

"""

# revision identifiers, used by Alembic.
revision = 'w0002'
down_revision = 'w0001'

from alembic import op
from sqlalchemy.sql import text


def upgrade():
    from lib.models.card_role import CardRole
    table = CardRole.__table__
    sql = 'INSERT INTO "{}" (id) VALUES (:id)'.format(table.name)
    op.get_bind().execute(text(sql), **{'id': CardRole.GIVER})


def downgrade():
    from lib.models.card_role import CardRole
    table = CardRole.__table__
    sql = 'DELETE FROM "{}" WHERE id=:id'.format(table.name)
    op.get_bind().execute(text(sql), **{'id': CardRole.GIVER})
