saucelabs-python
================
[![Build Status](https://travis-ci.org/maudineormsby/saucelabs-python.svg?branch=master)](https://travis-ci.org/maudineormsby/saucelabs-python)

Saucelabs REST API client for python

Quickstart
----------

Import the library:

`from sauce import Sauce`

Then create an instance of the client:

`sauce = Sauce(YOUR_SAUCE_USERNAME, YOUR_SAUCE_ACCESS_KEY)`

Now you can use the client!

```
sauce.status()
sauce.browsers('webdriver')
sauce.jobs.list_jobs(skip=10)
```

Jobs
----

Each webdriver session has a corresponding job id in sauce. You can access
the job/session id in the webdriver object:

```
wd = webdriver.Firefox()
wd.session_id
```

Modify and inspect jobs and job status by using the jobs object:

```
sauce = Sauce(YOUR_SAUCE_USERNAME, YOUR_SAUCE_ACCESS_KEY)
jobs = sauce.jobs
jobs.get_job_details(wd.session_id)
jobs.stop_job(wd.session_id)
jobs.delete_job(wd.session_id)
```

Enjoy!
