from ..base import ApiBaseTestCase
from tests.helpers import factories


class ViewCardTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(ViewCardTestCase, self).__init__(*args, **kwargs)
        factories.CardFactory.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/view_card',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        card = factories.CardFactory(id="card")
        self.db.session.commit()
        result = self.call_target(
            card_id="card"
        )
        self.assertEqual(result, factories.JsonResponseFactory.build())

        card = factories.CardFactory.get("card")
        self.assertEqual(card.views_count, 1)
        self.assertEqual(len(card.views), 1)
        self.assertEqual(card.views[0].id, self.user.id)
