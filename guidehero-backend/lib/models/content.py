# -*- coding: utf-8 -*-
import uuid
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


def uuid_gen():
    return str(uuid.uuid4())


class Card(db.Model):

    TEXT = 'text'
    IMAGE = 'image'
    DECK = 'deck'

    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)
    type = db.Column(db.String(255))
    name = db.Column(db.String(255))
    content = db.Column(db.String(255))
    language = db.Column(db.String(255), default='')
    pronunciation = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)

    creator = db.relationship('User')

    def to_dict(self):
        serialized = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'content': self.content,
            'creator': self.creator.name if self.creator else 'Chris Yamamoto',
        }
        if self.type == self.TEXT:
            serialized.update({
                'pronunciation': self.pronunciation,
                'language': self.language
            })
        return serialized
