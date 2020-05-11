import json
import mock
from ..base import ApiBaseTestCase

from lib.models.card import Card
from lib.models import card as card_module
from lib.models.user import User
from tests.helpers import factories

import unittest


class GiveCardToDeckTestCase(ApiBaseTestCase):

    def setUp(self):
        super(GiveCardToDeckTestCase, self).setUp()
        self.deck_creator = User(username='deck_creator')

        self.deck = Card(type=Card.DECK, name='test_deck', is_ask_mode_enabled=True, evaluation_period_status=card_module.EVALUATION_PERIOD_STATUS_OPEN, creator=self.deck_creator)
        self.db.session.add(self.deck)
        self.question_creator = User(username='question_creator')
        self.db.session.add(self.question_creator)
        self.question = Card(type=Card.TEXT, name='question', creator=self.question_creator)
        self.db.session.add(self.question)
        self.deck.cards.append(self.question)

        self.creator = User(username='giver1')
        self.answer = Card(type=Card.TEXT, name='answer', creator=self.creator)
        self.db.session.add(self.answer)

        self.db.session.commit()

    def test_success(self):
        start_struct = \
        [
            {
                'type': 'ask', 'id':  'Ask1', 'name': 'Ask_name',
                'children': [
                    {'type': 'deck', 'id': 'QUESTION-COLLECTION',
                        'children': [
                            {'id': 'Question1', 'name': 'Question1'}
                        ]
                    },
                ]
            },
            {'id': 'Submission1', 'name': 'Submission1'}
        ]

        expected_struct = \
        [
        {
            'type': 'ask', 'id':  'Ask1', 'name': 'Ask_name',
            'children': [
                {'type': 'deck', 'id': 'QUESTION-COLLECTION',
                    'children': [
                        {'id': 'Question1', 'name': 'Question1'}
                    ]
                },
                {'id': 'Submission1', 'name': 'Submission1'},
            ]
        }
        ]

        self.initialize_data(start_struct)
        self.db.session.commit()

        deck = factories.CardFactory.get("Ask1")

        data = {
            'deck_id': 'Ask1',
            'card_id': 'Submission1'
        }
        with mock.patch('lib.models.card.uuid_gen') as m:
            m.return_value = 'NEW_ID'
            response = self.client.post('/api/v1/deck/give_card_to_deck', data=json.dumps(data), content_type='application/json')

        deck = factories.CardFactory.get("Ask1")
        self.assert_data(expected_struct)

    def test_only_for_askers(self):
        data = {
            'deck_id': self.deck.id,
            'card_id': self.answer.id,
            'visibility': card_module.ANSWER_VISIBILITY_ONLY_ASKERS
        }

        response = self.client.post('/api/v1/deck/give_card_to_deck', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.get(self.deck.id)
        self.assertEqual(len(deck.cards), 2)
        self.assertEqual(deck.cards[0].id, self.question.id)
        self.assertEqual(deck.cards[1].id, self.answer.id)
        self.assertEqual(deck.cards[1].answer_visibility, card_module.ANSWER_VISIBILITY_ONLY_ASKERS)
        self.assertEqual(deck.get_givers(), [self.creator])

    def initialize_data(self, data):
        res = []
        for item in data:
            tp = item.pop('type', 'card')
            fact = {
                'card': factories.CardFactory,
                'deck': factories.DeckFactory,
                'ask': factories.AskDeckFactory
            }[tp]
            children = item.pop('children', [])
            entity = fact(**item)
            if tp == 'ask':
                entity.evaluation_period_status = 'open'
            cards = self.initialize_data(children)
            for card in cards:
                entity.cards.append(card)
            res.append(entity)
        return res

    def assert_data(self, data, cards=None):
        for i, item in enumerate(data):
            if cards is not None:
                entity = cards[i]
            else:
                entity = factories.CardFactory.get(item['id'])
            tp = item.pop('type', 'card')
            if tp == 'ask':
                self.assertEqual(entity.type, 'deck')
                self.assertEqual(entity.is_ask_mode_enabled, True)
            if tp == 'deck':
                self.assertEqual(entity.type, 'deck')
                self.assertEqual(entity.is_ask_mode_enabled, False)
            if tp == 'card':
                self.assertEqual(entity.type, 'text')
                self.assertEqual(entity.is_ask_mode_enabled, False)
            children = item.pop('children', [])
            parent_id = item.pop('parent_id', None)
            if parent_id is not None:
                self.assertEqual(entity.parent.id, parent_id)
            for key, value in item.items():
                self.assertEqual(getattr(entity, key), value)
            for idx, child in enumerate(children):
                child['parent_id'] = entity.id
                if 'id' in child:
                    self.assertEqual(
                        entity.cards[idx].id, child['id'], 
                        "Wrong entity at position={} {}, {} != {}".format(idx, entity.cards[idx].position, entity.cards[idx].id, child['id'])
                    )
            self.assert_data(children, entity.cards)

    def test_convert_card_to_deck_for_second_submission(self):
        start_struct = \
        [
            {
                'type': 'ask', 'id':  'Ask1', 'name': 'Ask_name',
                'children': [
                    {'type': 'deck', 'id': 'QUESTION-COLLECTION',
                        'children': [
                            {'id': 'Question1', 'name': 'Question1'}
                        ]
                    },
                    {'id': 'Submission1', 'name': 'Submission1'}
                ]
            },
            {'id': 'Submission2', 'name': 'Submission2'}
        ]

        expected_struct = \
        [
        {
            'type': 'ask', 'id':  'Ask1', 'name': 'Ask_name',
            'children': [
                {'type': 'deck', 'id': 'QUESTION-COLLECTION',
                    'children': [
                        {'id': 'Question1', 'name': 'Question1'}
                    ]
                },
                {'type': 'deck', 'is_answer': True,
                    'children': [
                        {'id': 'Submission1', 'name': 'Submission1'},
                        {'id': 'Submission2', 'name': 'Submission2',}
                    ]
                },
            ]
        }
        ]

        self.initialize_data(start_struct)
        self.db.session.commit()

        data = {
            'deck_id': 'Ask1',
            'card_id': 'Submission2'
        }
        with mock.patch('lib.models.card.uuid_gen') as m:
            m.return_value = 'NEW_ID'
            response = self.client.post('/api/v1/deck/give_card_to_deck', data=json.dumps(data), content_type='application/json')
        self.assert_data(expected_struct)
