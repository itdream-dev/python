# -*- coding: utf-8 -*-
from flask.ext.security import RoleMixin
from lib.registry import get_registry

db = get_registry()['DB']


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
