# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
