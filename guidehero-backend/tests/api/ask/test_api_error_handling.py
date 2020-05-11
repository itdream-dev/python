import json
import mock
from ..base import ApiBaseTestCase


class ErrorHandlingTestCase(ApiBaseTestCase):
    def __init__(self, *args, **kwargs):
        super(ErrorHandlingTestCase, self).__init__(*args, **kwargs)
        self.url = '/api/v1/deck/test_error_handling'

    def setUp(self):
        super(ErrorHandlingTestCase, self).setUp()
        self.view_patcher = mock.patch('app.api.deck_api.test_error_handling_process')
        self.view_mock = self.view_patcher.start()
        self.app.config['DEBUG'] = False

    def tearDown(self):
        super(ErrorHandlingTestCase, self).tearDown()
        self.app.config['DEBUG'] = True

    def test_success(self):
        self.view_mock.return_value = {'result': 'success'}, 200
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status, '200 OK')

    def test_error_handling(self):
        self.view_mock.side_effect = [ValueError('Something Wrong')]
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(response.status, '400 BAD REQUEST')
        data = json.loads(response.data)
        self.assertEqual(data, {'error': 'Something Wrong'})
