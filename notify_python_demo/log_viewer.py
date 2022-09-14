import os

from dotenv import load_dotenv
from tabulate import tabulate
from notifications_python_client.notifications import NotificationsAPIClient


def print_table(title, headers, data):
    """Renders a formatted table."""
    print(title)
    print("-" * len(title))
    print(
        tabulate(
            data,
            headers=headers,
            tablefmt="pipe",
            stralign="left",
        )
    )
    print("\n")


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

response = notifications_client.get_all_notifications(template_type="sms")
sms_headers = ["Phone Number", "Status", "Completed"]
sms_data = [
    [r["phone_number"], r["status"], r["completed_at"]]
    for r in response["notifications"]
]

print_table("SMS Log", sms_headers, sms_data)

response = notifications_client.get_all_notifications(template_type="email")
email_headers = ["Email Address", "Status", "Completed"]
email_data = [
    [r["email_address"], r["status"], r["completed_at"]]
    for r in response["notifications"]
]
print_table("Email Log", email_headers, email_data)
