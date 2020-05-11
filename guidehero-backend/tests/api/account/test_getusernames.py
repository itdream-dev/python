import json
from ..base import ApiBaseTestCase

from lib.models.user import User


class GetUserNamesTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(GetUserNamesTestCase, self).__init__(*args, **kwargs)
        self.url = '/api/v1/account/get_usernames'

    def test_success(self):
        user = User(username='first_name user1', password='12345', active=True)
        self.db.session.add(user)
        self.db.session.commit()

        data = {'search_key': 'user1'}

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        usernames = json.loads(response.data)['users']
        self.assertEqual(usernames, [{'user_id': user.id, 'username': 'first_name user1'}])
