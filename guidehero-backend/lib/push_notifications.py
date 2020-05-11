# -*- coding: utf-8 -*-
import arrow
import random
from apns import APNs, Payload, Frame
from config import Ivysaur
from lib.registry import get_registry
import logging
_logger = logging.getLogger(__name__)


class PushNotifications(object):

    def __init__(self):
        self.cert = Ivysaur.Config.CERT_FILE
        self.key = Ivysaur.Config.KEY_FILE
        self.use_sandbox = Ivysaur.Config.APN_USE_SANDBOX
        self.device_repo = get_registry()['DEVICE_REPO']
        self.skill_repo = get_registry()['SKILL_REPO']

    def send_notification(self, device_token, message, sound=None):
        apns_enhanced = APNs(use_sandbox=self.use_sandbox,
                             cert_file=self.cert,
                             key_file=self.key,
                             enhanced=True)
        if not sound:
            sound = "default"
        apns_enhanced.gateway_server.register_response_listener(
            self.response_listener
        )
        payload = Payload(alert=message, sound=sound, content_available=True)
        identifier = random.getrandbits(32)

        apns_enhanced.gateway_server.send_notification(
            device_token, payload, identifier=identifier
        )

    def send_notifications(self, frame):
        apns = APNs(use_sandbox=self.use_sandbox,
                    cert_file=self.cert,
                    key_file=self.key,
                    enhanced=True)
        apns.gateway_server.send_notification_multiple(frame)

    def send_expert_requests(self, user, approx_call_time, price_per_min,
                             max_wait, experts):
        frame = Frame()
        for expert in experts:
            frame = self.add_expert_request(
                user, approx_call_time, price_per_min, max_wait, expert, frame
            )
        if frame.notification_data:
            self.send_notifications(frame)

    def add_expert_request(self, user, approx_call_time, price_per_min,
                           max_wait, expert, frame):
        device = self.device_repo.get_latest_device(expert['expert_id'])
        if not device:
            return frame
        device_token = device.device_token
        skill = self.skill_repo.get_skill(expert['skill_id'])
        message = (
            "%s is requesting %s minutes of help for '%s' within the next %s "
            "minutes. $%.2f/min"
        ) % (
            user.first_name, approx_call_time, skill.name, max_wait,
            min(price_per_min, int(expert.get('price', 0))) / 100.00
        )

        now = arrow.utcnow().timestamp
        expiry = now + 3600
        identifier = random.getrandbits(32)
        payload = Payload(alert=message, sound="default")
        frame.add_item(device_token, payload, identifier, expiry, 10)
        return frame

    def response_listener(error_response):
        _logger.debug("client get error-response: " + str(error_response))
