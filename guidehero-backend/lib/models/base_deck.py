# -*- coding: utf-8 -*-
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


class BaseDeck(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    content = db.relationship('BaseSet')
    folder_id = db.Column(db.Integer, db.ForeignKey('base_folder.id'))
    creator = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def to_dict(self):
        return {
            'name': self.name,
            'type': 'deck',
            'creator': self.creator,
            'image': self.image,
            'content': [base_set.to_dict() for base_set in self.content]
        }
