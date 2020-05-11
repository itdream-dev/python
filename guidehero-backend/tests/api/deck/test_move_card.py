from ..base import ApiBaseTestCase
from tests.helpers import factories
from lib.models.card import Card


class MoveCardTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(MoveCardTestCase, self).__init__(*args, **kwargs)
        factories.JsonResponseWithResultStatusFactory.register_assert(self)
        factories.CardFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/move_card',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        expected_response = factories.JsonResponseWithResultStatusFactory.build(data={'result': 'success'})

        self.assertEqual(response, expected_response)

        return response

    def test_move_detached_card_to_deck(self):
        card = factories.ImageCardFactory(id="card_id", creator=self.user)
        deck = factories.DeckFactory(id="deck_id", creator=self.user)
        self.db.session.commit()
        result = self.call_target(
            card_ids=[card.id],
            move_to=deck.id
        )

        self.assertEqual(len(deck.cards), 1)
        self.assertEqual(deck.cards[0].id, "card_id")
        card = factories.CardFactory.get("card_id")
        self.assertEqual(card.parent.id, deck.id)

        self.assertEqual(
            card,
            factories.CardFactory.build(position=0, parent_id=deck.id)
        )

    def test_move_card_out_of_deck(self):
        deck = factories.DeckFactory(id="deck_id", creator=self.user)
        card = factories.ImageCardFactory(id="card_id", creator=self.user, parent=deck)
        self.db.session.commit()

        self.call_target(
            card_ids=[card.id]
        )

        self.assertEqual(len(deck.cards), 0)

        self.assertEqual(
            factories.CardFactory.get("card_id"),
            factories.CardFactory.build(parent=None)
        )

    def test_move_card_out_of_deck_and_convert_deck_to_card(self):
        '''
        When after reemove card from deck, the deck has only one children, then we need co convert deck to card

        Was:

        deck
            children
                card1
                card2

        action:
        move card1 out of deck

        Result:
        card1
        card2
        '''

        deck = factories.DeckFactory(id="deck", creator=self.user, position=1)
        card1 = factories.ImageCardFactory(id="card1", creator=self.user, parent=deck)
        card1 = factories.ImageCardFactory(id="card2", creator=self.user, parent=deck)
        self.db.session.commit()

        self.call_target(
            card_ids=[card1.id]
        )

        deck = factories.CardFactory.get(deck.id)
        self.assertIsNone(deck)
        card1 = factories.CardFactory.get("card1")
        card2 = factories.CardFactory.get("card2")

        self.assertIsNone(card1.parent)
        self.assertIsNone(card2.parent)
        self.assertEqual(card2.position, 1) # keep position of deck 

    def test_move_card_from_one_deck_to_another(self):
        deck1 = factories.DeckFactory(id="deck1_id", creator=self.user)
        deck2 = factories.DeckFactory(id="deck2_id", creator=self.user)
        card = factories.ImageCardFactory(id="card_id", creator=self.user, parent=deck1)
        card1 = factories.ImageCardFactory(id="card0_id", creator=self.user, parent=deck1)
        self.db.session.commit()

        self.assertEqual(card1.position, 1)
        self.assertEqual(card.position, 0)

        self.call_target(
            card_ids=[card.id],
            move_to=deck2.id
        )

        deck1 = factories.CardFactory.get('deck1_id')
        deck2 = factories.CardFactory.get('deck2_id')
        card = factories.CardFactory.get('card_id')
        card1 = factories.CardFactory.get('card0_id')
        self.assertEqual(len(deck1.cards), 1)
        self.assertEqual(deck1.cards[0].id, "card0_id")
        self.assertEqual(deck1.cards[0].position, 0)

        self.assertEqual(len(deck2.cards), 1)
        self.assertEqual(deck2.cards[0].id, "card_id")
        self.assertEqual(deck2.cards[0].position, 0)

    def test_move_card_to_another_card(self):
        ''' If destination is card, we need to create new deck, append destination card as first and source card second.'''
        cardA = factories.ImageCardFactory(id="card_id", creator=self.user)
        cardB = factories.ImageCardFactory(id="card0_id", creator=self.user)
        self.db.session.commit()

        self.call_target(
            card_ids=[cardA.id],
            move_to=cardB.id
        )

        cardA = factories.CardFactory.get(cardA.id)
        self.assertEqual(cardA.position, 1)
        deck = cardA.parent
        self.assertEqual(deck.type, Card.DECK)
        self.assertEqual(len(deck.cards), 2)
        cardB = factories.CardFactory.get(cardB.id)
        self.assertEqual(cardB.position, 0)
        self.assertEqual(cardB.parent.id, cardA.parent.id)
