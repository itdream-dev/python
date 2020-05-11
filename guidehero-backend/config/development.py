# -*- coding: utf-8 -*-
import sys
from config.application import GlobalApplicationConfig, GlobalLogConfig
import logging


class ApplicationConfig(GlobalApplicationConfig):

    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/ivysaur'
    DEBUG = True

    CERT_FILE = 'pems/cert_dev.pem'
    KEY_FILE = 'pems/pkey_dev.pem'
    APN_USE_SANDBOX = True

    S3_VIDEO_BUCKET = 'ivysaur-development-video'
    S3_IMAGE_BUCKET = 'ivysaur-development-image'

    S3_VIDEO_CLOUDFRONT = 'https://d7tfpj09w38w8.cloudfront.net'
    S3_IMAGE_CLOUDFRONT = 'https://d3b5mt98r7nr4r.cloudfront.net'


class LogConfig(GlobalLogConfig):
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    ROOT_LEVEL = logging.INFO
    for arg in sys.argv:
        if arg.startswith('--logging='):
            level = arg[len('--logging='):]
            level_code = {
                'CRITICAL': 50,
                'ERROR': 40,
                'WARNING': 30,
                'INFO': 20,
                'DEBUG': 10,
                'NOTSET': 0,
            }[level]
            print('Debug  level {}'.format(level))
            ROOT_LEVEL = level_code
