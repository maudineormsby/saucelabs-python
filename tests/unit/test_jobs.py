try:
    import unittest2 as unittest
except ImportError:
    import unittest

import json
import mock

import sauce


@mock.patch.object(sauce.Sauce, 'request')
class TestJobs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sauce = sauce.Sauce('sauce-user', 'sauce-key')

    def test_list_jobs(self, mock_request):
        jobs_url = '/rest/v1/sauce-user/jobs'
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
            'GET', '/rest/v1/sauce-user/jobs/123')

    def test_update_job(self, mock_request):
        params = {u'build': u'456',
                  u'custom_data': {u'my-data': u'789'},
                  u'name': u'test name', 
                  u'passed': u'False',
                  u'public': u'False', 
                  u'tags': [u'tag1', u'tag2']
                  }
        self.sauce.jobs.update_job('123', **params)
        _, _, payload = mock_request.call_args[0]
        args_dict = json.loads(payload)
        # custom_data becomes custom-data
        params[u'custom-data'] = params.pop(u'custom_data')
        self.assertEqual(params, args_dict)

    def test_stop_job(self, mock_request):
        self.sauce.jobs.stop_job('123')
        mock_request.assert_called_with(
            'PUT', '/rest/v1/sauce-user/jobs/123/stop')

    def test_delete_job(self, mock_request):
        self.sauce.jobs.delete_job('123')
        mock_request.assert_called_with(
            'DELETE', '/rest/v1/sauce-user/jobs/123')

    def test_list_job_assets(self, mock_request):
        self.sauce.jobs.list_job_assets('123')
        mock_request.assert_called_with(
            'GET', '/rest/v1/sauce-user/jobs/123/assets')

    @mock.patch.object(sauce.Sauce, 'download')
    def test_download_job_asset(self, mock_download, mock_request):
        self.sauce.jobs.download_job_asset('123', 'file.log')
        mock_request.assert_not_called()
        mock_download.assert_called_with('/rest/v1/sauce-user/jobs/123/assets/file.log')

    def test_delete_job_assets(self, mock_request):
        self.sauce.jobs.delete_job_assets('123')
        mock_request.assert_called_with('DELETE', '/rest/v1/sauce-user/jobs/123/assets')
