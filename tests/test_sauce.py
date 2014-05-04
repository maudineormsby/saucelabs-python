import os
import tempfile
import time
import unittest

from requests.exceptions import HTTPError
from selenium import webdriver

import sauce

sauce_user = os.environ['SAUCE_USERNAME']
sauce_key = os.environ['SAUCE_ACCESS_KEY']


def create_session():
    sauce_exec = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'
    sauce_url = sauce_exec.format(sauce_user, sauce_key)
    ctime = time.time()
    driver = webdriver.Remote(sauce_url, webdriver.DesiredCapabilities.FIREFOX)
    driver.ctime = ctime
    return driver


class TestJobs(unittest.TestCase):
    '''
    Test the Jobs API client.
    '''

    @classmethod
    def setUpClass(cls):
        cls.driver = create_session()
        cls.sauce = sauce.Sauce(sauce_user, sauce_key)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_job_ids(self):
        resp = self.sauce.jobs.list_jobs()
        for job in resp:
            assert job['id'], "No response for GET job ids."

    def test_job_id_limit(self):
        resp = self.sauce.jobs.list_jobs(limit=1)
        assert len(resp) == 1, "Got too many jobs from API."

    def test_job_full(self):
        resp = self.sauce.jobs.list_jobs(full=True)
        for res in resp:
            assert res['creation_time'], "Did not get full data for job."

    def test_job_skip(self):
        resp = self.sauce.jobs.list_jobs(skip=1)
        comp_time = time.time()
        try:
            assert resp[0]['id'] != self.driver.session_id, "Did not skip."
        except AssertionError:
            # handle case where a job is created after the job checked above
            resp = self.sauce.jobs.list_jobs(full=True)
            if resp[0]['id'] == self.driver.session_id:
                raise
            for idx, job in enumerate(resp):
                if job['id'] == self.driver.session_id:
                    last_job = resp[idx - 1]
                    break
            if comp_time > last_job['creation_time'] > self.driver.ctime:
                return
            raise

    def test_job_details(self):
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['creation_time'], "Did not get full data for job."

    def test_job_update_name(self):
        name = "Test Job update name"
        self.sauce.jobs.update_job(self.driver.session_id, name=name)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['name'] == name, "Name from API wrong."

    def test_job_update_tags(self):
        tags = ['test', 'job', 'update']
        self.sauce.jobs.update_job(self.driver.session_id, tags=tags)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['tags'] == tags, "Tags from API wrong."

    def test_job_update_public_bool(self):
        public = True
        self.sauce.jobs.update_job(self.driver.session_id, public=public)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['public'] == "public", "Public setting from API wrong."

    def test_job_update_public_str(self):
        public = "public"
        self.sauce.jobs.update_job(self.driver.session_id, public=public)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['public'] == public, "Public setting from API wrong."

    def test_job_update_passed(self):
        passed = True
        self.sauce.jobs.update_job(self.driver.session_id, passed=passed)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['passed'] == passed, "Passed value from API wrong."

    def test_job_update_build(self):
        build = "test_build_x"
        self.sauce.jobs.update_job(self.driver.session_id, build=build)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['build'] == build, "Build value from API wrong."

    def test_job_update_custom_data(self):
        custom_data = {'custom': 'data',
                       'test_job': True,
                       'id-number': 4452231}
        self.sauce.jobs.update_job(self.driver.session_id, custom_data=custom_data)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['custom-data'] == custom_data, "Custom data from API wrong."


class TestJobAssets(unittest.TestCase):
    '''
    Test listing and downloading job assets.

    Requires the job to be finished before getting assets.
    '''

    @classmethod
    def setUpClass(cls):
        cls.driver = create_session()
        cls.sauce = sauce.Sauce(sauce_user, sauce_key)
        cls.session = cls.driver.session_id
        cls.sauce.jobs.stop_job(cls.session)

    def test_job_list_assets(self):
        resp = self.sauce.jobs.list_job_assets(self.session)
        assert 'sauce-log' in resp

    def test_job_download_asset(self):
        with tempfile.TemporaryFile() as tmpfile:
            tmpfile.write(self.sauce.jobs.download_job_asset(
                self.session, 'selenium-server.log')
            tmpfile.seek(0)
            self.assertIn('org.openqa.grid.selenium.GridLauncher', tmpfile.read(),
                          "File did not download properly.")


class TestJobAssetsDelete(unittest.TestCase):
    '''
    Test deleting job assets. Has to have it's own session to test this to
    be process-safe.
    '''

    def setUp(self):
        self.driver = create_session()
        self.sauce = sauce.Sauce(sauce_user, sauce_key)
        self.sauce.jobs.stop_job(self.driver.session_id)

    def test_job_asssets_delete(self):
        self.sauce.jobs.delete_job_assets(self.driver.session_id)
        try:
            self.sauce.jobs.download_job_asset(self.driver.session_id,
                                               'selenium-server.log')
        except HTTPError as err:
            if err.message == '404 Client Error: Not Found':
                return
            raise


class TestJobStopDelete(unittest.TestCase):
    '''
    Test stopping a job and deleting a job.
    '''

    def setUp(self):
        self.driver = create_session()
        self.sauce = sauce.Sauce(sauce_user, sauce_key)

    def test_job_stop(self):
        self.sauce.jobs.stop_job(self.driver.session_id)
        resp = self.sauce.jobs.get_job_details(self.driver.session_id)
        assert resp['error'] == 'User terminated', "Job not stopped."

    def test_job_delete(self):
        self.sauce.jobs.stop_job(self.driver.session_id)
        self.sauce.jobs.delete_job(self.driver.session_id)
        try:
            self.sauce.jobs.get_job_details(self.driver.session_id)
        except HTTPError as err:
            if err.message == '404 Client Error: Not Found':
                return
            raise
