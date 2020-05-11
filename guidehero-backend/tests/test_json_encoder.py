import flask
from datetime import datetime
from pytz import timezone

from tests.app_base_testcase import AppBaseTestCase


class JsonEncoderTestCase(AppBaseTestCase):
    def test_datetime(self):
        eastern = timezone('US/Eastern')
        data = {'val1': datetime(2016, 11, 28, 9, 51, 38, tzinfo=eastern)}
        json_str = flask.json.dumps(data)
        self.assertEqual(json_str, '{"val1": "28 Nov 2016 14:47:38"}')
