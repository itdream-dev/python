# -*- coding: utf-8 -*-
from tag import Tag  # NOQA
from lib.registry import get_registry

db = get_registry()['DB']


relationship_table = db.Table(
    'answer_association',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'))
)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    tags = db.relationship(
        'Tag', secondary=relationship_table, backref='answer'
    )
