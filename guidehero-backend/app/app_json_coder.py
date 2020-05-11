from datetime import datetime
import pytz
from flask.json import JSONEncoder
from flask import current_app


class AppJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return encode_datetime(obj, date_format=self.get_dateformat())
        return JSONEncoder.default(self, obj)

    def get_dateformat(self):
        return current_app.config['DATE_FORMAT']


def decode_datetime(s):
    if s is None:
        return None
    return datetime.strptime(s, current_app.config['DATE_FORMAT']).replace(
        tzinfo=pytz.utc
    )


def encode_datetime(dt, date_format=None):
    if date_format is None:
        date_format = current_app.config['DATE_FORMAT']
    return dt.astimezone(pytz.utc).strftime(date_format)
