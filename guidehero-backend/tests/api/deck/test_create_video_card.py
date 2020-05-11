import json
from ..base import ApiBaseTestCase

from lib.models.card import Card


class CreateVideoCardTestCase(ApiBaseTestCase):
    def test_create(self):
        data = {
            'card_title': 'test_card1',
            'tags': ['tag1', 'tag2'],
            's3_file_name': 'S3_FILE_NAME',
            'scale': 3,
            'video_length': 45
        }
        response = self.client.post('/api/v1/deck/create_video_card', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.filter(Card.name == 'test_card1')[0]

        self.assertEqual(deck.name, 'test_card1')
        self.assertEqual(deck.type, Card.VIDEO)
        self.assertEqual(len(deck.tags), 2)
        self.assertEqual([tag.name for tag in deck.tags], ['tag1', 'tag2'])
        self.assertEqual(deck.scale, 3)
        self.assertEqual(deck.video_length, 45)
