try:
    import unittest2 as unittest
except ImportError:
    import unittest

from .helpers import sauce_helpers as helpers
from .helpers.sauce_helpers import travis_only
import sauce


class TestTunnels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce(helpers.sauce_user, helpers.sauce_key)
        cls.driver = helpers.create_session({'tunnel-identifier': helpers.travis_job_number})

    @travis_only
    def test_tunnels_list_tunnels(self):
        tuns = self.sauce.tunnels.list_tunnels()
        self.assertIsInstance(tuns, list)

    @travis_only
    def test_tunnel_details(self):
        tuns = self.sauce.tunnels.list_tunnels()
        info = self.sauce.tunnels.get_tunnel_details(tuns[0])
        self.assertEqual(tuns[0], info['id'])

class TestTunnelsDelete(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce(helpers.sauce_user, helpers.sauce_key)
        cls.driver = helpers.create_session({'tunnel-identifier': helpers.travis_job_number})

    @travis_only
    def test_tunnels_delete_tunnel(self):
        tuns = self.sauce.tunnels.list_tunnels()
        self.sauce.tunnels.delete_tunnel(tuns[0])
        tries = 0
        # this is terrible but tunnels take time to close
        while tuns[0] in self.sauce.tunnels.list_tunnels():
            sleep(.5)
        self.assertNotIn(tuns[0], self.sauce.tunnels.list_tunnels())
