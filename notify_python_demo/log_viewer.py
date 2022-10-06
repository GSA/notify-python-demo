import os

from dotenv import load_dotenv
from rich.table import Table as rich_table
from rich.console import Console
from notifications_python_client.notifications import NotificationsAPIClient


def __print_table(client, template_type, id, limit=None):
    console = Console()
    if template_type == "sms":
        vals = {"header": "Phone Number", "key": "phone_number"}
    else:
        vals = {"header": "Email Address", "key": "email_address"}
    response = client.get_all_notifications(template_type=template_type)
    data = []

    for r in response["notifications"]:
        row = ["", r[vals["key"]], r["status"], r["completed_at"]]
        if r["id"] == id:
            row[0] = "->"
            row = [f"[yellow on black]{e}[yellow on black]" for e in row]
        data.append(row)
    title = f"{template_type.upper()} Service Log"
    if limit:
        data = data[0:limit]
        title = f"{title} (last {str(limit)} entries)"

    table = rich_table(title=f"{title} {client.base_url}", row_styles=["dim", ""])
    headers = ["", vals["header"], "Status", "Completed"]
    for h in headers:
        table.add_column(h, justify="left")
    [table.add_row(d[0], d[1], d[2], d[3]) for d in data[0:limit]]
    console.print("\n")
    console.print(table)


def sms_log_table(client, id=None, limit=None):
    __print_table(client, template_type="sms", id=id, limit=limit)


def email_log_table(client, id=None, limit=None):
    __print_table(client, template_type="email", id=id, limit=limit)


def main():
    # STUFF FROM .env file
    load_dotenv()
    base_url = os.environ.get("BASE_URL")
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
