# -*- coding: utf-8 -*-
import uuid
from lib.registry import get_registry


db = get_registry()['DB']


def uuid_gen():
    return str(uuid.uuid4())


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    extra_user_id = db.Column(db.String, db.ForeignKey('user.id'))
    card_id = db.Column(db.String, db.ForeignKey('card.id'))
    content = db.Column(db.String(255))
    created_at = db.Column(db.Integer)
    opened = db.Column(
        db.Boolean,
        default=False,
        server_default='false',
        nullable=False
    )

    user = db.relationship('User', foreign_keys=[user_id])
    extra_user = db.relationship('User', foreign_keys=[extra_user_id])

    def to_dict(self):
        return {
            'card_id': self.card_id or '',
            'content': self.content.format(username=self.extra_user.name),
            'created_at': self.created_at,
            'thumbnail_url': self.extra_user.thumbnail_url,
            'opened': self.opened
        }
