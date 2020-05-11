from lib.models.user import User
from ..base import ApiBaseTestCase
from lib.models import card_role
from tests.helpers import factories
from app.api.auth_api import get_base_user_info
import flask


class EditUserTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(EditUserTestCase, self).__init__(*args, **kwargs)
        factories.UserFactory.register_assert(self)
        factories.JsonResponseFactory.register_assert(self)

    def setUp(self):
        super(EditUserTestCase, self).setUp()
        self.data = {}

    def call_target(self):
        response = self.client.post('/api/v1/auth/edit_user', data=flask.json.dumps(self.data), content_type='application/json')
        return response

    def test_basic_info(self):
        user = factories.UserFactory(
            id='TestUser',
            username='test',
            first_name='first_name',
            last_name='last_name',
            bio='bio'
        )
        self.db.session.add(user)
        self.db.session.commit()
        self.set_current_user(user)
        self.user = user
        self.data = dict(
            username='test1',
            first_name='first_name1',
            last_name='last_name1',
            bio='bio1'
        )

        response = self.call_target()

        expected_user = factories.UserFactory.build(
            id='TestUser',
            username='test1',
            first_name='first_name1',
            last_name='last_name1',
            bio='bio1'
        )

        self.assertEqual(
            factories.UserFactory.get('TestUser'),
            expected_user
        )

        self.assertEqual(
            response,
            factories.JsonResponseFactory(
                data=get_base_user_info(expected_user)
            )
        )
