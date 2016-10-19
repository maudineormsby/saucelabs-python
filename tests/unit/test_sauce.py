try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock
import requests

import sauce


class TestStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce('sauce-user', 'sauce-key')

    @mock.patch.object(requests, 'post')
    def test_storage_upload(self, mock_req):
        test_file = 'file.txt'
        with mock.patch('sauce.sauce.open', mock.mock_open(read_data='test'), create=True) as m:
            self.sauce.upload_file(test_file, overwrite=True)
            mock_req.assert_called_with(
                'https://sauce-user:sauce-key@saucelabs.com/storage/sauce-user/file.txt',
                headers={'Content-Type': 'application/octet-stream'},
                data=m.return_value
            )

    @mock.patch.object(requests, 'request')
    def test_sauce_status(self, mock_req):
        self.sauce.status()
        mock_req.assert_called_with(
            'GET',
            'https://sauce-user:sauce-key@saucelabs.com/rest/v1/info/status',
            data=None, params=None
        )

    @mock.patch.object(requests, 'request')
    def test_sauce_browsers(self, mock_req):
        self.sauce.browsers()
        mock_req.assert_called_with(
            'GET',
            'https://sauce-user:sauce-key@saucelabs.com/rest/v1/info/browsers/all',
            data=None, params=None
        )
        self.sauce.browsers('webdriver')
        mock_req.assert_called_with(
            'GET',
            'https://sauce-user:sauce-key@saucelabs.com/rest/v1/info/browsers/webdriver',
            data=None, params=None
        )
        self.assertRaises(ValueError, self.sauce.browsers, 'frobnaz')

    @mock.patch.object(requests, 'request')
    def test_sauce_counter(self, mock_req):
        self.sauce.counter()
        mock_req.assert_called_with(
            'GET',
            'https://sauce-user:sauce-key@saucelabs.com/rest/v1/info/counter',
            data=None, params=None
        )
