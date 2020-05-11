# -*- coding: utf-8 -*-
from config.application import GlobalApplicationConfig, GlobalLogConfig
import logging


class ApplicationConfig(GlobalApplicationConfig):

    SQLALCHEMY_DATABASE_URI = 'postgresql://ivysaur:ivysaur2013redsox@ivysaur.ccbco11iv3s9.us-east-1.rds.amazonaws.com:5432/ivysaur'  # NOQA
    DEBUG = False

    CERT_FILE = 'pems/cert_prod.pem'
    KEY_FILE = 'pems/pkey_prod.pem'
    APN_USE_SANDBOX = False
    RESTRICT_EXPERTS = True
    SEARCHABLE_EXPERTS = ['chrisryuichi@gmail.com', 'yoyo716jp@gmail.com']

    S3_VIDEO_BUCKET = 'ivysaur-production-video'
    S3_IMAGE_BUCKET = 'ivysaur-production-image'

    S3_VIDEO_CLOUDFRONT = 'https://dowbozmvgoreb.cloudfront.net'
    S3_IMAGE_CLOUDFRONT = 'https://dx7a8qmcex4os.cloudfront.net'


class LogConfig(GlobalLogConfig):
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = False
    ROOT_LEVEL = logging.INFO
    FILE_LEVEL = logging.INFO
    TEMP_LOG = True
