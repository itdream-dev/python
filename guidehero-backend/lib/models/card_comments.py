# -*- coding: utf-8 -*-
import uuid
from lib.registry import get_registry
from lib.models.comment_like import CommentLike


db = get_registry()['DB']


def uuid_gen():
    return str(uuid.uuid4())


class CardComments(db.Model):
    __tablename__ = 'card_comments'
    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    card_id = db.Column(db.String, db.ForeignKey('card.id'), nullable=True)
    comment_id = db.Column(db.String, db.ForeignKey('card_comments.id', name='fk_sub_comments'), nullable=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)
    liked_users = db.relationship("CommentLike", back_populates="comment")

    user = db.relationship("User", back_populates="comments")
    card = db.relationship("Card", back_populates="comments")
    sub_comments = db.relationship("CardComments", backref=db.backref("comment", remote_side=[id]))

    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='pk_card_comments'),
        db.UniqueConstraint('user_id', 'card_id', 'comment_id', name='uq_card_comments'),
    )

    @property
    def likes(self):
        return len(self.liked_users)

    def to_dict(self, user=None):
        def is_liked_by_user():
            if user is None:
                return None
            return len(CommentLike.query.filter(CommentLike.user == user, CommentLike.comment == self).all()) > 0

        return {
            'id': self.id,
            'user_id': self.user.id,
            'name': self.user.name,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'thumbnail_url': self.user.thumbnail_url or '',
            'sub_comments': [c.to_dict() for c in self.sub_comments],
            'likes': self.likes,
            'liked_by_current_user': is_liked_by_user()
        }
