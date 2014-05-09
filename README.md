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

Enjoy!