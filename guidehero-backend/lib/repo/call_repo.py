# -*- coding: utf-8 -*-
import arrow
from lib.registry import get_registry
from lib.models.call import Call


class CallRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def start_session(self, user, user2, session_id):
        call = Call(
            session_id=session_id,
            user_id_1=user.id,
            user_id_2=user2.id,
            initiated_at=arrow.utcnow().timestamp,
            status=Call.INITIATED
        )
        self.db.session.add(call)
        self.db.session.commit()

    def get_pending_call(self, user):
        now = arrow.utcnow().timestamp
        return Call.query.filter(
            Call.user_id_2 == user.id,
            Call.status == Call.INITIATED,
            Call.initiated_at + 60 > now
        ).order_by(Call.initiated_at.desc()).first()

    def get_call_from_session_id(self, session_id):
        return Call.query.filter(Call.session_id == session_id).first()

    def report_connected(self, call):
        call.status = Call.CONNECTED
        call.connected_at = arrow.utcnow().timestamp
        self.db.session.merge(call)
        self.db.session.commit()

    def report_ended(self, call):
        call.status = Call.ENDED
        call.ended_at = arrow.utcnow().timestamp
        self.db.session.merge(call)
        self.db.session.commit()
