import sys
import os
import re
import time

from dotenv import load_dotenv
from colorama import init, Back, Fore
from notifications_python_client.notifications import NotificationsAPIClient

import log_viewer

# hard-code API URL to local dev location
base_url = "http://localhost:6011"

# STUFF FROM .env file
load_dotenv()
user_api_key = os.environ.get("USER_API_KEY")
admin_api_key = os.environ.get("ADMIN_API_KEY")
iss_uid = os.environ.get("ISS_UUID")
service_name = os.environ.get("SERVICE_NAME")
phone_number = os.environ.get("PHONE_NUMBER")
send_email_address = os.environ.get("SEND_EMAIL_ADDRESS")

concat_api_key = "_".join([service_name, iss_uid, user_api_key])


def greeting():
    init()
    title = " * U.S. Notify Python Client Demo * "
    short_stripe = " " * 28
    long_stripe = " " * 37
    print("")
    print(f"{Back.BLUE} ******* {Back.RESET}{Back.WHITE}{short_stripe}{Back.RESET}")
    print(f"{Back.BLUE} ******* {Back.RESET}{Back.RED}{short_stripe}{Back.RESET}")
    print(f"{Back.BLUE} ******* {Back.RESET}{Back.WHITE}{short_stripe}{Back.RESET}")
    print(f"{Back.RED}{long_stripe}{Back.RESET}")
    print(f"{Back.WHITE}{Fore.BLACK}{title} {Fore.RESET}{Back.RESET}")
    print(f"{Back.RED}{long_stripe}{Back.RESET}")
    print(f"{Back.WHITE}{long_stripe}{Back.RESET}")
    print(f"{Fore.RESET}")
    print(" This program demonstrates some of the capabilities of the Notify Python")
    print(" client and the underlying API that drives it. Using the Notify API, you")
    print(" can access a live service's templates, send SMS and emails to recpients,")
    print(" and check detailed statuses of sent messages.")
    print("")
    __divider()


def intro():
    send_type = input("Would you like to send an SMS or Email? --> ")
    while send_type.lower() not in ["sms", "email"]:
        send_type = input("Enter either SMS or Email for send type --> ")
    return send_type.lower()


def __divider():
    print("-" * 80)


def __command(command):
    print(f"{Fore.YELLOW}{Back.BLACK}{command}{Fore.RESET}{Back.RESET}")


def print_template_description(template_type):
    __divider()
    print("")
    print(" For a given service and template type (SMS, email, letter),")
    print(" a list of templates and their associated metadata can be retrieved.")
    print(" This is the Python function used to retrieve the {template_type} below:")
    print("")
    __command(f"response = client.get_all_templates(template_type={template_type})")
    print("")


def print_send_description(template_type, template_id, personalisation):
    __divider()
    print("")
    print(" Once a template is selected and any template variables are set,")
    print(f" sending {template_type} is a simple call to the Python client object")
    print(" To sent the selected template, the client method is:")
    print("")
    __command("response = client.send_sms_notification(")
    __command(f"\t\tphone_number='{phone_number}',")
    __command(f"\t\ttemplate_id='{template_id}',")
    __command(f"\t\tpersonalisation={personalisation})")
    print("")
    __divider()

    print("")


def print_logview_description(template_type):
    __divider()
    print("")
    print(" Notify keeps a message log that can be queried by the API.")
    print(f" To get the {template_type} log, this client method can be issued:")
    print("")
    __command(f"response = client.get_all_notifications(template_type={template_type})")
    print("")
    __divider()


def select_template(client, template_type):
    response = client.get_all_templates(template_type=template_type)
    templates = [x["body"] for x in response["templates"]]

    print_template_description(template_type)
    print(f"\nSelect one of the following {template_type} templates:")
    print("-" * 30)
    [print(f"{idx}. {template}") for idx, template in enumerate(templates, start=1)]
    print("-" * 30)

    valid_selections = [str(idx) for idx, x in enumerate(templates, start=1)]
    template_selection = input("--> ")
    while template_selection not in valid_selections:
        template_selection = input(
            f"Valid Selections are: {', '.join(valid_selections)} --> "
        )

    template = response["templates"][int(template_selection) - 1]

    personalisation = {}
    pattern = re.compile(r"\(\((.*?)\)\)")
    match = pattern.findall(template["body"])
    for m in match:
        personalisation[m] = input(
            f"\nWhat value would you like to send for (({m})) --> "
        )

    return (template["id"], personalisation)


def prompt_to_send_it(client, template_type, template_id, personalisation):
    print_send_description(template_type, template_id, personalisation)
    print("Do you want to send it?")
    send_it = input("Y or N [default: N] --> ")
    if send_it.lower() == "y":
        # send it!
        print_logview_description(template_type)
        if template_type == "sms":
            response = client.send_sms_notification(
                phone_number=phone_number,  # currently hard-coded from .env
                template_id=template_id,
                personalisation=personalisation,
            )
            id = response["id"]
            print(f"Sending SMS to {phone_number}...")
            log_viewer.sms_log_table(client, id=id, limit=5)
            print(
                "Waiting up to 10 seconds to verify SMS sent successfully...",
                end="",
                flush=True,
            )
            inc = 1
            while inc <= 10:
                inc = inc + 1
                response = client.get_notification_by_id(id)
                if response["completed_at"] is None:
                    time.sleep(1)
                    print(".", end="", flush=True)
                else:
                    print("", flush=True)
                    log_viewer.sms_log_table(client, id=response["id"], limit=5)
                    break
            print("", flush=True)
        else:
            response = client.send_email_notification(
                email_address=send_email_address,  # currently hard-coded from .env
                template_id=template_id,
                personalisation=personalisation,
            )
            print(f"Sending email to {send_email_address}...")
            time.sleep(2)
            log_viewer.email_log_table(client, id=response["id"], limit=5)
    else:
        print(f"{template_type} send cancelled")


def main():
    # must pass in base_url, as the default is notify.uk's production URL
    client = NotificationsAPIClient(concat_api_key, base_url=base_url)

    # introduce yourself
    greeting()

    # and ask if SMS or email template is desired
    template_type = intro()

    # present selections for SMS/email templates
    template_id, personalisation = select_template(client, template_type)

    # present y/n to send
    prompt_to_send_it(client, template_type, template_id, personalisation)


if __name__ == "__main__":
    main()
