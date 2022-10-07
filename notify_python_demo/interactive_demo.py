import os
import sys
import re
from time import sleep

from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich import print
from notifications_python_client.notifications import NotificationsAPIClient

import log_viewer

# STUFF FROM .env file
load_dotenv()
base_url = os.environ.get("BASE_URL")
user_api_key = os.environ.get("USER_API_KEY")
iss_uuid = os.environ.get("ISS_UUID")
service_name = os.environ.get("SERVICE_NAME")
phone_number = os.environ.get("PHONE_NUMBER")
send_email_address = os.environ.get("SEND_EMAIL_ADDRESS")

concat_api_key = "_".join([service_name, iss_uuid, user_api_key])


def greeting():
    title = " * U.S. Notify Python Client Demo *  "
    short_stripe = " " * 26
    long_stripe = " " * 37
    c = Console()
    print("")
    c.print(" ********* ", style="white on navy_blue", end="")
    c.print(short_stripe, style="black on white")
    c.print(" ********* ", style="white on navy_blue", end="")
    c.print(short_stripe, style="black on red")
    c.print(" ********* ", style="white on navy_blue", end="")
    c.print(short_stripe, style="black on white")
    c.print(" ********* ", style="white on navy_blue", end="")
    c.print(short_stripe, style="black on red")

    c.print(title, style="black on white")
    c.print(long_stripe, style="black on red")
    c.print(long_stripe, style="black on white")
    c.print(long_stripe, style="black on red")

    c.print(" This program demonstrates some of the capabilities of the Notify Python")
    c.print(" client and the underlying API that drives it. Using the Notify API, you")
    c.print(" can access a live service's templates, send SMS and emails to recpients,")
    c.print(" and check detailed statuses of sent messages.")
    __divider()


def intro():
    send_type = Prompt.ask("Would you like to send an SMS or Email? --> ")
    while send_type.lower() not in ["sms", "email"]:
        send_type = Prompt.ask("Enter either SMS or Email for send type --> ")
    return send_type.lower()


def __divider():
    print("[red]-[/red]" * 80)


def print_template_description(template_type):
    __divider()
    print("")
    print(" For a given service and template type (SMS, email, letter),")
    print(" a list of templates and their associated metadata can be retrieved.")
    print(
        f" This is the Python function used to retrieve the {template_type} templates:"
    )
    print("")
    print(f"response = client.get_all_templates(template_type={template_type})")
    print("")


def print_send_description(template_type, template_id, personalisation):
    if template_type == "sms":
        send_string = f"phone_number='{phone_number}'"
        object_method = "send_sms_notification"
    else:
        send_string = f"email_address='{send_email_address}'"
        object_method = "send_email_notification"
    __divider()
    print("")
    print(" Once a template is selected and any template variables are set,")
    print(f" sending {template_type} is a simple call to the Python client object")
    print(" To sent the selected template, the client method is:")
    print("")
    print(f"response = client.{object_method}(")
    print(f"\t\t{send_string}',")
    print(f"\t\ttemplate_id='{template_id}',")
    print(f"\t\tpersonalisation={personalisation})")
    print("")
    __divider()

    print("")


def print_logview_description(template_type):
    __divider()
    print("")
    print(" Notify keeps a message log that can be queried by the API.")
    print(f" To get the {template_type} log, this client method can be issued:")
    print("")
    print(f"response = client.get_all_notifications(template_type={template_type})")
    print("")
    __divider()


def select_template(client, template_type):
    response = client.get_all_templates(template_type=template_type)
    templates = [x["body"] for x in response["templates"]]

    print_template_description(template_type)
    print(f"\nSelect one of the following {template_type} templates:")
    __divider()
    for idx, template in enumerate(templates, start=1):
        print(f"{idx}. {template}")
        __divider()

    valid_selections = [str(idx) for idx, x in enumerate(templates, start=1)]
    template_selection = Prompt.ask(f"({', '.join(valid_selections)})--> ")
    while template_selection not in valid_selections:
        template_selection = Prompt.ask(
            f"Valid Selections are: {', '.join(valid_selections)} --> "
        )

    template = response["templates"][int(template_selection) - 1]

    personalisation = {}
    pattern = re.compile(r"\(\((.*?)\)\)")
    match = pattern.findall(template["body"])
    for m in match:
        personalisation[m] = Prompt.ask(
            f"\nWhat value would you like to send for (({m})) --> "
        )

    return (template["id"], personalisation)


def prompt_to_send_it(client, template_type, template_id, personalisation):
    print_send_description(template_type, template_id, personalisation)
    send_it = Prompt.ask("Do you want to send it? (y|N) --> ")
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

            response = client.get_notification_by_id(id)
            if response["completed_at"] is None:
                print(
                    "Waiting up to 10 seconds to verify SMS sent successfully...",
                    end="",
                    flush=True,
                )
                inc = 1
                console = Console()
                msg = "[bold green]Waiting for successful send..."
                success = False
                with console.status(msg):
                    while inc <= 10:
                        inc = inc + 1
                        response = client.get_notification_by_id(id)
                        if response["completed_at"] is None:
                            sleep(1)
                            console.log(msg)
                        else:
                            success = True
                if success is True:
                    print("", flush=True)
                    log_viewer.sms_log_table(client, id=response["id"], limit=5)
                    print("", flush=True)
        else:
            response = client.send_email_notification(
                email_address=send_email_address,  # currently hard-coded from .env
                template_id=template_id,
                personalisation=personalisation,
            )
            print(f"Sending email to {send_email_address}...")
            sleep(2)
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
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
