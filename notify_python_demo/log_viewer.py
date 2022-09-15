import os

from dotenv import load_dotenv
from tabulate import tabulate
from colorama import init, Back, Fore
from notifications_python_client.notifications import NotificationsAPIClient


def __print_table(client, template_type, id, limit=None):
    init()
    if template_type == "sms":
        vals = {"header": "Phone Number", "key": "phone_number"}
    else:
        vals = {"header": "Email Address", "key": "email_address"}
    response = client.get_all_notifications(template_type=template_type)
    headers = ["", vals["header"], "Status", "Completed"]
    data = []
    for r in response["notifications"]:
        row = ["", r[vals["key"]], r["status"], r["completed_at"]]
        if r["id"] == id:
            row[0] = "->"
            row = [f"{Back.YELLOW}{Fore.BLACK}{e}{Fore.RESET}{Back.RESET}" for e in row]
        data.append(row)
    if limit:
        data = data[0:limit]
        print(f"{template_type.upper()} Log (last {str(limit)} entries)")
    else:
        print(f"{template_type.upper()} Log")
    print(
        tabulate(
            data[0:limit],
            headers=headers,
            tablefmt="simple_outline",
            stralign="left",
        )
    )
    print("\n")


def sms_log_table(client, id=None, limit=None):
    __print_table(client, template_type="sms", id=id, limit=limit)


def email_log_table(client, id=None, limit=None):
    __print_table(client, template_type="email", id=id, limit=limit)


def main():
    # hard-code API URL to local dev location
    base_url = "http://localhost:6011"

    # STUFF FROM .env file
    load_dotenv()
    user_api_key = os.environ.get("USER_API_KEY")
    iss_uid = os.environ.get("ISS_UUID")
    service_name = os.environ.get("SERVICE_NAME")

    concat_api_key = "_".join([service_name, iss_uid, user_api_key])

    # must pass in base_url, as the default is notify.uk's production URL
    notifications_client = NotificationsAPIClient(concat_api_key, base_url=base_url)

    # print the log tables
    sms_log_table(notifications_client)
    email_log_table(notifications_client)


if __name__ == "__main__":
    main()