# -*- coding: utf-8 -*-
from lib.registry import get_registry


db = get_registry()['DB']


class CardLikes(db.Model):
    __tablename__ = 'card_likes'
    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    card_id = db.Column(db.String, db.ForeignKey('card.id'), primary_key=True)

    user = db.relationship("User", back_populates="liked_cards")
    card = db.relationship("Card", back_populates="liked_users")
