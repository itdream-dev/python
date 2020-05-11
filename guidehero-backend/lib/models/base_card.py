# -*- coding: utf-8 -*-
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


class BaseCard(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.relationship('BaseCardContent')
    set_id = db.Column(db.Integer, db.ForeignKey('base_set.id'))
    name = db.Column(db.String(255))
    public = db.Column(db.Boolean(),
                       default=False,
                       server_default='false',
                       nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

    creator = db.relationship('User')

    def to_dict(self):
        return {
            'name': self.name,
            'type': 'card',
            'creator': self.creator.name if self.creator else 'Chris Yamamoto',
            'content': [content.to_dict() for content in self.content]
        }
