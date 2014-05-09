import os

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

    def upload_file(self, user_file, dest_file=None, overwrite=False):
        """
        Uploads a file to sauce's temporary storage.

        Args:
          user_file: relative or absolute path to the file to upload to sauce.
          dest_file: filename to use in sauce's system.
          overwrite: whether the file in sauce's system should be overwritten.

        Returns:
          None
        """
        if not dest_file:
            file_name = os.path.basename(user_file)
        url = self.base_url + '/storage/{0}/{1}'.format(self.user, file_name)
        user_file_path = os.path.abspath(user_file)
        with open(user_file_path) as upload_data:
            headers = {'Content-Type': 'application/octet-stream'}
            requests.post(url, data=upload_data, headers=headers)
