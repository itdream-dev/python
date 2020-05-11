from ..base import ApiBaseTestCase
from tests.helpers import factories
from lib.models.card import Card


class ConvertCardToDeckTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(ConvertCardToDeckTestCase, self).__init__(*args, **kwargs)
        factories.CardFactory.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/convert_card_to_deck',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        card_id = 'card_id'
        card_name = 'card_name'
        card = factories.CardFactory(id=card_id, name='card_name', creator=self.user, description='description')
        tag = factories.Tag(name="tag1")
        card.tags.append(tag)
        self.db.session.commit()

        result = self.call_target(
            card_id=card_id
        )
        self.assertEqual(result.status, '200 OK')

        card = factories.CardFactory.get(card_id)
        deck = card.parent

        self.assertEqual(
            result,
            factories.JsonResponseFactory.build(
                data=deck.to_dict()
            )
        )

        self.assertEqual(deck.type, Card.DECK)
        self.assertEqual(deck.name, card_name)
        self.assertEqual(deck.description, 'description')
        self.assertEqual(len(deck.tags), 1)
        self.assertEqual(deck.tags[0].name, 'tag1')
