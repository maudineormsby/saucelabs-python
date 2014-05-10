try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

import sauce


@mock.patch.object(sauce.Sauce, 'request')
class TestTunnels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce('sauce-user', 'sauce-key')

    def test_tunnels_list_tunnels(self, mock_req):
        self.sauce.tunnels.list_tunnels()
        mock_req.assert_called_with('GET', '/rest/v1/sauce-user/tunnels')

    def test_tunnels_get_tunnel_details(self, mock_req):
        self.sauce.tunnels.get_tunnel_details('fake-tunnel')
        mock_req.assert_called_with(
            'GET', '/rest/v1/sauce-user/tunnels/fake-tunnel')

    def test_tunnels_delete_tunnel(self, mock_req):
        self.sauce.tunnels.delete_tunnel('fake-tunnel')
        mock_req.assert_called_with(
            'DELETE', '/rest/v1/sauce-user/tunnels/fake-tunnel')
