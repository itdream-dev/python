import mock
from ..base import ApiBaseTestCase
from tests.helpers import factories


class FbSigninTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(FbSigninTestCase, self).__init__(*args, **kwargs)
        factories.Comment.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/auth/fb_signin',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def setUp(self):
        super(FbSigninTestCase, self).setUp()

    def tearDown(self):
        super(FbSigninTestCase, self).tearDown()

    @mock.patch('app.managers.account_manager.get_facebook_verification_data')
    def test_activate_user_if_was_inactive(self, mfb):
        user = factories.UserFactory(email='test@example.com', verification_code='', active=False, password='12345')
        self.db.session.commit()
        mfb.return_value = {
            'verified': True,
            'email': 'test@example.com',
            'thumbnail_url': 'thumbnail_url'
        }

        result = self.call_target(
            fb_access_token="fb_access_token",
        )

        self.assertEqual(result.status, '200 OK')

        user = factories.UserFactory.get(email="test@example.com")

        self.assertEqual(user.active, True)
        self.assertEqual(user.verification_code, '')
