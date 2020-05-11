import json
from ..base import ApiBaseTestCase
from tests.helpers import factories
from lib.models.card import Card


class CopyCardTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(CopyCardTestCase, self).__init__(*args, **kwargs)
        factories.CardFactory.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/copy_card',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_succcess(self):
        card_id = 'card_id'
        card = factories.CardFactory(id=card_id, name='card_name', creator=self.user)
        self.db.session.commit()
        result = self.call_target(
            card_id=card_id
        )
        self.assertEqual(result.status, '200 OK')

        data = json.loads(result.data)
        new_card_id = data['id']

        card = factories.CardFactory.get(card_id)
        new_card = factories.CardFactory.get(new_card_id)
        self.assertEqual(card.name, new_card.name)
