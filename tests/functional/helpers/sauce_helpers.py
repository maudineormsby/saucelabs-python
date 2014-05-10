"""
Helper functions used by functional tests.
"""

import functools
import os
import time

from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest
from selenium import webdriver

sauce_user = os.getenv('SAUCE_USERNAME')
sauce_key = os.getenv('SAUCE_ACCESS_KEY')
travis = os.getenv('TRAVIS', False)


def create_session():
    sauce_exec = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'
    sauce_url = sauce_exec.format(sauce_user, sauce_key)
    ctime = time.time()
    driver = webdriver.Remote(
        sauce_url, webdriver.DesiredCapabilities.FIREFOX)
    driver.ctime = ctime
    return driver


def travis_only(func):
    @functools.wraps(func)
    def run_test(*args, **kwargs):
        if not travis:
            raise SkipTest('Tunnel tests are run in travis-ci only.')
        func(*args, **kwargs)
    return attr('travis_only')(run_test)
