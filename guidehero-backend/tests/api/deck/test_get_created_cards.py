from ..base import ApiBaseTestCase
import flask
from tests.helpers import factories


class GetCreatedCardsTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(GetCreatedCardsTestCase, self).__init__(*args, **kwargs)
        factories.Comment.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/get_created_cards',
            data=dict(**request_data),
            method='GET'
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        card = factories.CardFactory(creator=self.user)
        self.db.session.commit()
        result = self.call_target(
        )
        self.assertEqual(result.status, '200 OK')
        data = flask.json.loads(result.data)
        cards = data['created']
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0]['id'], card.id)
