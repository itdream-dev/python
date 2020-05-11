# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class UserRoleCard(db.Model):
    __tablename__ = 'user_role_card'
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.String(255), db.ForeignKey('card_role.id'), primary_key=True)
    card_id = db.Column(db.String(255), db.ForeignKey('card.id'), primary_key=True)

    # how many points contributed by user to the card, valid only for creator and joined users
    contribution = db.Column(db.Integer(), default=0, server_default='0', nullable=False)

    # how many points user received for correct solution
    prize = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
    # how many total likes user get for all his/her solutions
    total_likes = db.Column(db.Integer(), default=0, server_default='0', nullable=False)
