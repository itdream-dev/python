from ..base import ApiBaseTestCase

from lib.models.card import Card
from tests.helpers import factories


class DeskAddModeTestCase(ApiBaseTestCase):

    def test_create_ask_from_single_card(self):
        card = factories.CardFactory(name="card_name")
        self.db.session.commit()

        self.call_target(
            data=dict(
                deck_id=card.id,
                is_ask_mode_enabled=True
            )
        )
        # TO DO check response
        card = factories.CardFactory.get(card.id)
        self.assertEqual(card.type, Card.TEXT)
        self.assertEqual(card.is_ask_mode_enabled, False)
        self.assertEqual(card.name, "card_name")

        container = card.parent

        self.assertEqual(container.type, Card.DECK)
        self.assertEqual(container.name, "card_name")
        self.assertEqual(container.is_ask_mode_enabled, False)

        ask_mode_deck = container.parent

        self.assertEqual(ask_mode_deck.type, Card.DECK)
        self.assertEqual(ask_mode_deck.is_ask_mode_enabled, True)

    def test_enable_ask_mode_for_deck(self):
        deck = factories.DeckFactory(name="deck_name")
        card = factories.CardFactory(parent=deck, name="card_name")
        self.call_target(
            data=dict(
                deck_id=deck.id,
                is_ask_mode_enabled=True
            )
        )

        # TO DO check response
        card = factories.CardFactory.get(card.id)
        self.assertEqual(card.type, Card.TEXT)
        self.assertEqual(card.is_ask_mode_enabled, False)
        self.assertEqual(card.name, "card_name")

        container = card.parent

        self.assertEqual(container.type, Card.DECK)
        self.assertEqual(container.name, "deck_name")
        self.assertEqual(container.is_ask_mode_enabled, False)

        ask_mode_deck = container.parent

        self.assertEqual(ask_mode_deck.type, Card.DECK)
        self.assertEqual(ask_mode_deck.name, "deck_name")
        self.assertEqual(ask_mode_deck.is_ask_mode_enabled, True)

    def call_target(self, data=None):
        input_data = factories.ApiRequestEnvironmentFactory(
            data=data,
            path='/api/v1/deck/add_mode'
        )
        response = self.client.open(**input_data)
        return response
