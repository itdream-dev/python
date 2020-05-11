import json
from ..base import ApiBaseTestCase

from lib.models.card import Card
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole
from tests.helpers import factories


class JoinAskTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(JoinAskTestCase, self).__init__(*args, **kwargs)
        factories.Transfer.register_assert(self)

    def setUp(self):
        super(JoinAskTestCase, self).setUp()
        self.user = factories.UserFactory(silver_points=100)
        self.db.session.add(self.user)
        self.set_current_user(self.user)

        # input data
        self.owner = User(username='owner')
        self.db.session.add(self.owner)
        self.deck = Card(type=Card.DECK, name='test_deck', creator=self.owner, is_ask_mode_enabled=True, silver_points=0, prize_to_join=10)
        self.db.session.add(self.deck)
        self.db.session.commit()
        self.asker_ids = None
        self.custom_join_prize = None

        self.response = None

    def call_target(self):
        data = {
            'deck_id': self.deck.id,
        }
        if self.custom_join_prize is not None:
            data['custom_join_prize'] = self.custom_join_prize

        response = self.client.post('/api/v1/deck/join_ask', data=json.dumps(data), content_type='application/json')
        self.response = response
        return response

    def assert_result(self):
        self.assert_response()

    def assert_response(self):
        self.assertEqual(self.response.status, '200 OK')

        deck = Card.query.get(self.deck.id)
        data = json.loads(self.response.data)
        self.assertEqual(data['result'], 'success')
        deck_data = data['deck']
        self.assertEqual(deck_data['id'], deck.id)

    def assert_askers(self, asker_ids):
        urc_s = list(UserRoleCard.query.filter(UserRoleCard.card_id == self.deck.id, UserRoleCard.role_id == CardRole.JOINED).all())
        self.assertEqual(len(urc_s), len(asker_ids))
        urc_s = sorted(urc_s, key=lambda it: it.user_id)
        asker_ids = sorted(asker_ids)
        for idx in range(0, len(asker_ids)):
            self.assertEqual(urc_s[idx].user_id, asker_ids[idx])

    def test_custom_prize(self):
        self.custom_join_prize = 100
        self.call_target()
        self.assertEqual(self.deck.silver_points, 100)
        self.assert_result()

    def test_success(self):
        self.call_target()
        self.assert_askers([self.user.id])
        self.assertEqual(self.deck.silver_points, 10)
        self.assertEqual(self.user.silver_points, 90)
        self.assert_result()
        tr = factories.Transfer.get()[0]
        self.assertEqual(
            tr,
            factories.Transfer.build(id=tr.id, user_from=self.user, card_to=self.deck, silver_points=10, transaction_type='join_ask')
        )
