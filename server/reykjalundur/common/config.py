import os

message_disconnect: dict = {
    "subject": "Some subject",
    "body": "Some body",
}

message_reconnect: dict = {
    "subject": "Some subject",
    "body": "Some body",
}

recipients = os.environ["RECIPIENT"].split(",")
email_enabled: bool = True if os.environ["EMAIL_ENABLED"] else False
