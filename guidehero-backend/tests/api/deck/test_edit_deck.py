import json
from ..base import ApiBaseTestCase
from tests.helpers import factories

from lib.models.card import Card


class EditDeckTestCase(ApiBaseTestCase):
    def test_edit_deck(self):
        deck = factories.DeckFactory(name="test_deck", creator=self.user)
        self.db.session.add(deck)
        self.db.session.commit()

        data = {
            'deck_id': deck.id,
            'card_ids': [],
            'tags': ['tag1', 'tag2']
        }
        response = self.client.post('/api/v1/deck/edit_deck', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.get(deck.id)

        self.assertEqual(deck.name, 'test_deck')
        self.assertEqual(len(deck.tags), 2)
        self.assertEqual([tag.name for tag in deck.tags], ['tag1', 'tag2'])
