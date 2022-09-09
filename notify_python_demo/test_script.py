import os 
from dotenv import load_dotenv
from notifications_python_client.notifications import NotificationsAPIClient


load_dotenv()
api_key = os.environ.get('USER_API_KEY')
admin_api_key = os.environ.get('ADMIN_API_KEY')
service_id = os.environ.get('ISS_UID')
service_key_name = os.environ.get('SERVICE_NAME')

concat_api_key = "_".join([service_key_name, service_id, api_key])
# must pass in base_url, as the default is notify.uk's production URL
notifications_client = NotificationsAPIClient(concat_api_key, base_url="http://localhost:6011")

response = notifications_client.send_sms_notification(
    phone_number="18016525984",
    template_id="8ccb6087-abf9-469e-bce5-9a3b361dd4c2",
    personalisation={
        "day_of_week": "Wednesday",
        "colour": "Purple"
    }
)

print(response)
