"""
Helper functions used by functional tests.
"""

import os
import time

from selenium import webdriver

sauce_user = os.environ['SAUCE_USERNAME']
sauce_key = os.environ['SAUCE_ACCESS_KEY']


def create_session():
    sauce_exec = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'
    sauce_url = sauce_exec.format(sauce_user, sauce_key)
    ctime = time.time()
    driver = webdriver.Remote(
        sauce_url, webdriver.DesiredCapabilities.FIREFOX)
    driver.ctime = ctime
    return driver
