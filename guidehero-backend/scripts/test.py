# -*- coding: utf-8 -*-
import os
import sys

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(_root)


from app.ivysaur_app import create_app
ivysaur_env = os.environ.get('IVYSAUR_ENV')
if not ivysaur_env:
    print "please set IVYSAUR_ENV environment var"
    sys.exit(1)

create_app(ivysaur_env)


from lib.push_notifications import PushNotifications


if __name__ == '__main__':
    P = PushNotifications()
    device_token = 'f65408b229246c2806cea01deabd29cee2083567754c6b462b246219e159300b'
    P.send_notification(device_token, 'yoyo')