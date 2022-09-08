# Notify Python Client QUICKSTART

* run notifications-api repo in a dev container, including `make run-flask` and `make run-celery` that listens at http://localhost:6011 as an API base URL
* look at notifications-api .env file and copy the value in ADMIN_CLIENT_SECRET to ADMIN_API_KEY
* copy sample.env to .env
* login to Notify web UI and get an API key (XXX: better instructions here)
* copy API key to the value for USER_API_KEY in .env file

