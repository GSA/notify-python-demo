import os
import sys
import argparse
import logging
from dotenv import load_dotenv
from notifications_python_client.notifications import NotificationsAPIClient


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments using the argparse library
    return argparse object
    """
    parser = argparse.ArgumentParser(description='Options for testing python notify client')
    parser.add_argument('--send_sms', type=bool, help='send sms')
    parser.add_argument('--send_email', type=bool, help='send email')
    parser.add_argument('--number', type=str, help='phone number to send notification')
    parser.add_argument('--email', type=str, help='email address to send notification')
    args = parser.parse_args()

    return args

def check_and_send_sms(notifications_client, args):
    if not args.number:
        logging.error("Cannot send sms without phone number")
    if args.number:
        # validate phone number?
        response = notifications_client.send_sms_notification(
            phone_number=args.number,
            template_id="8ccb6087-abf9-469e-bce5-9a3b361dd4c2",
            personalisation={
                "day_of_week": "Wednesday",
                "colour": "Purple"
            }
        )
        print(response)


def main():
    load_dotenv()
    api_key = os.environ.get('USER_API_KEY')
    admin_api_key = os.environ.get('ADMIN_API_KEY')
    service_id = os.environ.get('ISS_UID')
    service_key_name = os.environ.get('SERVICE_NAME')
    concat_api_key = "_".join([service_key_name, service_id, api_key])
    base_url = "http://localhost:6011"

    # must pass in base_url, as the default is notify.uk's production URL
    notifications_client = NotificationsAPIClient(concat_api_key, base_url=base_url)
    
    args = parse_args()
    if len(sys.argv) == 0:
        print("Please pass in some arguments to run the script.")

    # todo: csv check/load here before others
    if args.send_sms:
        check_and_send_sms(notifications_client, args)

if __name__ == '__main__':
    main()
