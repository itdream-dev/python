import mock
import json
from lib.models.user import User
from ..base import ApiBaseTestCase


class GoogleSigninTestCase(ApiBaseTestCase):
    def test_signin_success(self):
        self.user = User(username='test', email='test@test.com', password='12345', silver_points=41)
        self.db.session.add(self.user)
        self.db.session.commit()

        with mock.patch('app.managers.account_manager.get_google_verification_data') as m:
            m.return_value = {
                'verified': True,
                'email': 'test@test.com'
            }
            data = {
                'google_access_token': 'my_goolge_token'
            }
            response = self.client.post('/api/v1/auth/google_signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')

        data = json.loads(response.data)
        self.assertEqual(data['user']['id'], self.user.id)
        self.assertEqual(data['user']['total_silver_points'], 41)
        self.assertEqual(data['auth_token'], self.user.get_auth_token())

    def test_signup_success(self):
        with mock.patch('app.managers.account_manager.get_google_verification_data') as m:
            m.return_value = {
                'verified': True,
                'email': 'test@test.com'
            }
            data = {
                'google_access_token': 'my_goolge_token'
            }
            response = self.client.post('/api/v1/auth/google_signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')

        self.user = User.query.filter(User.email == 'test@test.com').first()
        data = json.loads(response.data)
        self.assertEqual(data['user']['id'], self.user.id)
        self.assertEqual(data['user']['total_silver_points'], 1000)
        self.assertEqual(data['auth_token'], self.user.get_auth_token())
