# Notify Python Client Demo QUICKSTART

* Doing this demo requires a running local Notify API. Run the notifications-api repo in a dev container. In a container terminal, run `make run-flask`. After that's running, in another container terminal run `make run-celery`. This will get the API running locally and the base URL will be http://localhost:6011
* copy sample.env to .env
* look at notifications-api .env file and copy the value in ADMIN_CLIENT_SECRET to ADMIN_API_KEY
* through the Notify web UI, choose a service that the demo will interact with, and make sure that a few templates have been mocked up for both SMS and email.
* login to Notify web UI and generate a user API key for that service (XXX: better instructions here)
* copy that API key into .env for the USER_API_KEY value
* install `poetry` locally (https://python-poetry.org/docs/)
* after `poetry` is installed, run `poetry install`, which will create a virtual environment for running the demo, including all package dependencies
* run `poetry shell` to invoke a shell using this new virtual environment
* there are three demo files available, all in the notify_python_demo/ folder: `test_script.py`, `interactive_demo.py`, and `log_viewer.py`.
* any of these scripts can be invoked with `python notify_python_demo/<script>.py`. Details below.

# test_script.py

test_script.py is intended to demonstrate how to send SMS or email, including to a list of users from a csv file:

```
usage: test_script.py [-h] [--send_sms SEND_SMS] [--send_email SEND_EMAIL]
[--number NUMBER] [--email EMAIL] [--csv CSV] [--path PATH] [--filename FILENAME]

Options for testing python notify client

optional arguments:
  -h, --help            show this help message and exit
  --send_sms SEND_SMS   send sms
  --send_email SEND_EMAIL
                        send email
  --number NUMBER       phone number to send notification
  --email EMAIL         email address to send notification
  --csv CSV             send bulk message
  --path PATH           path to directory where csv file resides
  --filename FILENAME   csv file name
  ```

To send via CSV, you will need the `--csv` `bool` flag, the `--path` and the `--filename` options.
Currently, the csv send functionality is set to send bulk messages per template. This means that you will
need to have the `template_id` and all of the `personalisation` attributes will need to be individual columns in your csv. And, as of now, you will need to modify the code to match those personalisations.

For example, if you have a template which has two personalisations: `((day_of_the_week))` and `((color))`,
you will need to have a `day_of_the_week` column and a `color` column in your csv, in addition to either `number` or `email` and `template_id`.

# interactive_demo.py

This script is an interactive demonstration of sending SMS or email from Notify. It will read templates and determine if there are any template variables to populate, then will send the message and give real-time updates of the message success in sending.

`python notify_python_demo/interactive_demo.py`

# log_viewer.py

This script will dump the SMS and email logs in tabular format to the console.

`python notify_python_demo/log_viewer.py`

This script is also importable as a module and is used by interactive_demo.py
```
import log_viewer

...
# client is a NotificationsAPIClient object (see interactive_demo.py code for details)
log_viewer.sms_log_table(client)
log_viewer.email_log_table(client)

```