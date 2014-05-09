try:
    import unittest2 as unittest
except ImportError:
    import unittest

from .helpers import sauce_helpers as helpers
import sauce


class TestSauce(unittest.TestCase):

    def setUp(self):
        self.sauce = sauce.Sauce(helpers.sauce_user, helpers.sauce_key)

    def test_counter(self):
        count = self.sauce.counter()
        self.assertIsInstance(count, int)

    def test_browsers(self):
        browsers = self.sauce.browsers()
        self.assertIn('automation_backend', browsers[0],
                      'Did not recieve list of browsers.')

    def test_status(self):
        status = self.sauce.status()
        self.assertIn('status_message', status)
