import mock
from lib.registry import get_registry
from ..base import ApiBaseTestCase
from tests.helpers import factories


class SignUpTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(SignUpTestCase, self).__init__(*args, **kwargs)
        factories.Comment.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def call_target(self, **request_data):
        input_obj = factories.ApiRequestEnvironmentFactory(
            path='/api/v1/auth/signup',
            data=dict(**request_data)
        )
        response = self.client.open(**input_obj)
        return response

    def setUp(self):
        super(SignUpTestCase, self).setUp()
        self.code_patcher = mock.patch('lib.repo.user_repo.generate_verification_code')
        self.code_mock = self.code_patcher.start()

        self.registry = get_registry()
        self.original_mail = self.registry['MAIL']
        self.mail_mock = mock.Mock()
        self.registry['MAIL'] = self.mail_mock

        self.code_mock.return_value = "abscdef"

    def tearDown(self):
        super(SignUpTestCase, self).tearDown()
        self.code_patcher.stop()
        self.registry['MAIL'] = self.original_mail 

    def test_succcess(self):

        self.code_mock.return_value = "1234567"
        result = self.call_target(
            username="username",
            email="test@example.com"
        )
        self.assertEqual(result, factories.JsonResponseFactory.build(
            data={
                'verification_code': '1234567'
            }
        ))

        user = factories.UserFactory.get(email="test@example.com")
        self.assertEqual(user.username, "username")
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.verification_code, "1234567")

        self.mail_mock.send.assert_called_once()
        message = self.mail_mock.send.call_args[0][0]
        self.assertEqual(message.recipients[0], 'test@example.com')

    def test_email_exists_exception(self):
        factories.UserFactory(email='test@example.com')
        self.db.session.commit()

        result = self.call_target(
            username="username",
            email="test@example.com"
        )
        self.assertEqual(result, factories.JsonResponseFactory.build(
            data={
                'error': 'email_exists'
            }
        ))

    def test_username_exists_exception(self):
        factories.UserFactory(username='testuser')
        self.db.session.commit()

        result = self.call_target(
            username="testuser",
            email="test@example.com"
        )
        self.assertEqual(result, factories.JsonResponseFactory.build(
            data={
                'error': 'username_exists'
            }
        ))

    def test_school_does_not_exist_exception(self):
        result = self.call_target(
            username="username",
            email="test@noschool.edu"
        )
        self.assertEqual(result, factories.JsonResponseFactory.build(
            data={
                'error': 'no_school'
            }
        ))
