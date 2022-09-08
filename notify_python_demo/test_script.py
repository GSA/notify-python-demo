import os 
from dotenv import load_dotenv
from notifications_python_client.notifications import NotificationsAPIClient
from pprint import pprint


load_dotenv()

# hard-code API URL to local dev location
base_url = "http://localhost:6011"

# STUFF FROM .env file
user_api_key = os.environ.get('USER_API_KEY')
admin_api_key = os.environ.get('ADMIN_API_KEY')
iss_uid = os.environ.get('ISS_UUID')
service_name = os.environ.get('SERVICE_NAME')
template_id = os.environ.get('TEMPLATE_ID')
phone_number = os.environ.get('PHONE_NUMBER')

concat_api_key = "_".join([service_name, iss_uid, user_api_key])

# must pass in base_url, as the default is notify.uk's production URL
notifications_client = NotificationsAPIClient(concat_api_key, base_url=base_url)

response = notifications_client.send_sms_notification(
    phone_number=phone_number,
    template_id=template_id,
    personalisation={
        "day_of_week": "Wednesday",
        "colour": "Purple"
    }
)

pprint(response)

