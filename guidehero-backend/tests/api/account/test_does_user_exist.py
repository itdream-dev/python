from ..base import ApiBaseTestCase
from tests.helpers import factories


class DoesUserExistTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(DoesUserExistTestCase, self).__init__(*args, **kwargs)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/account/does_user_exist',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def test_user_exists(self):
        user = factories.UserFactory(username="test")

        result = self.call_target(
            username="test"
        )
        self.assertEqual(
            result,
            factories.JsonResponseFactory.build(
                data={'result': True}
            )
        )

    def test_user_does_exist(self):
        result = self.call_target(
            username="test"
        )
        self.assertEqual(
            result,
            factories.JsonResponseFactory.build(
                data={'result': False}
            )
        )
