import unittest
import json
from ..base import ApiBaseTestCase

from lib.models.card import Card
from lib.models.user import User
from lib.models.user_role_card import UserRoleCard
from lib.models.card_role import CardRole


@unittest.skip('set_askers endpoint is obsolete')
class SetAskersTestCase(ApiBaseTestCase):
    def setUp(self):
        super(SetAskersTestCase, self).setUp()

        # input data
        self.owner = User(username='owner')
        self.db.session.add(self.owner)
        self.deck = Card(type=Card.DECK, name='test_deck', creator=self.owner, is_ask_mode_enabled=True)
        self.db.session.add(self.deck)
        self.asker = User(username='asker')
        self.db.session.add(self.asker)
        self.db.session.commit()
        self.asker_ids = None

    def call_target(self):
        asker_ids = self.asker_ids
        if asker_ids is None:
            asker_ids = [self.asker.id]
        data = {
            'deck_id': self.deck.id,
            'user_ids': asker_ids,
        }

        response = self.client.post('/api/v1/deck/set_askers', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        return response

    def assert_askers(self, asker_ids):
        urc_s = list(UserRoleCard.query.filter(UserRoleCard.card_id == self.deck.id, UserRoleCard.role_id == CardRole.JOINED).all())
        self.assertEqual(len(urc_s), len(asker_ids))
        urc_s = sorted(urc_s, key=lambda it: it.user_id)
        asker_ids = sorted(asker_ids)
        for idx in range(0, len(asker_ids)):
            self.assertEqual(urc_s[idx].user_id, asker_ids[idx])

    def test_success(self):
        self.call_target()
        self.assert_askers([self.asker.id])
