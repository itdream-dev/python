# -*- coding: utf-8 -*-
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


class BaseFolder(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    root_level = db.Column(db.Boolean, default=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('base_folder.id'))
    decks = db.relationship('BaseDeck')
    folders = db.relationship('BaseFolder')
    creator = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def to_dict(self):
        return {
            'name': self.name,
            'type': 'directory',
            'creator': self.creator,
            'image': self.image,
            'content': (
                [deck.to_dict() for deck in self.decks] if self.decks else
                [folder.to_dict() for folder in self.folders]
            )
        }
