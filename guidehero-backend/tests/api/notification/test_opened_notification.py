import json
from ..base import ApiBaseTestCase


class NotificationOpenedNotificationTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(NotificationOpenedNotificationTestCase, self).__init__(*args, **kwargs)
        self.url = '/api/v1/notification/opened_notification'

    def test_success(self):
        from lib.models.notification import Notification

        n = Notification(user_id=self.user.id, opened=False)
        self.db.session.add(n)
        self.db.session.commit()

        data = {}

        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status, '200 OK')
        n = Notification.query.get(n.id)
        self.assertEqual(n.opened, True)
