# -*- coding: utf-8 -*-
import uuid
from tag import Tag  # NOQA
from lib.registry import get_registry
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import text
from lib.models.card_likes import CardLikes  # NOQA
from lib.models.card_role import CardRole
from lib.models.user import serialize_user_extended
import utils

db = get_registry()['DB']


def uuid_gen():
    return str(uuid.uuid4())


DISTRIBUTION_RULE_SPLIT_EVENLY = 'evenly'
DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY = 'proportionally'

ANSWER_VISIBILITY_ANYONE = 'anyone'
ANSWER_VISIBILITY_ONLY_ASKERS = 'only_askers'


EVALUATION_PERIOD_STATUS_CLOSE = 'close'
EVALUATION_PERIOD_STATUS_OPEN = 'open'
EVALUATION_PERIOD_STATUS_DONE = 'done'


def assert_ask_deck_open(card):
    if not card.is_ask_mode_enabled:
        raise ValueError('Desk is not in ask mode')
    if card.evaluation_period_status != EVALUATION_PERIOD_STATUS_OPEN:
        raise ValueError('Evaluation period for deck is not open')


card_tag_relation_table = db.Table(
    'card_tag',
    db.Column('card_id', db.String, db.ForeignKey('card.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False)
)


card_user_views_relation_table = db.Table(
    'card_user_views',
    db.Column('card_id', db.String, db.ForeignKey('card.id'), nullable=False),
    db.Column('user_id', db.String, db.ForeignKey('user.id'), nullable=False)
)


class Card(db.Model):

    DECK = 'deck'
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'

    DISTRIBUTION_RULE_SPLIT_EVENLY = 'evenly'
    DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY = 'proportinally'

    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)
    type = db.Column(db.String(255))
    name = db.Column(db.String(255))
    content = db.Column(db.String(255))
    sub_content = db.Column(db.String(255))
    language = db.Column(db.String(255), default='')
    pronunciation = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    created_at = db.Column(db.Integer)
    updated_at = db.Column(db.Integer)
    published = db.Column(db.Boolean(),
                          default=False,
                          server_default='false',
                          nullable=False)
    description = db.Column(db.Text(),
                            default='',
                            server_default='',
                            nullable=False)
    parent_id = db.Column(db.String, db.ForeignKey('card.id'))
    position = db.Column(db.Integer)

    cards = db.relationship('Card',
                            order_by="Card.position",
                            collection_class=ordering_list('position'),
                            backref=db.backref('parent', remote_side=[id]),
                            )
    creator = db.relationship('User')
    x_position = db.Column(db.Float)
    y_position = db.Column(db.Float)
    height = db.Column(db.Float)
    width = db.Column(db.Float)
    scale = db.Column(db.Integer, nullable=True)
    silver_points = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    original_prize_pool = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    gold_points = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    prize_to_join = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    answer_visibility = db.Column(db.String(50), default=ANSWER_VISIBILITY_ANYONE, server_default=ANSWER_VISIBILITY_ANYONE, nullable=False)
    liked_users = db.relationship("CardLikes", back_populates="card")
    comments = db.relationship("CardComments", back_populates="card")
    related_users = db.relationship('UserRoleCard', backref='card', cascade="delete")
    is_ask_mode_enabled = db.Column(
        db.Boolean,
        default=False,
        server_default='false',
        nullable=False
    )
    format = db.Column(
        db.Text,
        default='',
        server_default='',
        nullable=False
    )
    distribution_rule = db.Column(
        db.String(20),
        default=DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY,
        server_default=DISTRIBUTION_RULE_SPLIT_PROPORTIONALLY,
        nullable=False
    )
    distribution_for = db.Column(
        db.Integer(),
        nullable=True
    )
    evaluation_start_dt = db.Column(db.DateTime(timezone=True), nullable=True)
    evaluation_end_dt = db.Column(db.DateTime(timezone=True), nullable=True)
    evaluation_period_status = db.Column(
        db.String(50),
        nullable=False,
        default=EVALUATION_PERIOD_STATUS_CLOSE,
        server_default=EVALUATION_PERIOD_STATUS_CLOSE
    )
    is_answer = db.Column(
        db.Boolean,
        default=False,
        server_default='false',
        nullable=False
    )
    tags = db.relationship(
        'Tag',
        secondary=card_tag_relation_table,
        backref='cards'
    )
    video_length = db.Column(
        db.Integer(),
        nullable=True
    )
    views = db.relationship(
        'User',
        secondary=card_user_views_relation_table
    )

    @property
    def views_count(self):
        return len(self.views)

    @db.validates('silver_points')
    def validate_silver_points(self, key, value):
        return utils.validate_points(value)

    @db.validates('gold_points')
    def validate_gold_points(self, key, value):
        return utils.validate_points(value)

    def get_answers(self):
        return (card for card in self.cards if card.is_answer)

    def get_winners(self):
        return [u for u in self.related_users if u.prize > 0]

    def get_sponsors(self):
        return [u for u in self.related_users if u.contribution > 0]

    def get_givers(self):
        res = []
        ids = []
        for child in self.get_answers():
            if child.creator and child.creator.id not in ids:
                res.append(child.creator)
                ids.append(child.creator.id)
        return res

    def to_dict_structure_only(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'is_ask_mode_enabled': self.is_ask_mode_enabled,
            'children': [c.to_dict_structure_only() for c in self.cards]
        }

    def to_dict(self, user=None):
        serialized = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'content': self.content,
            'sub_content': self.sub_content,
            'creator': self.creator.name if self.creator else 'Chris Yamamoto',
            'creator_full_name': self.creator.full_name,
            'creator_bio': self.creator.bio or '',
            'creator_thumbnail': (
                self.creator.thumbnail_url if self.creator else ''
            ),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'description': self.description,
            'likes': len(self.liked_users),
            'views_count': self.views_count,
            'liked_by_me': False,
            'silver_points': self.silver_points,
            'prize_to_join': self.prize_to_join,
            'original_prize_pool': self.original_prize_pool,
            'comments': [
                comment.to_dict(user) for comment in self.comments
            ],
            'ask_enabled': bool(self.is_ask_mode_enabled),
            'answer_visibility': self.answer_visibility,
            'tags': [tag.name for tag in self.tags],
            'scale': self.scale,
            'gives_by_me': False
        }

        if self.type == Card.IMAGE:
            serialized['image_scale'] = self.scale
        if self.creator:
            serialized['creator_info'] = serialize_user_extended(self.creator)
        children = self.cards
        if children:
            serialized['children'] = [
                child.to_dict(user=user) for child in children
            ]
        if self.type == self.TEXT:
            serialized.update({
                'pronunciation': self.pronunciation,
                'language': self.language
            })
        if self.type == self.IMAGE:
            serialized.update({
                'image_x': self.x_position or 0,
                'image_y': self.y_position or 0,
                'image_width': self.height or 0,
                'image_height': self.width or 0
            })
        if self.type == self.VIDEO:
            serialized.update({
                'video_length': self.video_length
            })
        if self.type == self.DECK:
            serialized['published'] = self.published

        if user:
            liked_cards = [
                liked_card.card_id for liked_card in user.liked_cards
            ]
            serialized['liked_by_me'] = self.id in liked_cards

            serialized['viewed_by_me'] = user in self.views
            serialized['commented_by_me'] = bool([c for c in self.comments if c.user == user])
        serialized['is_answer'] = self.is_answer
        if self.is_ask_mode_enabled:
            serialized['format'] = self.format
            serialized['evaluation_period_status'] = (
                self.evaluation_period_status
            )
            serialized['distribution_rule'] = self.distribution_rule
            serialized['distribution_for'] = self.distribution_for
            serialized['evaluation_start_dt'] = self.evaluation_start_dt
            serialized['evaluation_end_dt'] = self.evaluation_end_dt
            serialized['asked_users'] = [
                serialize_user(u)
                for u in get_related_users(self, CardRole.ASKED)
            ]
            serialized['joined_users'] = [
                serialize_user(u)
                for u in get_related_users(self, CardRole.JOINED)
            ]
            serialized['givers'] = [
                serialize_user(u)
                for u in self.get_givers()
            ]
            serialized['winners'] = [
                serialize_user_role_card(u)
                for u in self.get_winners()
            ]
            serialized['sponsors'] = [
                serialize_user_role_card(u)
                for u in self.get_sponsors()
            ]
            if self.creator:
                for u in serialized['joined_users']:
                    if u['user_id'] == self.creator.id:
                        u['ask_creator'] = True
            if user:
                serialized['won_by_me'] = bool(
                    [True for it in self.get_winners() if it.user == user]
                )
                if children:
                    serialized['gives_by_me'] = bool(
                        [
                            True for child in children[1:] if
                            child.user_id == user.id
                        ]
                    )
        return serialized


def serialize_user_role_card(urc):
    data = serialize_user(urc.user)
    data['prize'] = urc.prize
    data['contribution'] = urc.contribution
    return data


def get_related_users(card, role_id):
    db = get_registry()['DB']
    sql_str = '''SELECT u.id, u.email, u.stripped_email, u.first_name, u.last_name, u.username,
u.bio, u.thumbnail_url, u.linkedin_profile, u.linkedin_headline, u.active, u.confirmed_at, u.source,
u.tier, urc.role_id, urc.contribution, urc.prize
FROM "user" u JOIN user_role_card urc ON (u.id = urc.user_id)
WHERE urc.role_id = :role_id and urc.card_id = :card_id'''
    sql = text(sql_str)
    result = list(db.engine.execute(sql, {'role_id': role_id, 'card_id': card.id}))
    return result


def serialize_user(user):
    data = serialize_user_extended(user)
    if hasattr(user, 'role_id') and user.role_id == CardRole.JOINED:
        data['contribution'] = user.contribution
    return data
