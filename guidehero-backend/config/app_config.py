# -*- coding: utf-8 -*-
from lib import Log


class Ivysaur(object):
    Config = None
    LogConfig = None

    @staticmethod
    def init_config(env):
        if env == 'development':
            import development as env_config
        elif env == 'staging':
            import staging as env_config
        elif env == 'production':
            import production as env_config
        elif env == 'test':
            import tests as env_config
        else:
            raise Exception("Environment not found: %s" % env)

        Ivysaur.Config = env_config.ApplicationConfig
        Ivysaur.LogConfig = env_config.LogConfig


def init_config(env=None):
    init_constants(env)
    Log.init(Ivysaur.LogConfig)


def init_constants(env):
    Ivysaur.init_config(env)
