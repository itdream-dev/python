# -*- coding: utf-8 -*-
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


class BaseSet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.relationship('BaseCard')
    name = db.Column(db.String(255))
    deck_id = db.Column(db.Integer, db.ForeignKey('base_deck.id'))
    creator = db.Column(db.String(255))

    def to_dict(self):
        return {
            'name': self.name,
            'type': 'set',
            'creator': self.creator,
            'content': [card.to_dict() for card in self.content]
        }
