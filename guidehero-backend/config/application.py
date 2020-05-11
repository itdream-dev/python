# -*- coding: utf-8 -*-
import logging


class GlobalApplicationConfig(object):
    """ Application Defaults """

    SQLALCHEMY_POOL_RECYCLE = 3600
    WTF_CSRF_ENABLED = False
    SECRET_KEY = '\xdc[@\xc0\x8cj\x00`6\xfa\xf3\xce\x1b\x05\xbdN\xa8\xfelk\xdf=A\xb4'  # NOQA
    SECURITY_REGISTER_URL = '/'
    SECURITY_LOGIN_URL = '/'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'd7Wl2tOwed7FvR8a'
    PASSWORD_PLACEHOLDER = 'fCEl3tavMd7FvR8a'

    FACEBOOK_KEY = '27fe84932352f6b582b780a5b83caaf9'

    # MAIL
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'yoheichris@gmail.com'
    MAIL_PASSWORD = 'guidehero20162017'

    # TWILIO
    TWILIO_ACCOUNT_SID = 'ACb1975d0d6a05c2a41ca9eb96e6eae0dd'
    TWILIO_API_KEY = 'SK28f43053444c8fd84c2c7350ab6618d6'
    TWILIO_API_SECRET = 'qyzf0Yw5zSOVFsudJFhdxyqJn9ANQ3Xq'
    TWILIO_CONFIGURATION_SID = 'VSc8c4d1217c121b09e48f35f8081e233a'

    TOKBOX_API_KEY = '45640822'
    TOKBOX_API_SECRET = 'dc07442a4309db1dd059d6f250f7366e92c28839'

    RESTRICT_EXPERTS = False
    SEARCHABLE_EXPERTS = []

    S3_AWS_ACCESS_KEY_ID = 'AKIAINEDUQ2PHQEBEV7Q'
    S3_AWS_SECRET_ACCESS_KEY = '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'

    DATE_FORMAT = '%d %b %Y %H:%M:%S'


class GlobalLogConfig(object):

    FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ROOT_LEVEL = logging.DEBUG
    LOG_TO_CONSOLE = True
    CONSOLE_LEVEL = logging.DEBUG
    LOG_TO_FILE = False
    FILE_BASE = '/var/log/ivysaur/'
    FILE_LEVEL = logging.DEBUG
    TEMP_LOG = False
