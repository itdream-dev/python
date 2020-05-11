# -*- coding: utf-8 -*-
import arrow
from lib.registry import get_registry
from lib.models.notification import Notification


class NotificationRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def create_like_notification(self, liked_user, card):
        now = arrow.utcnow().timestamp
        notification = Notification(
            user_id=card.user_id,
            extra_user_id=liked_user.id,
            card_id=card.id,
            content='{username} liked your post: "%s"' % card.name,
            created_at=now
        )
        self.db.session.add(notification)
        self.db.session.commit()

    def create_comment_notification(self, commented_user, card, comment):
        now = arrow.utcnow().timestamp
        notification = Notification(
            user_id=card.user_id,
            extra_user_id=commented_user.id,
            card_id=card.id,
            content='{username} commented on your post: "%s"' % comment,
            created_at=now
        )
        self.db.session.add(notification)
        self.db.session.commit()

    def get_notifications_for_user(self, user):
        notifications = Notification.query.filter(
            Notification.user_id == user.id
        ).all()
        return notifications

    def create_mention_notification(self, user, commented_user, card, comment):
        now = arrow.utcnow().timestamp
        notification = Notification(
            user_id=user.id,
            extra_user_id=commented_user.id,
            card_id=card.id,
            content='{username} mentioned you in a comment: "%s"' % comment,
            created_at=now
        )
        self.db.session.add(notification)
        self.db.session.commit()

    def opened_notification(self, user):
        Notification.query.filter(
            Notification.user_id == user.id,
            Notification.opened == False
        ).update({'opened': True})
