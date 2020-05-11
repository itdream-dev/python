import json
from ..base import ApiBaseTestCase

from lib.models.card import Card


class DeckTestCase(ApiBaseTestCase):
    def test_create(self):
        data = {
            'deck_title': 'test_deck',
            'card_ids': [],
            'is_ask_mode_enabled': True,
            'format': 'test format',
            'tags': ['tag1', 'tag2']
        }
        response = self.client.post('/api/v1/deck/create_deck', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.filter(Card.name == 'test_deck')[0]

        self.assertEqual(deck.name, 'test_deck')
        self.assertEqual(deck.is_ask_mode_enabled, True)
        self.assertEqual(deck.format, 'test format')
        self.assertEqual(len(deck.tags), 2)
        self.assertEqual([tag.name for tag in deck.tags], ['tag1', 'tag2'])
