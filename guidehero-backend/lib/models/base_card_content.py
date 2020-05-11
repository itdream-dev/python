# -*- coding: utf-8 -*-
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


class BaseCardContent(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255))
    content = db.Column(db.String(255))
    language = db.Column(db.String(255))
    card_id = db.Column(db.Integer, db.ForeignKey('base_card.id'))

    def to_dict(self):
        as_dict = {
            'type': self.type,
            'content': self.content,
        }
        if self.type == 'audio':
            as_dict['language'] = self.language
        return as_dict
