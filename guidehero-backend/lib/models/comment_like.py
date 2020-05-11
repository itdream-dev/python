# -*- coding: utf-8 -*-
from lib.registry import get_registry


db = get_registry()['DB']


class CommentLike(db.Model):
    __tablename__ = 'comment_like'
    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    comment_id = db.Column(db.String, db.ForeignKey('card_comments.id'), primary_key=True)

    user = db.relationship("User", back_populates="liked_comments")
    comment = db.relationship("CardComments", back_populates="liked_users")
