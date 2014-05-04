import requests

import jobs


class Sauce(object):

    def __init__(self, sauce_user, sauce_key):
        self.user = sauce_user
        self.key = sauce_key
        self.jobs = jobs.Jobs(self)
        self.base_url = 'https://{0}:{1}@saucelabs.com'.format(
            self.user, self.key)

    def request(self, method, rel_url, data=None, params=None):
        url = self.base_url + rel_url
        resp = requests.request(method, url, data=data, params=params)
        resp.raise_for_status()
        return resp.json()

    def download(self, rel_url):
        url = self.base_url + rel_url
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.content
