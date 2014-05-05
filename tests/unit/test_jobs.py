import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import mock

from sauce import sauce

sauce_user = os.environ['SAUCE_USERNAME']
sauce_key = os.environ['SAUCE_ACCESS_KEY']


@mock.patch.object(sauce.Sauce, 'request')
class TestJobs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce(sauce_user, sauce_key)

    def test_list_jobs(self, mock_request):
        jobs_url = '/rest/v1/saucelabs-python/jobs'
        self.sauce.jobs.list_jobs()
        mock_request.assert_called_with('GET', jobs_url,
                                        params={})
        self.sauce.jobs.list_jobs(limit=1, full=True, skip=1)
        mock_request.assert_called_with('GET', jobs_url,
                                        params={'limit': 1,
                                                'full': True,
                                                'skip': 1
                                                }
                                        )

    def test_get_job_details(self, mock_request):
        self.sauce.jobs.get_job_details('123')
        mock_request.assert_called_with(
            'GET', '/rest/v1/saucelabs-python/jobs/123')

    def test_update_job(self, mock_request):
        self.sauce.jobs.update_job('123', build='456',
                                   custom_data={'my-data': '789'},
                                   name='test name', passed='False',
                                   public='False', tags=['tag1', 'tag2'])
        mock_request.assert_called_with('PUT',
                                        '/rest/v1/saucelabs-python/jobs/123',
                                        '{"name": "test name", '
                                        '"tags": ["tag1", "tag2"], '
                                        '"custom-data": {"my-data": "789"}, '
                                        '"build": "456", "passed": "False", '
                                        '"public": "False"}')

    def test_stop_job(self, mock_request):
        self.sauce.jobs.stop_job('123')
        mock_request.assert_called_with(
            'PUT', '/rest/v1/saucelabs-python/jobs/123/stop')

    def test_delete_job(self, mock_request):
        self.sauce.jobs.delete_job('123')
        mock_request.assert_called_with(
            'DELETE', '/rest/v1/saucelabs-python/jobs/123')

    def test_list_job_assets(self, mock_request):
        self.sauce.jobs.list_job_assets('123')
        mock_request.assert_called_with(
            'GET', '/rest/v1/saucelabs-python/jobs/123/assets')

    @mock.patch.object(sauce.Sauce, 'download')
    def test_download_job_asset(self, mock_download, mock_request):
        self.sauce.jobs.download_job_asset('123', 'file.log')
        mock_request.assert_not_called()
        mock_download.assert_called_with('/rest/v1/saucelabs-python/jobs/123/assets/file.log')

    def test_delete_job_assets(self, mock_request):
        self.sauce.jobs.delete_job_assets('123')
        mock_request.assert_called_with('DELETE', '/rest/v1/saucelabs-python/jobs/123/assets')
