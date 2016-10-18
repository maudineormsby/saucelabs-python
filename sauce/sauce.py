import os

import requests

from . import jobs
from . import tunnels

class Sauce(object):

    def __init__(self, sauce_user, sauce_key):
        self.user = sauce_user
        self.key = sauce_key
        self.jobs = jobs.Jobs(self)
        self.tunnels = tunnels.Tunnels(self)
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

    def status(self):
        """
        Returns the status of the Saucelabs service.
        """
        info_url = '/rest/v1/info/status'
        return self.request('GET', info_url)

    def browsers(self, se_version='all'):
        """
        Returns the list of browsers supported for a given version of selenium.

        Args:
          se_version: The version of selenium to use to list compatible
            browsers. Should be 'selenium-rc' or 'webdriver'.

        Returns:
          List of supported browser, version, and os combinations.

        Raises:
          NameError: If se_version is an unrecognized selenium version.
        """
        browser_url = '/rest/v1/info/browsers/'
        if se_version in ('all', 'selenium-rc', 'webdriver'):
            browser_url = ''.join((browser_url, se_version))
        else:
            raise ValueError(
                'Unsupported Selenium version: {0}'.format(se_version))
        return self.request('GET', browser_url)

    def counter(self):
        """
        Returns the number of jobs run on Saucelabs service.
        """
        counter_url = '/rest/v1/info/counter'
        return self.request('GET', counter_url)
