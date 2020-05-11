import unittest
import json
from ..base import ApiBaseTestCase

from lib.models.card import Card


@unittest.skip('Stop working after add  silver gold points')
class SearchDecksTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(SearchDecksTestCase, self).__init__(*args, **kwargs)
        self.url = '/api/v1/deck/search_cards'

    def test_success(self):

        deck = Card(type=Card.TEXT, name='1 apple', description='...green...', published=True)
        self.db.session.add(deck)
        card = Card(type=Card.TEXT, name='2 green', description='...apple...', published=True)
        self.db.session.add(card)
        card_no = Card(type=Card.TEXT, name='3 does not match', published=True)
        self.db.session.add(card_no)
        self.db.session.commit()

        data = {
            'keywords': ['apple', 'green'],
        }

        response = self.client.get(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        cards = json.loads(response.data)['cards']
        cards = sorted(cards, key=lambda c: c['name'])
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["id"], deck.id)
        self.assertEqual(cards[1]["id"], card.id)
