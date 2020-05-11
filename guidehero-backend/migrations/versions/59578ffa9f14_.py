"""empty message

Revision ID: 59578ffa9f14
Revises: 3110bd82dd67
Create Date: 2016-10-26 14:39:24.243012

"""

# revision identifiers, used by Alembic.
revision = '59578ffa9f14'
down_revision = '3110bd82dd67'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'width')
    op.drop_column('card', 'y_position')
    op.drop_column('card', 'x_position')
    op.drop_column('card', 'height')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('card', sa.Column('x_position', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('card', sa.Column('y_position', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('card', sa.Column('width', sa.INTEGER(), autoincrement=False, nullable=True))
    ### end Alembic commands ###