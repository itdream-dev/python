import unittest
from tests.app_base_testcase import AppBaseTestCase

from lib.models.user import User
from lib.models.card import Card
from lib.models.role import Role
from lib.repo.deck_repo import DeckRepo


@unittest.skip('We dont need it (for history')
class GetViewableDecksCase(AppBaseTestCase):
    def test_visible(self):
        from lib.models.user_permission import UserPermission
        user = User(username='test_user1', password='12345', active=True)
        role = Role(name='homes')
        user.roles.append(role)
        self.db.session.add(user)
        self.db.session.commit()

        deck_visible = Card(type=Card.DECK, name='1 visible_deck')
        self.db.session.add(deck_visible)

        deck_owned = Card(type=Card.DECK, name='2 owned_by_user', user_id=user.id)
        self.db.session.add(deck_owned)

        deck_invisible = Card(type=Card.DECK, name='3 invisible_deck')
        self.db.session.add(deck_invisible)

        deck_visible_by_role = Card(type=Card.DECK, name='4 visible_by_role')
        self.db.session.add(deck_visible_by_role)

        self.db.session.commit()

        up1 = UserPermission(card_id=deck_visible.id, permission_id='view', user_id=user.id)
        self.db.session.add(up1)

        up2 = UserPermission(card_id=deck_visible_by_role.id, permission_id='view', role_id=role.id)
        self.db.session.add(up2)

        self.db.session.commit()

        deck_repo = DeckRepo()
        decks = list(deck_repo.get_viewable_decks(user))
        decks = sorted(decks, key=lambda d: d.name)
        self.assertEqual(len(decks), 3)
        self.assertEqual(decks[0].id, deck_visible.id)
        self.assertEqual(decks[1].id, deck_owned.id)
        self.assertEqual(decks[2].id, deck_visible_by_role.id)


class JustKeepCodeHereForHistory(object):
    def check_view_permission(self, user, q):
        from lib.models.user_permission import UserPermission
        from sqlalchemy import or_, and_
        roles_id = [r.id for r in user.roles]
        return q.outerjoin(UserPermission).\
            filter(
                or_(
                    and_(
                        Card.id == UserPermission.card_id,
                        UserPermission.permission_id == 'view',
                        or_(
                            UserPermission.user_id == user.id,
                            UserPermission.role_id.in_(roles_id)
                        )
                    ),
                    (
                        Card.user_id == user.id
                    )
                )
            )

    def get_viewable_decks(self, user):
        q = self.check_view_permission(
            user,
            Card.query.filter(
                Card.type == Card.DECK
            )
        )
        return q.all()
