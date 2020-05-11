from tests.app_base_testcase import AppBaseTestCase
from flask import jsonify, Response
from app.api.utils import dict_to_response


class DictToResponseTestCase(AppBaseTestCase):
    def setUp(self):
        super(DictToResponseTestCase, self).setUp()
        self.return_value = None

        self.response = None
        self.status = None

        self.expected_response = None
        self.expected_status = None

    def call_target(self):
        @dict_to_response
        def return_is_dict():
            return self.return_value
        res = return_is_dict()
        if isinstance(res, tuple):
            self.response, self.status = res
        else:
            self.response = res

    def assert_result(self):
        self.assertEqual(self.response.get_data(), self.expected_response.get_data())
        self.assertEqual(self.response.status, '200 OK')
        self.assertEqual(self.status, self.expected_status)

    def test_response_is_dict(self):
        self.return_value = {'one': 1}
        self.expected_response = jsonify(self.return_value)
        self.expected_status = '200 OK'

        self.call_target()
        self.assert_result()

    def test_response_is_response(self):
        self.return_value = Response('12345')
        self.expected_response = Response('12345')

        self.call_target()
        self.assert_result()

    def test_response_is_tuple_with_response(self):
        self.return_value = (Response('12345'), 300)
        self.expected_response = Response('12345')
        self.expected_status = 300

        self.call_target()
        self.assert_result()

    def test_response_is_tuple_with_dict(self):
        self.return_value = ({'one': 1}, 300)
        self.expected_response = jsonify(self.return_value[0])
        self.expected_status = 300

        self.call_target()
        self.assert_result()
