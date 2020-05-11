import mock

from tests.app_base_testcase import AppBaseTestCase
from lib.models.user import User


class ApiBaseTestCase(AppBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(ApiBaseTestCase, self).__init__(*args, **kwargs)
        self.url = ''

    def setUp(self):
        super(ApiBaseTestCase, self).setUp()

        # create current user
        self.user = User(id='DefaultCurrentUser', username='test_user', password='12345', active=True)
        self.db.session.add(self.user)
        self.db.session.commit()
        self.set_current_user(self.user)

        # way around of flask_securirty.decorators.auth_token_required decarator
        self._check_token_patcher = mock.patch('flask_security.decorators._check_token', return_value=True)
        self._check_token_mock = self._check_token_patcher.start()

    def set_current_user(self, user):
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id
            sess['_fresh'] = True  # https://flask-login.readthedocs.org/en/latest/#fresh-logins

    def tearDown(self):
        super(ApiBaseTestCase, self).tearDown()
        self._check_token_patcher.stop()
