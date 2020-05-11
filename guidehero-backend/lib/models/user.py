# -*- coding: utf-8 -*-
import uuid
from flask.ext.security import UserMixin
from roles_users import roles_users
from lib.registry import get_registry
from lib.models.skill import Skill  # NOQA
from lib.models.card_likes import CardLikes  # NOQA
from lib.models.card_comments import CardComments  # NOQA
import utils

db = get_registry()['DB']
relationship_table = db.Table(
    'user_skills',
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')),
    db.Column('user_id', db.String, db.ForeignKey('user.id'))
)


follower_following = db.Table(
    'follower_folling',
    db.Column('follower_id', db.String, db.ForeignKey('user.id'), primary_key=True),
    db.Column('following_id', db.String, db.ForeignKey('user.id'), primary_key=True)
)


class UserSkill(db.Model):

    __tablename__ = 'user_skill'
    user_id = db.Column(db.String, db.ForeignKey('user.id'), primary_key=True)
    skill_id = db.Column(
        db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    level = db.Column(db.String(50))
    details = db.Column(db.Text())
    price = db.Column(db.Integer)
    skill = db.relationship('Skill')

    def to_dict(self):
        return {
            'skill_id': self.skill_id,
            'level': self.level,
            'details': self.details,
            'price': self.price,
            'skill_name': self.skill.name
        }


def uuid_gen():
    return str(uuid.uuid4())


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    ANYONE_ID = '_anyone_'
    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)
    email = db.Column(db.String(255), unique=True)
    stripped_email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255), default='')
    last_name = db.Column(db.String(255), default='')
    username = db.Column(db.String(255), unique=True)
    bio = db.Column(db.Text)

    thumbnail_url = db.Column(db.String(255))
    linkedin_profile = db.Column(db.String(255))
    linkedin_headline = db.Column(db.String(255))

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.Integer)
    source = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    cards = db.relationship('Card')
    liked_cards = db.relationship("CardLikes", back_populates="user")
    comments = db.relationship("CardComments", back_populates="user")
    liked_comments = db.relationship("CommentLike", back_populates="user")

    silver_points = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    gold_points = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    related_cards = db.relationship('UserRoleCard', backref='user', cascade="delete")

    tier = db.Column(db.String(255), default='')

    followers = db.relationship(
        "User",
        secondary=follower_following,
        primaryjoin=id==follower_following.c.following_id,
        secondaryjoin=id==follower_following.c.follower_id,
        backref="followings"
    )

    verification_code = db.Column(db.String(255), default=None, nullable=True)
    confirmation_email = db.relationship("ConfirmationEmail", uselist=False)

    @db.validates('silver_points')
    def validate_address(self, key, value):
        return utils.validate_points(value)

    @db.validates('gold_points')
    def validate_address(self, key, value):
        return utils.validate_points(value)

    @property
    def name(self):
        if self.username:
            return self.username

        user_repo = get_registry()['USER_REPO']
        user = user_repo.set_default_username(self)
        if self.username:
            return user.username
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_basic_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'thumbnail_url': self.thumbnail_url or '',
            'linkedin_profile': self.linkedin_profile or '',
            'headline': self.linkedin_headline or ''
        }

    def get_extended_data(self):
        return serialize_user_extended(self)


def serialize_user_extended(user):
        return {
            'user_id': user.id,
            'email': user.email,
            'stripped_email': user.stripped_email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'bio': user.bio,

            'thumbnail_url': user.thumbnail_url,
            'linkedin_profile': user.linkedin_profile,
            'linkedin_headline': user.linkedin_headline,

            'active': user.active,
            'confirmed_at': user.confirmed_at,
            'source': user.source,
            'tier': user.tier
        }
