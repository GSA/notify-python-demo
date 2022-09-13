import os

from dotenv import load_dotenv
from pprint import pprint
from notifications_python_client.notifications import NotificationsAPIClient


load_dotenv()

# hard-code API URL to local dev location
base_url = "http://localhost:6011"

# STUFF FROM .env file
user_api_key = os.environ.get("USER_API_KEY")
admin_api_key = os.environ.get("ADMIN_API_KEY")
iss_uid = os.environ.get("ISS_UUID")
service_name = os.environ.get("SERVICE_NAME")
template_id = os.environ.get("TEMPLATE_ID")
phone_number = os.environ.get("PHONE_NUMBER")

concat_api_key = "_".join([service_name, iss_uid, user_api_key])

# must pass in base_url, as the default is notify.uk's production URL
notifications_client = NotificationsAPIClient(concat_api_key, base_url=base_url)

#response = notifications_client.send_sms_notification(
#    phone_number=phone_number,
#    template_id=template_id,
#    personalisation={"day_of_week": "Wednesday", "colour": "Purple"},
#)

#response = notifications_client.get_template(template_id)

#response = notifications_client.get_all_templates(
#    template_type="sms" # optional string
#)

# get all SMS templates
# ask user which one to use, by body
# prompt for a y/n on whether you want an SMS to be sent to phone_number

#templates = [x['body'] for x in response['templates']]
#[print(f"{x}. {template}") for x, template in enumerate(templates, start=1)]
#print(response['templates'])

response = notifications_client.get_all_notifications(template_type="sms")
print("SMS Log")
print("Phone#     ", "Status  ", "Completed")
print("-----------", "--------", "---------")
for r in response['notifications']:
    print(r['phone_number'], f"{r['status']}    ", r['completed_at'])