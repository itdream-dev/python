# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class Search(db.Model):

    __tablename__ = 'search'

    id = db.Column(db.Integer, primary_key=True)
    searched_at = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    keyword = db.Column(db.String(255))
