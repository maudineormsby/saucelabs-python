class Tunnels(object):

    def __init__(self, sauce):
        self.sauce = sauce
        self.tunnels_url = '/rest/v1/{0}/tunnels'.format(self.sauce.user)

    def list_tunnels(self):
        return self.sauce.request('GET', self.tunnels_url)

    def get_tunnel_details(self, tunnel_id):
        url = '/'.join((self.tunnels_url, tunnel_id))
        return self.sauce.request('GET', url)

    def delete_tunnel(self, tunnel_id):
        url = '/'.join((self.tunnels_url, tunnel_id))
        return self.sauce.request('DELETE', url)
