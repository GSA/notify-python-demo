# Notify Python Client Demo QUICKSTART

- **Doing this demo requires a running Notify API and Notify Admin**.
- To create a local development instance of Notify API and Notify Admin:
   - Follow [Notify API's Quickstart](https://github.com/GSA/notifications-api#quickstart) and get the API running in a VS Code docker container. After this is up and confirmed running, follow [Notify Admin's Quickstart](https://github.com/GSA/notifications-admin#quickstart) to get the web UI up and running. 
- In the Notify web UI, create a login for a user and go through all the necessary hoops to verify the account. Using a dispostable.com email address is a good way to configure an ephemeral user for the service and avoids any pitfalls of spam filters and the like. Note: after registering an email you will need to respond to a confirmation email in order to verify the address to AWS.
- In this repo, copy the file `sample.env` to `.env`
- In `.env`, configure the BASE_URL to the correct value for the API you will be querying. If running locally, the default of http://localhost:6011 will work without modification. 
- Go to the Notify web UI and choose (or create) a service that the demo will interact with. Make sure this service has a few templates mocked up for both SMS and email.
- From the chosen service, go to the dashboard and then select Login to Notify web UI and generate a user API key for that service (note, this is currently blocked in the UI. There is a privately shared workaround covered in the last few paragraphs of [this document](https://docs.google.com/document/d/1S5c-LxuQLhAtZQKKsECmsllVGmBe34Z195sbRVEzUgw/edit#)).
  - Copy the API key to your clipboard.
  - This API key string is composed of three sections, separated by hyphens: `[SERVICE_NAME]-[ISS_UUID]-[USER_API_KEY]`.
    - The name of your API key as you named it in the Web UI is the first section. Copy this value into the .env file for the variable `SERVICE_NAME`.
    - The remaining two sections are of equal length, 36 characters. Split the string into 36 character sections (removing the hyphen between the two), and copy them both into the .env file for the values of `ISS_UUID` and `USER_API_KEY`, respectively.
- Install `poetry` locally (https://python-poetry.org/docs/)
- After `poetry` is installed, from the home directory of this repository run `poetry install`. This will create a virtual environment for running the demo, including all package dependencies
- Run `poetry shell` to invoke a shell using this new virtual environment.
- There are three demo files available, all in the notify_python_demo/ folder: `test_script.py`, `interactive_demo.py`, and `log_viewer.py`.
- Any of these scripts can now be invoked with `python notify_python_demo/<script>.py`. Details on the individual scripts are below.

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

# interactive_demo.py

This script is an interactive demonstration of sending SMS or email from Notify. It will read templates and determine if there are any template variables to populate, then will send the message and give real-time updates of the message success in sending.

`python notify_python_demo/interactive_demo.py`

# log_viewer.py

This script will dump the SMS and email logs for a service in tabular format to the console.

`python notify_python_demo/log_viewer.py`

This script is also importable as a module and is used by interactive_demo.py
```
import log_viewer

...
# client is a NotificationsAPIClient object (see interactive_demo.py code for details)
log_viewer.sms_log_table(client)
log_viewer.email_log_table(client)

```