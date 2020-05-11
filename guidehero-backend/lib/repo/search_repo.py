# -*- coding: utf-8 -*-
import arrow
from lib.registry import get_registry
from lib.models.search import Search
from lib.models.skill import Skill
from lib.models.user import User
from lib.models.expert_request import ExpertRequest
from lib.email import EmailHelper
from lib.push_notifications import PushNotifications
from sqlalchemy import desc


class SearchRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def add_searches(self, user, keywords):
        now = arrow.utcnow().timestamp
        for keyword in keywords:
            search = Search(
                searched_at=now,
                keyword=keyword,
                user_id=user.id
            )
            self.db.session.add(search)
        self.db.session.commit()

    def request_help(self, user, expert, user_skill):
        now = arrow.utcnow()
        expert_request = ExpertRequest(
            requested_at=now.timestamp,
            user_id=user.id,
            expert_id=expert.id,
            skill_id=user_skill.skill.id,
            status=ExpertRequest.REQUESTED
        )
        self.db.session.add(expert_request)
        self.db.session.commit()
        EmailHelper().send_email(user, expert, user_skill, now)

    def cancel_help(self, user, expert, user_skill):
        expert_request = ExpertRequest.query.filter(
            ExpertRequest.user_id == user.id,
            ExpertRequest.expert_id == expert.id,
            ExpertRequest.skill_id == user_skill.skill.id
        ).order_by(desc(ExpertRequest.requested_at)).first()

        if not expert_request:
            return

        expert_request.status = ExpertRequest.CANCELLED
        self.db.session.merge(expert_request)
        self.db.session.commit()
        EmailHelper().send_cancel_email(user, expert, user_skill)

    def request_experts(self, user, approx_call_time, price_per_min, max_wait,
                        experts):
        now = arrow.utcnow()
        expires_at = now.replace(minutes=max_wait)
        for expert in experts:
            expert_request = ExpertRequest(
                requested_at=now.timestamp,
                expires_at=expires_at.timestamp,
                user_id=user.id,
                expert_id=expert['expert_id'],
                skill_id=expert['skill_id'],
                status=ExpertRequest.REQUESTED,
                price_per_min=min(price_per_min, int(expert.get('price', 0))),
                approx_call_time=approx_call_time
            )
            self.db.session.add(expert_request)
        self.db.session.commit()
        PushNotifications().send_expert_requests(
            user, approx_call_time, price_per_min, max_wait, experts
        )

    def get_offers(self, user):
        now = arrow.utcnow()
        return ExpertRequest.query.filter(
            ExpertRequest.expert_id == user.id,
            ExpertRequest.expires_at > now.timestamp
        ).all()

        return self.db.session.query(
            ExpertRequest, Skill, User
        ).filter(
            ExpertRequest.expert_id == user.id,
            ExpertRequest.expires_at > now.timestamp
        ).all()
