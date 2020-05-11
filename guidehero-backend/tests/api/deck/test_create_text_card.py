import json
from ..base import ApiBaseTestCase

from lib.models.card import Card


class CreateTextCardTestCase(ApiBaseTestCase):
    def test_create(self):
        data = {
            'card_title': 'test_card1',
            'tags': ['Tag1', 'tag2']
        }
        response = self.client.post('/api/v1/deck/create_text_card', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.filter(Card.name == 'test_card1')[0]

        self.assertEqual(deck.name, 'test_card1')
        self.assertEqual(len(deck.tags), 2)
        self.assertEqual([tag.name for tag in deck.tags], ['tag1', 'tag2'])
