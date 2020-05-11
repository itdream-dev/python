# -*- coding: utf-8 -*-
from lib.registry import get_registry
import uuid

db = get_registry()['DB']


def uuid_gen():
    return str(uuid.uuid4())


class Transfer(db.Model):
    __tablename__ = 'transfer'
    id = db.Column(db.String(255), primary_key=True, default=uuid_gen)

    user_from_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=True)
    user_from = db.relationship('User', foreign_keys=[user_from_id])

    card_from_id = db.Column(db.String(255), db.ForeignKey('card.id'), nullable=True)
    card_from = db.relationship('Card', foreign_keys=[card_from_id])

    user_to_id = db.Column(db.String(255), db.ForeignKey('user.id'), nullable=True)
    user_to = db.relationship('User', foreign_keys=[user_to_id])

    card_to_id = db.Column(db.String(255), db.ForeignKey('card.id'), nullable=True)
    card_to = db.relationship('Card', foreign_keys=[card_to_id])

    silver_points = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    gold_points = db.Column(db.Integer, default=0, server_default='0', nullable=False)
    transaction_type = db.Column(db.String, default='', server_default='', nullable=False)


class TransferTypes(object):
    def __init__(self):
        self.__types = [
            TransferTypeBase(code='send_to_friend'),
            TransferTypeWithSilverPoints(code='create_ask', silver_points=66),
            TransferTypeBase(code='end_evaluation_period'),
            TransferTypeBase(code='prize_for_answer'),
            TransferTypeBase(code='purchase'),
            TransferTypeBase(code='join_ask'),
            TransferTypeWithSilverPoints(code='verify_with_facebook', silver_points=25),

            # FOR TESTING
            TransferTypeBase(code='earn'),
            TransferTypeBase(code='use'),
        ]

    def __getitem__(self, name):
        for tt in self.__types:
            if tt.code == name:
                return tt
        options = [tt.code for tt in self.__types]
        raise ValueError('Can not find transaction for code: {}, available transfers: {}'.format(name, options))


class TransferTypeBase(object):
    def __init__(self, code):
        self.__code = code

    @property
    def code(self):
        return self.__code

    def __str__(self):
        return self.code


class TransferTypeWithSilverPoints(TransferTypeBase):
    def __init__(self, silver_points, *args, **kwargs):
        super(TransferTypeWithSilverPoints, self).__init__(*args, **kwargs)
        self.__silver_points = silver_points

    @property
    def silver_points(self):
        return self.__silver_points

TYPES = TransferTypes()
