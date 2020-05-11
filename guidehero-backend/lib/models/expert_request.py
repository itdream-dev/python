# -*- coding: utf-8 -*-
from lib.registry import get_registry

db = get_registry()['DB']


class ExpertRequest(db.Model):

    REQUESTED = 'requested'
    CANCELLED = 'cancelled'
    __tablename__ = 'expert_request'

    requested_at = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.String, db.ForeignKey('user.id'), primary_key=True)
    expert_id = db.Column(
        db.String, db.ForeignKey('user.id'), primary_key=True)
    skill_id = db.Column(
        db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    status = db.Column(db.String(50))
    expires_at = db.Column(db.Integer)
    approx_call_time = db.Column(db.Integer)
    price_per_min = db.Column(db.Integer)

    user = db.relationship("User", foreign_keys=[user_id])
    expert = db.relationship("User", foreign_keys=[expert_id])
    skill = db.relationship("Skill", foreign_keys=[skill_id])

    def to_dict(self):
        return {
            'user': self.user.get_basic_data(),
            'skill_id': self.skill_id,
            'skill_name': self.skill.name,
            'expires_at': self.expires_at,
            'approx_call_time': self.approx_call_time,
            'price_per_min': self.price_per_min
        }
