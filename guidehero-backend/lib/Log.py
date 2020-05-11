import logging
import sys
import os
from logging.handlers import WatchedFileHandler
import re


class Log(object):

    @classmethod
    def init(cls, config):
        formatter = logging.Formatter(config.FORMAT)
        root = logging.getLogger('')
        root.setLevel(config.ROOT_LEVEL)

        if config.LOG_TO_CONSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(config.CONSOLE_LEVEL)
            console_handler.setFormatter(formatter)
            root.addHandler(console_handler)
        if config.LOG_TO_FILE:
            file_name = cls.generate_log_file_name()
            file_handler = WatchedFileHandler(
                os.path.join(config.FILE_BASE, file_name),
                encoding='utf-8'
            )
            file_handler.setLevel(config.FILE_LEVEL)
            file_handler.setFormatter(formatter)
            root.addHandler(file_handler)
        if config.TEMP_LOG:
            file_name = cls.generate_log_file_name()
            file_handler = WatchedFileHandler(
                os.path.join('', file_name),
                encoding='utf-8'
            )
            file_handler.setLevel(config.FILE_LEVEL)
            file_handler.setFormatter(formatter)
            root.addHandler(file_handler)

    @classmethod
    def generate_log_file_name(cls):
        program = os.path.basename(sys.argv[0])
        if program[-3:] == '.py':

            # we're a normal python program! lets just log
            # the name of the python program
            return program[:-3] + '.log'
        if program == 'nosetests':
            return 'tests.log'

        if program == 'gunicorn':
            # hacky way to have logs with gunicorn apps go to the
            # appropriate location
            m = re.match('.*?([a-zA-Z]+)_gunicorn.*', sys.argv[-1])
            if m:
                return m.groups(1)[0] + '.log'

        if program == 'fab':
            m = re.match('(.*)\..*', sys.argv[1])
            if m:
                # return filename fab_<name of fab file>.log
                return 'fab_' + m.groups(1)[0] + '.log'

        if program == 'mod_wsgi':
            # TODO need to edit here
            pass

        return 'ivysaur.log'

    @staticmethod
    def override_log_level(level):
        """ Overrides log level on all handlers """

        root = logging.getLogger('')
        root.setLevel(level)
        for handler in root.handlers:
            handler.setLevel(level)
