import json
from lib.models.user import User
from ..base import ApiBaseTestCase


class EmailSigninTestCase(ApiBaseTestCase):
    def test_signin_success(self):
        self.user = User(username='test', email='test@test.com', password='12345')
        self.db.session.add(self.user)
        self.db.session.commit()

        data = {
            'email': 'test@test.com'
        }
        response = self.client.post('/api/v1/auth/signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')

        data = json.loads(response.data)
        self.assertEqual(data['user']['id'], self.user.id)
        self.assertEqual(data['auth_token'], self.user.get_auth_token())
