# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class Skill(db.Model):

    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
