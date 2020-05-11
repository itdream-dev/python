# -*- coding: utf-8 -*-
import uuid
from lib.registry import get_registry

db = get_registry()['DB']


def uuid_gen():
    return str(uuid.uuid4())


class Call(db.Model):

    INITIATED = 'initiated'
    CONNECTED = 'connected'
    ENDED = 'ended'

    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)
    session_id = db.Column(db.String(255), primary_key=True)
    user_id_1 = db.Column(db.ForeignKey('user.id'))
    user_id_2 = db.Column(db.ForeignKey('user.id'))
    session_id = db.Column(db.String(255))
    initiated_at = db.Column(db.Integer)
    connected_at = db.Column(db.Integer)
    ended_at = db.Column(db.Integer)
    status = db.Column(db.String(255))

    caller = db.relationship('User', foreign_keys=[user_id_1])
