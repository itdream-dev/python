from lib.registry import get_registry


class NotificationManager(object):

    def __init__(self):
        registry = get_registry()
        self.notification_repo = registry['NOTIFICATION_REPO']

    def get_notifications(self, user):
        return self.notification_repo.get_notifications_for_user(user)

    def opened_notification(self, user):
        return self.notification_repo.opened_notification(user)
