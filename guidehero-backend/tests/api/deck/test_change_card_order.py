from ..base import ApiBaseTestCase
from tests.helpers import factories


class ChangeCardOrderTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(ChangeCardOrderTestCase, self).__init__(*args, **kwargs)
        factories.JsonResponseWithResultStatusFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/change_order',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        deck = factories.DeckFactory(creator=self.user)
        card1 = factories.CardFactory(parent=deck)
        card2 = factories.CardFactory(parent=deck)
        card3 = factories.CardFactory(parent=deck)
        self.db.session.commit()

        self.assertEqual(card1.position, 0)
        self.assertEqual(card2.position, 1)
        self.assertEqual(card3.position, 2)

        result = self.call_target(
            card_id=card1.id,
            position=1
        )
        self.assertEqual(result, factories.JsonResponseWithResultStatusFactory.build())

        card1 = factories.CardFactory.get(card1.id)
        self.assertEqual(card1.position, 1)
        self.assertEqual(card2.position, 0)
        self.assertEqual(card3.position, 2)

    def test_card_should_not_published(self):
        deck = factories.DeckFactory(published=True, creator=self.user)
        card1 = factories.CardFactory(parent=deck)
        card2 = factories.CardFactory(parent=deck)
        self.db.session.commit()

        self.assertEqual(card1.position, 0)
        self.assertEqual(card2.position, 1)

        result = self.call_target(
            card_id=card1.id,
            position=1
        )
        self.assertEqual(
            result,
            factories.JsonResponseWithResultStatusFactory.build(
                data={
                    'result': 'error',
                    'message': u'Card deck is published. you can not change order'
                }
            )
        )

    def test_change_order_for_drafts(self):
        card1 = factories.CardFactory(creator=self.user, position=0)
        card2 = factories.CardFactory(creator=self.user, position=1)
        card3 = factories.CardFactory(creator=self.user, position=2)
        self.db.session.commit()

        self.assertEqual(card1.position, 0)
        self.assertEqual(card2.position, 1)
        self.assertEqual(card3.position, 2)

        result = self.call_target(
            card_id=card1.id,
            position=1
        )
        self.assertEqual(result, factories.JsonResponseWithResultStatusFactory.build())

        card1 = factories.CardFactory.get(card1.id)
        card2 = factories.CardFactory.get(card2.id)
        card3 = factories.CardFactory.get(card3.id)
        self.assertEqual(card1.position, 1)
        self.assertEqual(card2.position, 0)
        self.assertEqual(card3.position, 2)
