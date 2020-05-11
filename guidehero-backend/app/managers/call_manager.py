# -*- coding: utf-8 -*-
from config import Ivysaur
from lib.registry import get_registry
from lib.models.call import Call
from lib.push_notifications import PushNotifications


class CallManager(object):

    def __init__(self):
        registry = get_registry()
        self.call_repo = registry['CALL_REPO']
        self.user_repo = registry['USER_REPO']
        self.device_repo = registry['DEVICE_REPO']
        self.tokbox = registry['TOKBOX']
        self.push_notifications = PushNotifications()

    def start_session(self, user, user_id_2):
        session = self.tokbox.create_session()
        session_id = session.session_id
        token = self.tokbox.generate_token(session_id)

        recepient = self.user_repo.get_user(user_id_2)
        self.call_repo.start_session(user, recepient, session_id)
        device = self.device_repo.get_latest_device(user_id_2)
        if device:
            self.push_notifications.send_notification(
                device.device_token,
                'Incoming call from %s' % user.name,
                sound='calling.caf'
            )
        return {
            'api_key': Ivysaur.Config.TOKBOX_API_KEY,
            'session_id': session_id,
            'token': token
        }

    def get_pending_call(self, user):
        pending_call = self.call_repo.get_pending_call(user)
        if not pending_call:
            return {}
        session_id = pending_call.session_id
        token = self.tokbox.generate_token(session_id)

        return {
            'api_key': Ivysaur.Config.TOKBOX_API_KEY,
            'session_id': session_id,
            'token': token,
            'caller_name': pending_call.caller.name
        }

    def report_connected(self, session_id):
        call = self.call_repo.get_call_from_session_id(session_id)
        if not call or call.status != Call.INITIATED:
            return
        self.call_repo.report_connected(call)

    def report_ended(self, session_id):
        call = self.call_repo.get_call_from_session_id(session_id)
        if not call or call.status == Call.ENDED:
            return
        self.call_repo.report_ended(call)
