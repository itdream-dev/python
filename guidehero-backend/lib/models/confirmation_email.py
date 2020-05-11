# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class ConfirmationEmail(db.Model):

    __tablename__ = 'confirmation_email'
    id = db.Column(db.String(255), primary_key=True)
    confirmation_code = db.Column(db.String(10))
    attempts = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)
    verified = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    username = db.Column(db.String(255), unique=True)
    year = db.Column(db.Integer)
