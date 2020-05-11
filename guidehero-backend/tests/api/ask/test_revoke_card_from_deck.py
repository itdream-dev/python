import json
from ..base import ApiBaseTestCase

from lib.models.card import Card
from lib.models import card as card_module
from tests.helpers import factories


class RevokeCardFromDeckTestCase(ApiBaseTestCase):
    def test_success(self):
        deck = factories.DeckFactory(
            name='test_deck',
            is_ask_mode_enabled=True,
            evaluation_period_status=card_module.EVALUATION_PERIOD_STATUS_OPEN
        )
        self.db.session.add(deck)
        question = factories.CardFactory(name='question')
        self.db.session.add(question)
        deck.cards.append(question)

        answer1 = factories.CardFactory(name='answer1')
        self.db.session.add(answer1)
        deck.cards.append(answer1)

        answer2 = factories.CardFactory(name='answer2')
        self.db.session.add(answer2)
        deck.cards.append(answer2)

        self.db.session.commit()

        data = {
            'card_id': answer1.id
        }

        response = self.client.post('/api/v1/deck/revoke_card_from_deck', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.get(deck.id)
        self.assertEqual(len(deck.cards), 2)
        self.assertEqual(deck.cards[0].id, question.id)
        self.assertEqual(deck.cards[1].id, answer2.id)

    def test_revoke_submission(self):
        deck = factories.DeckFactory(
            name='test_deck',
            is_ask_mode_enabled=True,
            evaluation_period_status=card_module.EVALUATION_PERIOD_STATUS_OPEN
        )
        header_deck = factories.DeckFactory(name='header_deck', parent=deck)
        question = factories.CardFactory(name='question', parent=header_deck)
        answer1 = factories.CardFactory(name='answer1', parent=deck)
        self.db.session.commit()

        data = {
            'card_id': answer1.id
        }

        response = self.client.post('/api/v1/deck/revoke_card_from_deck', data=json.dumps(data), follow_redirects=True, content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        deck = Card.query.get(deck.id)
        self.assertEqual(len(deck.cards), 1)
        self.assertEqual(deck.cards[0].id, header_deck.id)

        header_deck = Card.query.get(header_deck.id)
        self.assertEqual(len(header_deck.cards), 1)
        self.assertEqual(header_deck.cards[0].id, question.id)
