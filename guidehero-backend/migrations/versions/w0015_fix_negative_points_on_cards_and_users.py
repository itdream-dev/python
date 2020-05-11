"""Fix negative points on cards and users

Revision ID: w0015
Revises: w0014
Create Date: 2017-02-08 12:00:06.813000

"""

# revision identifiers, used by Alembic.
revision = 'w0015'
down_revision = 'w0014'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    from lib.models.card import Card
    from lib.models.user import User

    table = Card.__table__
    sql = 'UPDATE "{}" SET silver_points=30000, gold_points=30000 WHERE silver_points < 0 OR  gold_points < 0;'.format(table.name)
    op.get_bind().execute(text(sql))

    table = User.__table__
    sql = 'UPDATE "{}" SET silver_points=30000, gold_points=30000 WHERE silver_points < 0 OR  gold_points < 0;'.format(table.name)
    op.get_bind().execute(text(sql))


def downgrade():
    pass
