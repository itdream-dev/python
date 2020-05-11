from ..base import ApiBaseTestCase
from tests.helpers import factories
from tests.helpers import asserts
from lib.models.card import Card


class CreateImageCardTestCase(ApiBaseTestCase):
    CARD_TITLE = 'test_card1'

    def run_case(self, input_data={}, expected_data={}):
        with self.db.session.no_autoflush:
            input_obj = self.arrange_input(**input_data)
            result = self.act(input_obj)
            expected = self.arrange_expected(**expected_data)
            self.assert_result(result, expected)
        self.db.session.rollback()

    def arrange_input(self, **input_data):
        request_data = input_data.pop('request_data', {})
        return factories.ApiRequestEnvironmentFactory(
            path='/api/v1/deck/create_image_card',
            data=dict(card_title=self.CARD_TITLE, **request_data)
        )

    def act(self, input_obj):
        response = self.client.open(**input_obj)
        return factories.NamedTupleFactory(
            card=Card.query.filter(Card.name == self.CARD_TITLE)[0],
            response=response
        )

    def arrange_expected(self, **expected_data):
        card_data = expected_data.get('card_data', {})
        return factories.NamedTupleFactory(
            card=factories.ImageCardFactory(name=self.CARD_TITLE, **card_data),
            response=factories.JsonResponseWithResultStatusFactory()
        )

    def assert_result(self, result, expected):
        asserts.assertJsonResponseWithResultStatus(result.response, expected.response)
        asserts.assertCard(result.card, expected.card)

    def test_default(self):
        self.run_case()

    def test_check_smiple_fields(self):
        self.run_case(
            input_data=dict(
                request_data=dict(tags=['tag1', 'tag2'], image_scale=3)
            ),
            expected_data=dict(
                card_data=dict(tag_names=['tag1', 'tag2'], scale=3)
            )
        )
