import os
import sys
import csv
import argparse
import logging
from dotenv import load_dotenv
from notifications_python_client.notifications import NotificationsAPIClient


# todo: figure out how to do personalisation object in csv??
ACCEPTABLE_COLUMNS = [
    "number",
    "email",
    "first_name",
    "template_id",
    "day_of_week",
    "colour",
]


def parse_args():
    """
    Parse command line arguments using the argparse library
    return argparse object
    """
    parser = argparse.ArgumentParser(
        description="Options for testing python notify client"
    )
    parser.add_argument("--send_sms", type=bool, help="send sms")
    parser.add_argument("--send_email", type=bool, help="send email")
    parser.add_argument("--number", type=str, help="phone number to send notification")
    parser.add_argument("--email", type=str, help="email address to send notification")
    parser.add_argument("--csv", type=bool, help="send bulk message")
    parser.add_argument(
        "--path",
        type=str,
        help="path to directory where csv file resides",
        default="csv_data",
    )
    parser.add_argument("--filename", type=str, help="csv file name")

    args = parser.parse_args()

    return args


def check_and_process_csv_file(notifications_client, args):
    if not args.path or not args.filename:
        logging.error(
            "You need to pass in both the path and filename to process a csv file"
        )
    else:
        with open(
            os.path.join(args.path, args.filename), mode="r", encoding="utf-8-sig"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            column_names = reader.fieldnames
            print("Passed in columns: {}".format(column_names))
            for col in column_names:
                if col not in ACCEPTABLE_COLUMNS:
                    raise logging.error("Cannot have {} column name".format(col))
            if "number" in column_names:
                # do stuff to send bulk sms
                for row in reader:
                    send_sms(
                        notifications_client,
                        number=row["number"],
                        day_of_week=row["day_of_week"],
                        colour=row["colour"],
                        template_id=row["template_id"],
                    )
            if "email" in column_names:
                # send email
                for row in reader:
                    send_email(
                        notifications_client,
                        email=row["email"],
                        first_name=row["first_name"],
                        template_id=row["template_id"],
                    )


def send_sms(notifications_client, **kwargs):
    # todo: make template_id a param?
    response = notifications_client.send_sms_notification(
        phone_number=kwargs.get("number"),
        template_id=kwargs.get("template_id"),
        personalisation={
            "day_of_week": kwargs.get("day_of_week"),
            "colour": kwargs.get("colour"),
        },
    )
    print("--------------------")
    print(response)


def send_email(notifications_client, **kwargs):
    # todo: add personalisations according to template_id?
    response = notifications_client.send_email_notification(
        email_address=kwargs.get("email"),
        template_id=kwargs.get("template_id"),
        personalisation={"first_name": kwargs.get("first_name")},
    )
    print("-------------------")
    print(response)


def main():
    load_dotenv()
    api_key = os.environ.get("USER_API_KEY")
    service_id = os.environ.get("ISS_UUID")
    service_key_name = os.environ.get("SERVICE_NAME")
    concat_api_key = "_".join([service_key_name, service_id, api_key])
    base_url = os.environ.get("BASE_URL")

    # must pass in base_url, as the default is notify.uk's production URL
    notifications_client = NotificationsAPIClient(concat_api_key, base_url=base_url)

    args = parse_args()
    if len(sys.argv) == 0:
        print("Please pass in some arguments to run the script.")

    if args.csv:
        check_and_process_csv_file(notifications_client, args)
    elif args.send_sms:
        if not args.number:
            logging.error("Cannot send sms without phone number")
        else:
            send_sms(notifications_client, number=args.number)
    elif args.send_email:
        if not args.email:
            logging.error("Cannot send email without email address")
        else:
            send_email(notifications_client, email=args.email)


if __name__ == "__main__":
    main()
