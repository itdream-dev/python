# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class Device(db.Model):

    device_token = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    device_type = db.Column(db.String(10), primary_key=True)
    updated_at = db.Column(db.Integer)
