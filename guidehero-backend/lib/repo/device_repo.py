# -*- coding: utf-8 -*-
import arrow
from lib.registry import get_registry
from lib.models.device import Device
from sqlalchemy import desc


class DeviceRepo(object):

    def __init__(self):
        self.db = get_registry()['DB']

    def register_device(self, user, device_token, device_type):
        device = Device(user_id=user.id,
                        device_token=device_token,
                        device_type=device_type,
                        updated_at=arrow.utcnow().timestamp)
        self.db.session.merge(device)
        self.db.session.commit()

    def get_latest_device(self, user_id):
        return Device.query.filter(
            Device.user_id == user_id
        ).order_by(desc(Device.updated_at)).first()

    # def get_latest_device_from_email(self, email):
    #     return Device.query.filter(
    #         Device.email == email
    #     ).order_by(desc(Device.updated_at)).first()

    def get_all_devices(self):
        return Device.query
