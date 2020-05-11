import unittest
from tests.app_base_testcase import AppBaseTestCase

from lib.models.user import User
from lib.models.card import Card
from lib.models import card
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole


@unittest.skip('Change plans')
class GetASkedUsersTestCase(AppBaseTestCase):
    def test_anyone(self):
        deck = Card(type=Card.DECK, name='DEck Test')
        self.db.session.add(deck)
        self.db.session.commit()

        urc = UserRoleCard(user_id=User.ANYONE_ID, role_id=CardRole.ASKED, card_id=deck.id)
        self.db.session.add(urc)

        self.db.session.commit()

        users = card.get_asked_users(deck)
        self.assertEqual(
            users,
            [
                {
                    'user_id': None,
                    'username': 'Anyone'
                }
            ]
        )
