try:
    import unittest2 as unittest
except ImportError:
    import unittest

from .helpers import sauce_helpers as helper
from .helpers.sauce_helpers import travis_only
import sauce


class TestTunnels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce(helper.sauce_user, helper.sauce_key)

    @travis_only
    def test_tunnels_list_tunnels(self):
        tuns = self.sauce.tunnels.list_tunnels()
        self.assertIsInstance(tuns, list)

    @travis_only
    def test_tunnels_list_tunnel(self):
        tuns = self.sauce.tunnels.list_tunnels()
        info = self.sauce.tunnels.get_tunnel_details(tuns[0])
        self.assertEqual(tuns[0], info['id'])

    @travis_only
    def test_tunnels_delete_tunnel(self):
        tuns = self.sauce.tunnels.list_tunnels()
        self.sauce.tunnels.delete_tunnel(tuns[0])
        self.assertNotIn(tuns[0], self.sauce.tunnels.list_tunnels())
