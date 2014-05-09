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
        test_file='file.txt'
        with mock.patch('__builtin__.open', mock.mock_open(read_data='test'), create=True) as mopen:
            self.sauce.upload_file(test_file, overwrite=True)
            mock_req.assert_called_with(
                'https://sauce-user:sauce-key@saucelabs.com/storage/sauce-user/file.txt',
                headers={'Content-Type': 'application/octet-stream'},
                data=open(test_file)
            )
