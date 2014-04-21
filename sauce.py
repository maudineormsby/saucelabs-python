import json

import requests


class Sauce(object):

    def __init__(self, sauce_user, sauce_key):
        self.user = sauce_user
        self.key = sauce_key
        self.jobs = Jobs(self)

    def request(self, method, rel_url, data=None, params=None):
        base_url = 'https://{0}:{1}@saucelabs.com'.format(self.user, self.key)
        url = base_url + rel_url
        resp = requests.request(method, url, data=data, params=params)
        resp.raise_for_status()
        return resp.json()


class Jobs(object):

    def __init__(self, sauce):
        self.sauce = sauce

    def list_jobs(self, limit=False, full=False, skip=False):
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
        rel_url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce.user, session)
        return self.sauce.request('GET', rel_url)

    def update_job(self, session, name=False, tags=False, public=None, passed=None,
                   build=False, custom_data=False):
        rel_url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce.user, session)
        payload = {}
        if name:
            payload["name"] = name
        if tags:
            payload["tags"] = tags
        if public is not None:
            payload["public"] = public
        if passed is not None:
            payload["passed"] = passed
        if build:
            payload["build"] = build
        if custom_data:
            payload["custom-data"] = custom_data
        data = json.dumps(payload)
        return self.sauce.request('PUT', rel_url, data)

    def stop_job(self, session):
        rel_url = '/rest/v1/{0}/jobs/{1}/stop'.format(self.sauce.user, session)
        return self.sauce.request('PUT', rel_url)

    def delete_job(self, session):
        rel_url = '/rest/v1/{0}/jobs/{1}'.format(self.sauce.user, session)
        return self.sauce.request('DELETE', rel_url)
