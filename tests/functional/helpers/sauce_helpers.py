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
travis_job_number = os.getenv('TRAVIS_JOB_NUMBER')

if (sauce_user == None or sauce_key == None):
    raise ValueError('Set SAUCE_USERNAME and SAUCE_ACCESS_KEY env variables.')

def create_session(extra=None):
    sauce_exec = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'
    sauce_url = sauce_exec.format(sauce_user, sauce_key)
    ctime = time.time()
    caps = webdriver.DesiredCapabilities.FIREFOX
    if extra:
        caps.update(extra)
    driver = webdriver.Remote(
        sauce_url, caps)
    driver.ctime = ctime
    return driver


def travis_only(func):
    @functools.wraps(func)
    def run_test(*args, **kwargs):
        if not travis:
            raise SkipTest('Tunnel tests are run in travis-ci only.')
        func(*args, **kwargs)
    return attr('travis_only')(run_test)


def wait_until_job_stopped(sauce, session_id):
    """
    Wait for sauce to finish stopping a job.

    This waits long enough for sauce to complete the operation but not long
    enough that the job will time out.
    """
    tries = 0
    status = 'in progress'
    while status == 'in progress' and tries < 10:
        try:
            stat = sauce.jobs.get_job_details(session_id)
            status = stat['status']
        except HTTPError as err:
            if err.respnse.status_code == 404:
                continue
            else:
                raise RuntimeError('Timed out waiting for sauce job to terminate.')
