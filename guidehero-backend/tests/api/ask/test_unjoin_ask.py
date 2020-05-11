import json
from ..base import ApiBaseTestCase

from lib.models.card import Card
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole


class UnJoinAskTestCase(ApiBaseTestCase):
    def setUp(self):
        super(UnJoinAskTestCase, self).setUp()

        # input data
        self.deck_silver_points = 100
        self.deck = None
        self.join_user = None

    def call_target(self):
        self.owner = User(username='owner')
        self.db.session.add(self.owner)
        self.deck = Card(type=Card.DECK, name='test_deck', creator=self.owner, is_ask_mode_enabled=True, silver_points=self.deck_silver_points, prize_to_join=10)
        self.db.session.add(self.deck)
        self.db.session.commit()

        self.join_user = self.user
        ucr = UserRoleCard(user_id=self.join_user.id, role_id=CardRole.JOINED, card_id=self.deck.id)
        self.db.session.add(ucr)
        self.db.session.commit()

        data = {
            'deck_id': self.deck.id
        }

        response = self.client.post('/api/v1/deck/unjoin_ask', data=json.dumps(data), content_type='application/json')
        self.response = response
        return response

    def assert_result(self):
        self.assert_deck_silver_points()
        self.assert_askers([])
        self.assert_response()

    def assert_response(self):
        self.assertEqual(self.response.status, '200 OK')
        data = json.loads(self.response.data)
        self.assertEqual(data['result'], 'success')
        deck_data = data['deck']
        self.assertEqual(deck_data['id'], self.deck.id)

    def assert_deck_silver_points(self):
        self.assertEqual(self.deck.silver_points, self.deck_silver_points)

    def assert_askers(self, asker_ids):
        urc_s = list(UserRoleCard.query.filter(UserRoleCard.card_id == self.deck.id, UserRoleCard.role_id == CardRole.JOINED).all())
        self.assertEqual(len(urc_s), len(asker_ids))
        urc_s = sorted(urc_s, key=lambda it: it.user_id)
        asker_ids = sorted(asker_ids)
        for idx in range(0, len(asker_ids)):
            self.assertEqual(urc_s[idx].user_id, asker_ids[idx])

    def test_success(self):
        self.deck_silver_points = 50
        self.call_target()
        self.assert_result()
