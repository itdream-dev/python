"""card_role_permission

Revision ID: 5c07ffa6a09b
Revises: 9cbfa7c72c88
Create Date: 2016-11-17 13:13:44.591000

"""

# revision identifiers, used by Alembic.
revision = '5c07ffa6a09b'
down_revision = '9cbfa7c72c88'

from alembic import op
import sqlalchemy as sa


def upgrade():
    card_permission_tbl = op.create_table(
        'card_permission',
        sa.Column('id', sa.String(length=255), primary_key=True)
    )
    card_role_tbl = op.create_table(
        'card_role',
        sa.Column('id', sa.String(length=255), primary_key=True)
    )

    card_role_permission_tbl = op.create_table(
        'card_role_permission',
        sa.Column('role_id', sa.String(length=255), sa.ForeignKey('card_role.id'), primary_key=True),
        sa.Column('permission_id', sa.String(length=255), sa.ForeignKey('card_permission.id'), primary_key=True)
    )

    op.create_table(
        'user_role_card',
        sa.Column('user_id', sa.String(255), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('role_id', sa.String(255), sa.ForeignKey('card_role.id'), nullable=False),
        sa.Column('card_id', sa.String(255), sa.ForeignKey('card.id'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'role_id', 'card_id')
    )

    insert_initial_data(card_permission_tbl, card_role_tbl, card_role_permission_tbl)


def insert_initial_data(card_permission_tbl, card_role_tbl, card_role_permission_tbl):
    permissions = ('view', 'add_card', 'edit', 'delete', 'join_to_ask', 'view_children')
    roles = (
        ('owner', permissions),
        ('joined', ('view', 'view_children')),
        ('asked', ('view', 'view_children', 'add_card')),
        ('join_candidate', ('join_to_ask',)),
        ('viewer', ('view',)),
    )

    op.bulk_insert(
        card_permission_tbl,
        [{'id': p} for p in permissions]
    )

    op.bulk_insert(
        card_role_tbl,
        [{'id': r[0]} for r in roles]
    )
    op.bulk_insert(
        card_role_permission_tbl,
        [{'role_id': r[0], 'permission_id': p} for p in r[1] for r in roles]
    )


def downgrade():
    op.drop_table('user_role_card')
    op.drop_table('card_role_permission')
    op.drop_table('card_role')
    op.drop_table('card_permission')
