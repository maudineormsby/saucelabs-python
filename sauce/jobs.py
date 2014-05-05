import json


class Jobs(object):

    def __init__(self, sauce):
        self.sauce = sauce

    def list_jobs(self, full=False, limit=False, skip=False):
        """
        List all jobs for the account.

        Uses the saucelabs username and access key in self.sauce.

        Args:
          full: return all job details not only job id.
          limit: max number of jobs to return.
          skip: number of jobs to skip

        Returns:
          List of JSON objects containing id of jobs (or all details if
          full=True).
        """
        payload = {}
        if limit:
            payload['limit'] = limit
        if full:
            payload['full'] = full
        if skip:
            payload['skip'] = skip
        rel_url = '/rest/v1/{0}/jobs'.format(self.sauce.user)
        return self.sauce.request('GET', rel_url, params=payload)

    def get_job_details(self, session):
        """
        Get details for the specified job.

        Args:
          session: the session id of the job to get details for.

        Returns:
          JSON object containing job information.
        """
        rel_url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce.user, session)
        return self.sauce.request('GET', rel_url)

    def update_job(self, session, build=False, custom_data=False, name=False,
                   passed=None, public=None, tags=False):
        rel_url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce.user, session)
        payload = {}
        if name:
            payload['name'] = name
        if tags is not False:
            payload['tags'] = tags
        if public is not None:
            payload['public'] = public
        if passed is not None:
            payload['passed'] = passed
        if build:
            payload['build'] = build
        if custom_data:
            payload['custom-data'] = custom_data
        data = json.dumps(payload)
        return self.sauce.request('PUT', rel_url, data)

    def stop_job(self, session):
        rel_url = '/rest/v1/{0}/jobs/{1}/stop'.format(self.sauce.user, session)
        return self.sauce.request('PUT', rel_url)

    def delete_job(self, session):
        rel_url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce.user, session)
        return self.sauce.request('DELETE', rel_url)

    def list_job_assets(self, session):
        rel_url = '/rest/v1/{0}/jobs/{1}/assets'.format(self.sauce.user, session)
        return self.sauce.request('GET', rel_url)

    def download_job_asset(self, session, asset):
        """
        Download job asset from sauce.

        Args:
          session: session id for sauce job.
          asset: name of asset to download.

        Returns:
          The contents of the asset from the server, as a bytestring.
        """
        rel_url = '/rest/v1/{0}/jobs/{1}/assets/{2}'.format(
            self.sauce.user, session, asset)
        return self.sauce.download(rel_url)

    def delete_job_assets(self, session):
        rel_url = '/rest/v1/{0}/jobs/{1}/assets'.format(self.sauce.user, session)
        return self.sauce.request('DELETE', rel_url)
