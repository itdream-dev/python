from ..base import ApiBaseTestCase
from tests.helpers import factories


class VerifyEmailTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(VerifyEmailTestCase, self).__init__(*args, **kwargs)
        factories.Comment.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/auth/verify_email',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def setUp(self):
        super(VerifyEmailTestCase, self).setUp()

    def tearDown(self):
        super(VerifyEmailTestCase, self).tearDown()

    def test_succcess(self):
        user = factories.UserFactory(email='test@example.com', verification_code='12345', active=False)
        self.db.session.commit()

        result = self.call_target(
            email="test@example.com",
            code='12345'
        )

        self.assertEqual(result, factories.JsonResponseFactory.build())

        user = factories.UserFactory.get(email="test@example.com")

        self.assertEqual(user.active, True)
        self.assertEqual(user.verification_code, '')
