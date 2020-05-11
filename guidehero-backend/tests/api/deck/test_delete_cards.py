import flask

from lib.models.card import Card

from tests.api.base import ApiBaseTestCase
from tests.helpers import factories


class DeleteCardsTestCase(ApiBaseTestCase):
    def test_delete_card_with_reference_to_user_role_card(self):
        user_role_card = factories.UserRoleCard(card=factories.CardFactory(creator=self.user))
        self.db.session.commit()
        card = user_role_card.card
        data = {
            'card_ids': [card.id]
        }
        response = self.client.post('/api/v1/deck/delete_cards', data=flask.json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        card = Card.query.get(card.id)
        self.assertIsNone(card)
