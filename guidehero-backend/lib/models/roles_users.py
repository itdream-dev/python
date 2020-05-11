# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.String(255), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
)
