# -*- coding: utf-8 -*-
from config.application import GlobalLogConfig
from config.development import ApplicationConfig as DevelopmentApplicationConfig
import logging


class ApplicationConfig(DevelopmentApplicationConfig):

    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_ivysaur'
    LOGIN_DISABLED = True


class LogConfig(GlobalLogConfig):
    LOG_TO_FILE = True
    LOG_TO_CONSOLE = True
    ROOT_LEVEL = logging.INFO
