import os

from nose.tools import raises
from requests.exceptions import HTTPError
from selenium import webdriver

import sauce

sauce_user = os.environ['SAUCE_USERNAME']
sauce_key = os.environ['SAUCE_ACCESS_KEY']


def create_session():
    sauce_exec = 'http://{0}:{1}@ondemand.saucelabs.com/wd/hub'
    sauce_url = sauce_exec.format(sauce_user, sauce_key)
    driver = webdriver.Remote(sauce_url, webdriver.DesiredCapabilities.FIREFOX)
    return driver


class TestJobs(object):
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
        assert resp[0]['id'] != self.driver.session_id

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


class TestJobStopDelete(object):
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

    @raises(HTTPError)
    def test_job_delete(self):
        self.sauce.jobs.stop_job(self.driver.session_id)
        self.sauce.jobs.delete_job(self.driver.session_id)
        self.sauce.jobs.get_job_details(self.driver.session_id)

# 	def test_job_from():
# 		# test date 'from'

# 	def test_job_to():
# 		# test date 'to'

# 	def test_job_to_from():
# 		# duh

# 	def test_job_csv():
# 		#test csv job info

# 	def test_job_information():
# 		#get job information for job we set up

# 	def test_job_update():
# 		# update some params
# 		# verify they changed

# class TestJobsStopDelete(object):

#     def setUp(self):
#         self.driver = create_session()

#     def tearDown(self):
#         self.driver.quit()

# # 	def test_job_delete():
# # 		# create a job
# # 		# delteeted
# # 		# del... taco?

#     def test_job_stop(self):
#         sauce.stop_job(self.driver.id)


# class JobsAssetsTest():
# 	'''
# 	Test Jobs assets.
# 	'''

# 	def setUpClass
# 	def tearDownClass
	
# 	def test_list_job_assets():
# 		# run a job
# 		# get a list of assets

# 	def test_download_job_assets():
# 		# yep, download bitches

# 	def remove_job_assets():
# 		# same song and dance

